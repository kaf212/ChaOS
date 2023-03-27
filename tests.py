import os

from encryption import *
from input import *
from main import *
from login import *
from user import *
from csv_handling import *
from ChaOS_DevTools import *
import shutil

# f'A/ChaOS_Users/{user_dir}'

# for user_dir in os.listdir('A/ChaOS_Users'):  # delete directories of non existent users
#     if user_dir not in return_user_names():
#         shutil.rmtree(f'A/ChaOS_Users/{user_dir}')



print(decrypt_str("âÏÆÆÅÞÂÏØÏùÉÂÅÅÆÃÙÍÅÃÄÍÍÅÅÎËÙËÆÝËÓÙøÏÞßØÄÃÄÍÝËÙßÄÌÅØÞßÄËÞÏÓÏÞÄÅÞÎÃÙËÙÞØÅßÙëÙãÉËÄÙÏÏÓÅßËØÏÌËÇÃÆÃËØÝÃÞÂÞÂÏÙÅßØÉÏÉÅÎÏÅÌéÂËåùüÏØÓÍÅÅÎøÏÍËØÎÙþÂÏîÅÃÄÍßÙþÅËÙÞÏØ"))


# Hello there
# thereSchool is going good as always. Returning was unfortunate, yet not disastrous.
# As I can see, you are familiar with the source code of ChaOS. Very good.
# Regards, The Doingus Toaster
print(encrypt_str("Hello there\nSchool is going good as always. Returning was unfortunate, yet not disastrous.\nAs I can see, you are familiar with the source code of ChaOS. Very good.\nRegards, The Doingus Toaster"))
print(decrypt_str("âÏÆÆÅÞÂÏØÏ ùÉÂÅÅÆÃÙÍÅÃÄÍÍÅÅÎËÙËÆÝËÓÙøÏÞßØÄÃÄÍÝËÙßÄÌÅØÞßÄËÞÏÓÏÞÄÅÞÎÃÙËÙÞØÅßÙ ëÙãÉËÄÙÏÏÓÅßËØÏÌËÇÃÆÃËØÝÃÞÂÞÂÏÙÅßØÉÏÉÅÎÏÅÌéÂËåùüÏØÓÍÅÅÎ øÏÍËØÎÙþÂÏîÅÃÄÍßÙþÅËÙÞÏØ"))
print(decrypt_str("âÏÆÆÅÞÂÏØÏ ùÉÂÅÅÆÃÙÍÅÃÄÍÍÅÅÎËÙËÆÝËÓÙøÏÞßØÄÃÄÍÝËÙßÄÌÅØÞßÄËÞÏÓÏÞÄÅÞÎÃÙËÙÞØÅßÙ ëÙãÉËÄÙÏÏÓÅßËØÏÌËÇÃÆÃËØÝÃÞÂÞÂÏÙÅßØÉÏÉÅÎÏÅÌéÂËåùüÏØÓÍÅÅÎ øÏÍËØÎÙþÂÏîÅÃÄÍßÙþÅËÙÞÏØ"))





# reset_user_csv()

# dict_1 = [{'name': 'seve', 'password': 'mc'}]
# try:
#     os.mkdir('A/ChaOS_Users/new_dir', 0o777)
#     f = open('A/ChaOS_Users/new_dir/an_existing_file.txt', 'w')
#     f.close()
# except FileExistsError:
#     pass
# os.remove('A/ChaOS_Users/new_dir/an_existing_file.txt')
# os.rmdir('A/ChaOS_Users/new_dir')
#
# for file in os.listdir('A/ChaOS_Users/test_dir'):
#     os.remove(f'A/ChaOS_Users/test_dir/{file}')


# alter_user_csv('account type', old_value='admin', new_value='admin')
# alter_user_csv_pw('Seve', 'MINECRAFT_2')


# edit_user(['edit', 'user', 'kaf221122'])


# owner = User('kaf221122', '1234')
# # create_file(owner)
# read_txt('test.txt', owner)
# filename = find_file(owner)
# read_txt(filename, owner)
# letter_u = ord('a')
# print(letter_u)
# dec_bin(letter_u)

# string = 'this is motherfucking insane'
# string_list = list(string)
# string_list_enc = []
#
# for char in string_list:
#     string_list_enc.append(encrypt_char(char))
#
# string_enc = ''.join(string_list_enc)
#
# print(string_enc)
# input_selection(['a', 'b', 'c', 'd'], ['opt a', 'opt b', 'opt c', 'opt d'], 'What u want? ')
# split_path('A/ChaOS_Users/kaf221122/dir_test.txt')
# ui = translate_dir_2_ui('A/ChaOS_Users/kaf221122')
# print(ui)
# dir = translate_ui_2_dir(ui)
# print(dir)

# for path, subdirs, files in os.walk('A/ChaOS_Users'):
# for name in subdirs:
#     print(name)5
# for name in files:
#     print(name)
# print(path)
# user = login()
# print(user.account_type)
# dir_owners = {'A/ChaOS_Users/kaf221122': 'kaf221122',
#               'A/ChaOS_Users/NexToNothing': 'NexToNothing',
#               'A/ChaOS_Users/Custoomer31': 'Custoomer31',
#               'A/ChaOS_Users/Seve': 'Seve',
#               'A/ChaOS_Users/Manu': 'Manu',
#               }
# user = User(name='test_user', password='asdf', account_type='admin')
# print(user.account_type)
# print(validate_dir_access(path='A/ChaOS_Users/kaf221122', user=user, dir_owners=dir_owners))

# list_selection_options('asdf', ['opt_a', 'opt_b', 'opt_c', 'opt_d'])