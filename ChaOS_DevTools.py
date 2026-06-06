import csv
import ChaOS_constants
from encryption import *
from TNTFS import File


def reset_user_csv(reset_flag):
    """
    Genocide tool for test users.
    normal reset: only deletes users with "test" in their name.
    hard reset: deletes all non default users.
    :return:
    """

    if reset_flag == '-hard':
        with open('users.csv', 'w', encoding="utf-8") as csv_file:
            attributes = ChaOS_constants.USER_CSV_ATTRIBUTES
            csv_writer = csv.DictWriter(csv_file, fieldnames=attributes)
            csv_writer.writeheader()
            csv_writer.writerow(
                {'name': 'kaf221122', 'password': '', 'account type': 'dev'})
            csv_writer.writerow(
                {'name': 'NextToNothing', 'password': 'ËÙÎÌ', 'account type': 'dev'})
            csv_writer.writerow(
                {'name': 'the_razors_edge', 'password': 'ËÇÅÍßÙ', 'account type': 'admin'})
            csv_writer.writerow(
                {'name': 'Custoomer31', 'password': 'ÙÜÚ', 'account type': 'standard'})
            csv_writer.writerow(
                {'name': 'Seve', 'password': 'ÇÃÄÏÉØËÌÞ', 'account type': 'standard'})
            csv_writer.writerow(
                {'name': 'Manu', 'password': 'ÙÞÆßÞÐÃ', 'account type': 'standard'})
            csv_file.close()
            return
    else:
        temp_dict_list = []
        with open('users.csv', 'r', encoding='utf-8') as csv_file:   # read in every user in users.csv and add it to a temp dict if it doesnt contain "test"
            attributes = ChaOS_constants.USER_CSV_ATTRIBUTES
            csv_reader = csv.DictReader(csv_file, fieldnames=attributes)
            next(csv_file)
            for line in csv_reader:
                if 'test' not in line['name']:
                    temp_dict_list.append(line)

        with open('users.csv', 'w', encoding='utf-8') as csv_file:  # overwrite the csv with the temp dict
            attributes = ChaOS_constants.USER_CSV_ATTRIBUTES
            csv_writer = csv.DictWriter(csv_file, fieldnames=attributes)
            csv_writer.writeheader()
            for line in temp_dict_list:
                csv_writer.writerow(line)
            csv_file.close()

def initialize_user_dir_metadata():
    """
    Creates metadata entries for existing user directories that are missing them.
    Does not modify any existing metadata or directories.
    """
    with open('users.csv', 'r', encoding='utf-8') as csv_file:
        attributes = ChaOS_constants.USER_CSV_ATTRIBUTES
        csv_reader = csv.DictReader(csv_file, fieldnames=attributes)
        next(csv_file)  # Skip header
        for line in csv_reader:
            username = line['name']
            # Create metadata for main user directory
            user_dir = File(
                name=username,
                type='dir',
                path=f'A/ChaOS_Users/{username}',
                location='A/ChaOS_Users',
                owner=username,
                access_perm=[username]
            )
            if not user_dir.metadata_exists():
                user_dir.log_metadata()