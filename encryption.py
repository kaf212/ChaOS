def encrypt_str(string):
    string_list = list(string)
    string_list_enc = []

    for char in string_list:
        string_list_enc.append(encrypt_char(char))

    string_enc = ''.join(string_list_enc)

    return string_enc


def decrypt_str(string):
    string_list = list(string)
    string_list_decr = []

    for char in string_list:
        string_list_decr.append(decrypt_char(char))

    string_enc = ''.join(string_list_decr)

    return string_enc


def encrypt_char(char):
    char_unicode = str_unicode(char)
    char_bin = dec_bin(char_unicode)
    char_bin_inv = invert_bin(char_bin)
    char_hex = hex(int(char_bin_inv, 2))
    char_unicode_enc = chr(int(char_hex, 16))

    return char_unicode_enc


def decrypt_char(char_unicode_enc):
    char_hex = char_unicode_enc.encode('latin-1')
    try:
        char_hex.decode('utf-8')
    except UnicodeDecodeError:
        pass
    char_bin_inv = hex_bin(char_hex)
    char_bin = invert_bin(char_bin_inv)
    char_dec = bin_dec(char_bin)
    char_hex = hex(char_dec)

    char_decrypted = chr(int(char_hex, 16))
    return char_decrypted


def hex_bin(hex):
    dec_list = list(hex)
    bin_list = []
    for dec in dec_list:
        bin_list.append(dec_bin(dec))

    bin_str = ''.join(bin_list)

    return bin_str


def str_unicode(string):
    str_unicode_list = []
    for char in list(string):
        str_unicode_list.append(ord(char))

    unicode_str = ''
    for char in str_unicode_list:
        unicode_str += str(char)

    unicode_int = int(unicode_str)

    return unicode_int


def dec_bin(dec):
    """
    oh my, it's so sexy
    :param dec:
    :return a minimum 8 bit binary string:
    """
    bin_list = []
    while dec != 0:
        rest = dec % 2
        dec = (dec - rest) / 2
        bin_list.insert(0, rest)

    while len(bin_list) % 8 != 0:
        bin_list.insert(0, 0)

    binary_string = ''
    for binary in bin_list:
        binary = int(binary)
        binary_string += str(binary)

    return binary_string


def invert_bin(binary):
    """
    partially inverts a binary string
    :return:
    """
    bin_list = list(binary)
    i = 0
    for binary in bin_list:
        if i % 2 == 0:
            if binary == '1':
                bin_list.insert(i, '0')
            if binary == '0':
                bin_list.insert(i, '1')
            bin_list.pop(i + 1)
        i += 1

    bin_str = ''
    for binary in bin_list:
        bin_str += binary

    return bin_str

def bin_dec(binary):
    dec = int(binary, 2)
    return dec