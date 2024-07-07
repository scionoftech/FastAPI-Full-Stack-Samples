import random
import string

def generate_api_key(length=32):
    characters = string.ascii_letters + string.digits
    api_key = ''.join(random.choice(characters) for _ in range(length))
    return api_key

# Generate an API key of default length 32
api_key = generate_api_key()
print(api_key)
