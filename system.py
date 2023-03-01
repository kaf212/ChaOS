import ChaOS_constants
import csv

def reset_syslog():
    with open('syslog.csv', 'w', encoding='utf-8') as csv_file:
        attributes = ChaOS_constants.SYSLOG_CSV_ATTRIBUTES
        csv_writer = csv.DictWriter(csv_file, fieldnames=attributes)
        csv_writer.writeheader()
        csv_file.close()


def syslog(category, msg):
    if category not in ChaOS_constants.SYSLOG_CATEGORIES:
        raise ValueError(f'Invalid syslog category "{category}" given. ')

    with open('syslog.csv', 'r', encoding='utf-8') as csv_file:
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

    with open('syslog.csv', 'a+', encoding='utf-8') as csv_file:
        attributes = ChaOS_constants.SYSLOG_CSV_ATTRIBUTES
        csv_writer = csv.DictWriter(csv_file, fieldnames=attributes)
        csv_writer.writerow({'ID': index, 'category': category, 'msg': msg})


def show_syslog():
    with open('syslog.csv', 'r', encoding='utf-8') as csv_file:
        attributes = ChaOS_constants.SYSLOG_CSV_ATTRIBUTES
        next(csv_file)
        csv_reader = csv.DictReader(csv_file, fieldnames=attributes)
        for line in csv_reader:
            print(f"id: {line['ID']}, category: {line['category']}, msg: {line['msg']}")
