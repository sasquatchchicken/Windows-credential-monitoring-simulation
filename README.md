# Windows-credential-monitoring-simulation
## The pwsh script helps users understand how credentials are stored and potentially exposed on a Windows system. 

Captures Stored Windows Credentials:

Uses the cmdkey command to list stored credentials on the system.

Saves the output to a file named 
```
credentials_log.txt.
```
Extracts Saved Browser Passwords:

Detects and backs up the Chrome and Edge browser password databases (Login Data files).
Copies these files to the current directory for further analysis.
```
Chrome_LoginData_Backup
Edge_LoginData_Backup
```
## The python script decrypts AES-encrypted passwords stored in the Chrome browser's Login Data file.
Reads the Chrome Login Data SQLite database to retrieve encrypted passwords, URLs, and usernames.

Extracts the AES key from the Chrome Local State file.

Decrypts the passwords using the AES key.

Outputs the decrypted URLs, usernames, and passwords.

## USAGE
install the following dependencies
```
pip install pywin32
pip install pycryptodome
sqlite3 is built into python3
```
```
First run decrypt_cred_grabber.ps1
in the python script
update db_path = Chrome_LoginData_Backup #this is the directory path of the Chrome_LoginData_Backup
update local_state_path = "C:\Users\<USERNAME_OF_TARGET_MACHINE>\AppData\Local\Google\Chrome\User Data\Local State"
then python decrypt_AES.py
```
## OUTPUT
```
URL: https://github.com/session, Username: <the_username_in_plain_text>, Password: b'<the_password_in_plain_text>'
If the decrypted data is not valid UTF-8:
b'\x9e\x8d\xe9<\xe7\xf7s.\x9d\xc8\xc2\x19L\xe7\xdf\xe2'
```
**Simulate credential extraction and decryption**
## Not responsible if these scripts are used for malicious purposes! These scripts are for educational purposes only.
