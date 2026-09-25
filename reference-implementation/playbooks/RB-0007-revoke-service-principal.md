# RB-0007 — Revoke an Entra ID Service Principal Grant

| Field | Value |
| --- | --- |
| Runbook ID | RB-0007 |
| Version | 1.0.0 |
| Parent playbook | PB-0003 |
| Required role | Cloud Application Administrator or Global Administrator |
| Estimated duration | 10 minutes |

> **Preserve before you destroy.** Every step below is irreversible from an
> evidence standpoint. Complete step 1 before anything else.

## 1. Preserve evidence

```powershell
Connect-MgGraph -Scopes "Directory.Read.All","AuditLog.Read.All"

$spId = "<service-principal-object-id>"

Get-MgServicePrincipal -ServicePrincipalId $spId |
    ConvertTo-Json -Depth 10 | Out-File "evidence/$spId-serviceprincipal.json"

Get-MgOauth2PermissionGrant -Filter "clientId eq '$spId'" |
    ConvertTo-Json -Depth 10 | Out-File "evidence/$spId-delegated-grants.json"

Get-MgServicePrincipalAppRoleAssignment -ServicePrincipalId $spId |
    ConvertTo-Json -Depth 10 | Out-File "evidence/$spId-approle-assignments.json"
```

## 2. Enumerate the blast radius

Identify every identity that consented, not only the one in the alert.

```powershell
Get-MgOauth2PermissionGrant -Filter "clientId eq '$spId'" |
    Select-Object Id, ConsentType, PrincipalId, Scope |
    Format-Table -AutoSize
```

`ConsentType` of `AllPrincipals` means tenant-wide admin consent. Every user is
affected. Escalate to Critical.

## 3. Remove delegated permission grants

```powershell
Get-MgOauth2PermissionGrant -Filter "clientId eq '$spId'" | ForEach-Object {
    Remove-MgOauth2PermissionGrant -OAuth2PermissionGrantId $_.Id -Confirm:$false
    Write-Host "Removed delegated grant $($_.Id)"
}
```

## 4. Remove application permission assignments

```powershell
Get-MgServicePrincipalAppRoleAssignment -ServicePrincipalId $spId | ForEach-Object {
    Remove-MgServicePrincipalAppRoleAssignment `
        -ServicePrincipalId $spId -AppRoleAssignmentId $_.Id -Confirm:$false
    Write-Host "Removed app role assignment $($_.Id)"
}
```

## 5. Disable the service principal

Disable rather than delete. Deletion destroys the audit trail.

```powershell
Update-MgServicePrincipal -ServicePrincipalId $spId -AccountEnabled:$false
```

## 6. Revoke issued tokens

**This step is mandatory.** Removing consent does not invalidate access tokens
already issued. Without it the adversary retains access until token expiry.

```powershell
$affectedUsers = @("j.mbeki@contoso.com")

foreach ($upn in $affectedUsers) {
    Revoke-MgUserSignInSession -UserId $upn
    Write-Host "Revoked sessions for $upn"
}
```

## 7. Verify

```powershell
Get-MgOauth2PermissionGrant -Filter "clientId eq '$spId'"          # expect empty
Get-MgServicePrincipalAppRoleAssignment -ServicePrincipalId $spId  # expect empty
(Get-MgServicePrincipal -ServicePrincipalId $spId).AccountEnabled  # expect False
```

## 8. Record

Attach evidence files to the incident ticket. Record the service principal
object ID, application ID and the list of affected identities. Confirm in the
ticket that step 6 was completed; token revocation is the step most often
skipped, and skipping it means the containment did not work.
