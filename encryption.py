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

    print(binary_string)
