# Repo-wide mechanical normalisation for the v2.1 restructure.
# Removes emoji, strips hardcoded Mermaid theming, normalises spelling and whitespace.
# Run from the repository root:  pwsh ./reference-implementation/tools/normalise-docs.ps1

[CmdletBinding()]
param(
    [string[]] $Path = @('.', 'reference-implementation', 'tools-and-templates', 'assessment'),
    [switch]   $WhatIfOnly
)

$ErrorActionPreference = 'Stop'

$excludedDirs = @('.venv', 'venv', 'site', 'node_modules', '.git')

$emojiChar = '(?:[\uD800-\uDBFF][\uDC00-\uDFFF]|[\u2300-\u23FF\u2460-\u24FF\u25A0-\u25FF\u2600-\u27BF\u2B00-\u2BFF\u3030\u303D\uFE0F\u200D\u20E3])'
$emojiRun  = "(?:$emojiChar)+ ?"

# en-GB -> en-US, plus documented typo corrections.
# Flat from/to pair list: PowerShell flattens nested arrays and hashtable keys are case-insensitive.
$textFixes = @(
    'organisational', 'organizational',
    'organisation',   'organization',
    'Organisation',   'Organization',
    'behavioural',    'behavioral',
    'behaviour',      'behavior',
    'Behaviour',      'Behavior',
    'prioritisation', 'prioritization',
    'prioritised',    'prioritized',
    'prioritise',     'prioritize',
    'normalisation',  'normalization',
    'normalised',     'normalized',
    'normalise',      'normalize',
    'categorised',    'categorized',
    'categorise',     'categorize',
    'utilised',       'utilized',
    'utilise',        'utilize',
    'minimise',       'minimize',
    'optimised',      'optimized',
    'optimise',       'optimize',
    'defences',       'defenses',
    'defence',        'defense',
    'analysed',       'analyzed',
    'analyse',        'analyze',
    'cataloguing',    'cataloging',
    'Cataloguing',    'Cataloging',
    'catalogue',      'catalog',
    'Catalogue',      'Catalog',
    'labelled',       'labeled',
    'modelling',      'modeling',
    'before we look at th phases', 'before we look at the phases',
    'In taddition',   'In addition',
    'Feasibilty',     'Feasibility',
    'Improvment',     'Improvement',
    'develped',       'developed',
    "Exception's Handling", 'Exception Handling',
    'Spear Fishing',  'Spear Phishing'
)

function Convert-MarkdownFile {
    param([string] $File)

    $raw   = [System.IO.File]::ReadAllText($File)
    $orig  = $raw
    $lines = $raw -split "`r?`n"

    $out       = New-Object System.Collections.Generic.List[string]
    $inFence   = $false
    $fenceLang = ''

    foreach ($line in $lines) {

        if ($line -match '^\s*```(\w*)') {
            if (-not $inFence) {
                $inFence = $true
                $fenceLang = $Matches[1]
                # markdownlint MD040: an unlabelled fence is treated as plain text.
                if (-not $fenceLang) {
                    $out.Add(($line -replace '```\s*$', '```text'))
                    $fenceLang = 'text'
                    continue
                }
            }
            else { $inFence = $false; $fenceLang = '' }
            $out.Add($line); continue
        }

        # Drop hardcoded Mermaid theming so diagrams follow the reader's colour scheme.
        if ($inFence -and $fenceLang -eq 'mermaid') {
            if ($line -match '^\s*(style\s+\S+\s+fill:|classDef\s+\w+\s+fill:|linkStyle\s|%%\s*Styling)') { continue }
        }

        $new = [regex]::Replace($line, $emojiRun, '')

        if (-not $inFence) {
            # Collapse runs of spaces inside the content only. Leading whitespace
            # is significant: it keeps list continuations and nested items intact.
            if ($new -match '^(\s*)(.*)$') {
                $indent = $Matches[1]
                $body   = [regex]::Replace($Matches[2], '  +', ' ')
                $new    = $indent + $body
            }
            $new = [regex]::Replace($new, '^(#{1,6})\s*', '$1 ')
            $new = $new.TrimEnd()
        }

        $out.Add($new)
    }

    $text = ($out -join "`n")

    for ($i = 0; $i -lt $textFixes.Count; $i += 2) {
        $text = [regex]::Replace($text, [regex]::Escape($textFixes[$i]), $textFixes[$i + 1])
    }

    # Tidy blank-line runs left behind by removed style blocks.
    $text = [regex]::Replace($text, "(`n[ \t]*){3,}`n", "`n`n")

    # Guarantee one blank line either side of a fenced block.
    $spaced  = New-Object System.Collections.Generic.List[string]
    $fenceOn = $false
    foreach ($l in ($text -split "`n")) {
        $isFence = $l -match '^\s*```'
        if ($isFence -and -not $fenceOn) {
            if ($spaced.Count -gt 0 -and $spaced[$spaced.Count - 1].Trim() -ne '') { $spaced.Add('') }
            $spaced.Add($l); $fenceOn = $true; continue
        }
        if ($isFence -and $fenceOn) { $spaced.Add($l); $spaced.Add(''); $fenceOn = $false; continue }
        if (-not $fenceOn -and $l.Trim() -eq '' -and $spaced.Count -gt 0 -and $spaced[$spaced.Count - 1].Trim() -eq '') { continue }
        $spaced.Add($l)
    }
    $text = ($spaced -join "`n")

    $text = [regex]::Replace($text, "(`n[ \t]*){3,}`n", "`n`n")
    if (-not $text.EndsWith("`n")) { $text += "`n" }

    if ($text -ne $orig) {
        if (-not $WhatIfOnly) {
            [System.IO.File]::WriteAllText($File, $text, (New-Object System.Text.UTF8Encoding($false)))
        }
        return $true
    }
    return $false
}

$changed = 0
$seen = New-Object System.Collections.Generic.HashSet[string]
foreach ($p in $Path) {
    if (-not (Test-Path $p)) { continue }
    $recurse = ($p -ne '.')
    $files = if ($recurse) { Get-ChildItem -Path $p -Recurse -Filter *.md -File }
             else          { Get-ChildItem -Path $p -Filter *.md -File }
    $files | Where-Object {
        $rel = $_.FullName.Replace($PWD.Path + [IO.Path]::DirectorySeparatorChar, '')
        -not ($excludedDirs | Where-Object { $rel -like "$_$([IO.Path]::DirectorySeparatorChar)*" })
    } | ForEach-Object {
        if (-not $seen.Add($_.FullName)) { return }
        if (Convert-MarkdownFile -File $_.FullName) {
            $changed++
            Write-Host "normalised  $($_.FullName.Replace($PWD.Path + [IO.Path]::DirectorySeparatorChar, ''))"
        }
    }
}
Write-Host ""
Write-Host "Files changed: $changed"
