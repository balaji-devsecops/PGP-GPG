import gnupg
from pprint import pprint

# Path to the private key file and details
private_key_path = 'path/to/private.key'  # Replace with the path to your private key file
passphrase = 'your_passphrase'            # Replace with your passphrase
key_id = '8845B9457FBD48FF'               # The ID of the key you need for decryption
encrypted_file_path = 'encrypted_file.gpg' # Replace with path to the encrypted file

# Create a GPG object with the correct home directory and GPG binary
gpg = gnupg.GPG(gnupghome='/path/to/gnupg/home', gpgbinary='gpg')  # Set the correct paths

# Check if the required private key is in the keyring
private_keys = gpg.list_keys(True)
found_key = any(key for key in private_keys if key_id in key['keyid'])
print("Have the right private key? ", found_key)

# Import private key if not found
if not found_key:
    print("Importing private key {}...".format(private_key_path))
    with open(private_key_path, "rb") as f:
        key_data = f.read()
    import_result = gpg.import_keys(key_data)
    pprint(import_result.results)
    found_key = import_result.count > 0

# Decrypt the file if the secret key is available
if found_key:
    with open(encrypted_file_path, 'rb') as f:
        encrypted_data = f.read()
        
    print("Trying to decrypt the file...")
    decrypted_data = gpg.decrypt(encrypted_data, passphrase=passphrase)

    if decrypted_data.ok:
        print("Decryption successful!")
        # Assuming the decrypted data is text, you can print or save it
        print("Decrypted data:", decrypted_data.data.decode('utf-8'))
        
        # Optionally, save the decrypted data to a file
        with open('decrypted_output.txt', 'w') as f:
            f.write(decrypted_data.data.decode('utf-8'))
    else:
        print("Decryption failed!")
        print("Status:", decrypted_data.status)
        print("Error message:", decrypted_data.stderr)
else:
    print("Private key not found in the keyring and could not be imported!")
