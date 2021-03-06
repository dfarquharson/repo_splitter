import os
import datetime
from git import execute as _git
from git import log_to_dict as _log
from sys import argv
from time import strptime
from time import strftime
from pprint import pprint


def get_log(repo):
    cwd = os.getcwd()
    os.chdir(repo)
    log = _log(_git(['log'])[0])
    os.chdir(cwd)
    return log


def get_next_revision(log):
    for l in log:
        if 'jstauffe' not in l['Author']:
            yield l


def get_specific_date(entry, key):
    return entry[key]['Date'].split('+')[0].strip() \
        if 'Date' in entry[key] else ''


def get_time(entry, key):
    date = get_specific_date(entry, key)
    return strptime(date[:-6] if '-' in date else date,
                    '%a %b %d %H:%M:%S %Y')


def calc_days(entry):
    if entry['previous_revision'] and entry['last_revision']:
        t1 = get_time(entry, 'last_revision')
        t2 = get_time(entry, 'previous_revision')
        return str((datetime.datetime(*t1[:6]) -
                    datetime.datetime(*t2[:6])).days)
    else:
        return '0'


def get_report(directory):
    entries = []
    for d in os.listdir(directory):
        repodir = (directory if directory.endswith('/') else directory+'/')+d
        log = get_log(repodir)
        rev_generator = get_next_revision(log)
        try:
            last_rev = rev_generator.next()
        except StopIteration:
            last_rev = ''
        try:
            prev_rev = rev_generator.next()
        except StopIteration:
            prev_rev = ''
        entry = {'xnet': d,
                 'last_revision': last_rev,
                 'previous_revision': prev_rev,
                 'days_between_revisions': ''}
        entry['days_between_revisions'] = calc_days(entry)
        entries.append(entry)
    return entries


def get_murica_time(entry, key):
    return strftime('%m/%d/%Y', get_time(entry, key))


def set_murica_dates(entries):
    for e in entries:
        if e['last_revision'] != '':
            e['last_revision']['Date'] = get_murica_time(e, 'last_revision')
        if e['previous_revision'] != '':
            e['previous_revision']['Date'] = get_murica_time(e, 'previous_revision')


def write_to_csv(entries):
    set_murica_dates(entries)
    csv = 'xnet,last_revision,previous_revision,days_between_revisions\n'
    for entry in entries:
        csv += entry['xnet'] + ',' + \
               (entry['last_revision']['Date'] \
               if entry['last_revision'] != '' else '') + ',' + \
               (entry['previous_revision']['Date'] \
               if entry['previous_revision'] != '' else '') + ',' + \
               entry['days_between_revisions'] + '\n'
    return csv


if __name__ == '__main__':
    print(write_to_csv(get_report(argv[1]))
          if len(argv) >= 2 else 'usage: python finance.py /dir/to/report/on/')
