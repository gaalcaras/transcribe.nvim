from datetime import datetime, timedelta

def msg(nvim, expr):
    string = (expr if isinstance(expr, str) else str(expr))
    nvim.call('transcribe#util#print_msg', string, async=True)


def error(nvim, expr):
    string = (expr if isinstance(expr, str) else str(expr))
    nvim.call('transcribe#util#print_error', string, async=True)


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
    time = datetime.strptime(time, fmt)
    duration = timedelta(hours=time.hour,
                         minutes=time.minute,
                         seconds=time.second)

    return duration.total_seconds()
