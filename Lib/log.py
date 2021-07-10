import datetime
import sys


def Debug(string):
    curr_time_string = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(curr_time_string, end='')
    print(' : ', end='')
    print(string)
    sys.stdout.flush()
