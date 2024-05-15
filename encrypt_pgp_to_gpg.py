import gnupg
from pprint import pprint

# Initialize the GPG object
gpg = gnupg.GPG()

# Path to the recipient's public PGP key
public_key_path = 'path/to/public_key.asc'  # Replace with the actual path
# Data you want to encrypt
data_to_encrypt = "This is a secret message."
# Output file for encrypted data
output_file_path = 'encrypted_output.gpg'   # Replace with your desired output path

# Import the recipient's public key
with open(public_key_path, 'rb') as f:
    public_key_data = f.read()
import_result = gpg.import_keys(public_key_data)
if import_result:
    pprint(import_result.results)
    # Assuming you want the first key in the imported batch
    recipient_key_id = import_result.fingerprints[0]  
else:
    print("Public key import failed.")
    exit(1)

# Encrypt the data using the imported key, trusting it implicitly
encrypt_result = gpg.encrypt(data_to_encrypt, recipient_key_id, always_trust=True)
if encrypt_result.ok:
    encrypted_data = str(encrypt_result)
    print("Encryption successful!")
    
    # Save encrypted data to file
    with open(output_file_path, 'wb') as f:
        f.write(encrypted_data.encode('utf-8'))  # Write as binary data
        print(f"Encrypted data saved to {output_file_path}")
else:
    print("Encryption failed!")
    print("Status:", encrypt_result.status)
    print("Error message:", encrypt_result.stderr)
