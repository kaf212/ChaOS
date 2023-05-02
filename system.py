import ChaOS_constants
import csv
from colors import *
from datetime import datetime
import os


def reset_syslog():
    with open('A/System42/logging/syslog.csv', 'w', encoding='utf-8') as csv_file:
        attributes = ChaOS_constants.SYSLOG_CSV_ATTRIBUTES
        csv_writer = csv.DictWriter(csv_file, fieldnames=attributes)
        csv_writer.writeheader()
        csv_file.close()


def syslog(category, msg):
    if category not in ChaOS_constants.SYSLOG_CATEGORIES:
        raise ValueError(f'Invalid syslog category "{category}" given. ')

    with open('A/System42/logging/syslog.csv', 'r', encoding='utf-8') as csv_file:
        attributes = ChaOS_constants.SYSLOG_CSV_ATTRIBUTES
        next(csv_file)
        csv_reader = csv.DictReader(csv_file, fieldnames=attributes)
        log_list = []
        for line in csv_reader:
            log_list.append(line)
        try:
            latest_log = log_list[-1]
            index = log_list.index(latest_log) + 1
        except IndexError:
            index = 0
    now = get_formatted_time()
    with open('A/System42/logging/syslog.csv', 'a+', encoding='utf-8') as csv_file:
        attributes = ChaOS_constants.SYSLOG_CSV_ATTRIBUTES
        csv_writer = csv.DictWriter(csv_file, fieldnames=attributes)
        csv_writer.writerow({'ID': index, 'time': now, 'category': category, 'msg': msg})


def get_formatted_time() -> str:
    now = datetime.now()
    if now.minute < 10:
        now = f'{now.hour}:0{now.minute}'
    else:
        now = f'{now.hour}:{now.minute}'
    return now


def show_syslog():
    with open('A/System42/logging/syslog.csv', 'r', encoding='utf-8') as csv_file:
        attributes = ChaOS_constants.SYSLOG_CSV_ATTRIBUTES
        next(csv_file)
        csv_reader = csv.DictReader(csv_file, fieldnames=attributes)

        for line in csv_reader:
            output = f"{line['ID']} - {line['time']}\t[{line['category']}]:\t\t{line['msg']}"
            if line['category'] == 'deletion':
                print_red(output)
            elif line['category'] == 'creation':
                print_green(output)
            elif line['category'] == 'alteration':
                print_orange(output)
            else:
                print(output)


def display_ipconfig(cmd_split):
    import subprocess  # that was not my idea honestly

    try:
        if cmd_split[1] == 'all':
            result = subprocess.run(['ipconfig', '/all'], capture_output=True, text=True, encoding='ANSI')
            output = result.stdout
            output = output.replace('Windows', 'ChaOS')
            output = output.replace('Konfiguration', 'Configuration')
            print(output)
    except IndexError:
        result = subprocess.run(['ipconfig'], capture_output=True, text=True, encoding='ANSI')
        output = result.stdout
        output = output.replace('Windows', 'ChaOS')
        output = output.replace('Konfiguration', 'Configuration')
        print(output)
