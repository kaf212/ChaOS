def encrypt_str(string):
    string_list = list(string)
    string_list_enc = []

    for char in string_list:
        string_list_enc.append(encrypt_char(char))

    string_enc = ''.join(string_list_enc)

    return string_enc


def encrypt_char(char):
    string_unicode = str_unicode(char)
    string_bin = dec_bin(string_unicode)
    string_bin_inv = invert_bin(string_bin)
    string_hex = hex(int(string_bin_inv, 2))
    string_unicode_enc = chr(int(string_hex, 16))

    return string_unicode_enc


def decrypt(string):
    pass


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
