from encryption import encrypt_str, decrypt_str


def test_1():
    strings = ['hello world', '  kaf212  ', '+"*ç%&/()=']
    strings_enc = []
    for string in strings:
        strings_enc.append(encrypt_str(string))

    print(strings_enc)

    strings_decr = []
    for string_enc in strings_enc:
        strings_decr.append(decrypt_str(string_enc))

    assert strings_decr == strings
