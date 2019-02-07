from datetime import datetime, timedelta
import re

def msg(nvim, expr):
    string = expr if isinstance(expr, str) else str(expr)
    nvim.out_write('[transcribe] {}\n'.format(string))


def error(nvim, expr):
    string = expr if isinstance(expr, str) else str(expr)
    nvim.async_call('transcribe#util#print_error', string)


def fmtseconds(seconds=0, fmt='{H}:{M}:{S}'):
    """Format a number of seconds into a human readable string"""
    dms_time = {}

    dms_time['H'], remainder = divmod(seconds, 3600)
    dms_time['M'], dms_time['S'] = divmod(remainder, 60)

    for time_unit, value in dms_time.items():
        dms_time[time_unit] = '{:02d}'.format(round(value))

    return fmt.format(**dms_time)


def time_to_seconds(time, fmt='%H:%M:%S'):
    """Convert a time string to total number of seconds"""
    try:
        time = datetime.strptime(time, fmt)
    except ValueError:
        time = datetime.strptime(time, '%M:%S')

    duration = timedelta(hours=time.hour,
                         minutes=time.minute,
                         seconds=time.second)

    return duration.total_seconds()


def get_timecodes(line):
    """Return timecodes in line"""

    pattern = re.compile(r'\[([0-9]{2}:)?[0-5][0-9]:[0-5][0-9]\]')
    matches = re.finditer(pattern, line)
    timecodes = []

    for match in matches:
        timecodes.append({
            'timecode': match[0],
            'start_index': match.span(0)[0],
            'end_index': match.span(0)[1]
            })

    if timecodes == []:
        return None
    else:
        return timecodes
