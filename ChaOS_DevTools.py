import csv
import ChaOS_constants
from encryption import *


def reset_user_csv(cmd_split):
    """
    Genocide tool for test users.  dev reset user_csv -hard
    :return:
    """
    reset_flag = None
    try:
        reset_flag = cmd_split[3]
    except IndexError:
        pass

    if reset_flag == '-hard':
        with open('users.csv', 'w', encoding="utf-8") as csv_file:
            attributes = ChaOS_constants.USER_CSV_ATTRIBUTES
            csv_writer = csv.DictWriter(csv_file, fieldnames=attributes)
            csv_writer.writeheader()
            csv_writer.writerow(
                {'name': 'kaf221122', 'password': encrypt_str(decrypt_str('')), 'account type': 'dev'})
            csv_writer.writerow(
                {'name': 'NextToNothing', 'password': encrypt_str(decrypt_str('ËÙÎÌ')), 'account type': 'dev'})
            csv_writer.writerow(
                {'name': 'Custoomer31', 'password': encrypt_str(decrypt_str('ÙÜÚ')), 'account type': 'admin'})
            csv_writer.writerow(
                {'name': 'Seve', 'password': encrypt_str(decrypt_str('ÇÃÄÏÉØËÌÞ')), 'account type': 'standard'})
            csv_writer.writerow(
                {'name': 'Manu', 'password': encrypt_str(decrypt_str('ÙÞÆßÞÐÃ')), 'account type': 'standard'})
            csv_file.close()
    else:
        temp_dict_list = []
        with open('users.csv', 'r', encoding='utf-8') as csv_file:
            attributes = ChaOS_constants.USER_CSV_ATTRIBUTES
            csv_reader = csv.DictReader(csv_file, fieldnames=attributes)
            next(csv_file)
            for line in csv_reader:
                if 'test' not in line['name']:
                    temp_dict_list.append(line)

        with open('users.csv', 'w', encoding='utf-8') as csv_file:
            attributes = ChaOS_constants.USER_CSV_ATTRIBUTES
            csv_writer = csv.DictWriter(csv_file, fieldnames=attributes)
            csv_writer.writeheader()
            for line in temp_dict_list:
                csv_writer.writerow(line)
            csv_file.close()
