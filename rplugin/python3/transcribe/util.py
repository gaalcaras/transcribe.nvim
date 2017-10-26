def msg(nvim, expr):
    string = (expr if isinstance(expr, str) else str(expr))
    nvim.call('transcribe#util#print_msg', string, async=True)

def error(nvim, expr):
    string = (expr if isinstance(expr, str) else str(expr))
    nvim.call('transcribe#util#print_error', string, async=True)
