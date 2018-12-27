def cryptor(text, key, amount_encryption):
    position_key = 0
    crypt_text = ''
    len_key = len(key)
    if int(amount_encryption) > 1:
        for i in range(0, int(amount_encryption)):
            for letter in text:
                crypt_text = crypt_text + str(chr(ord(letter) + ord(key[position_key % len_key])))
                position_key += 1
            return crypt_text
    else:
        for letter in text:
            crypt_text = crypt_text + str(chr(ord(letter) + ord(key[position_key % len_key])))
            position_key += 1
        return crypt_text


def decryptor(text, key, number_decryptions):
    position_key = 0
    decrypt_text = ''
    len_key = len(key)
    if int(number_decryptions) > 1:
        for i in range(0, int(number_decryptions)):
            for letter in text:
                decrypt_text = decrypt_text + str(chr(ord(letter) - ord(key[position_key % len_key ])))
                position_key += 1
            return decrypt_text
    else:
        for letter in text:
            decrypt_text = decrypt_text + str(chr(ord(letter) - ord(key[position_key % len_key])))
            position_key += 1
        return decrypt_text

if __name__ == "main":
    pass