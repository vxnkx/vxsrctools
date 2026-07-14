from files.algorithm import encrypt_data
def encrypt_file(key, nonce, input_file):

    
    with open(input_file, 'rb') as file:
        payload = file.read()

    
    encrypted_payload, tag = encrypt_data(key, nonce, payload)

    return encrypted_payload, tag