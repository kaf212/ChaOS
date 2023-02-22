import csv
import ChaOS_constants
from encryption import *


def reset_user_csv():
    """
    Genocide tool for test users.
    :return:
    """
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
