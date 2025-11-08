import hashlib

# Function to generate SHA-256 hash
def generate_sha256_hash(input_string):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(input_string.encode())
    return sha256_hash.hexdigest()

# Get input from terminal
user_input = input("Enter text to hash (SHA-256): ")

# Generate hash
hash_value = generate_sha256_hash(user_input)

# Display the result
print(f"SHA-256 Hash: {hash_value}")
