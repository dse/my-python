import os

stderr_fd = os.dup(2)
disabled = False
if "DISABLE_SILENCE" in os.environ:
    disabled = True

def silence(flag=True):
    global disabled
    global stderr_fd
    if disabled:
        return
    if flag is None:
        disabled = True
        os.dup2(stderr_fd, 2)
    elif flag:
        os.close(2)
    else:
        os.dup2(stderr_fd, 2)

def on():
    silence(True)

def off():
    silence(False)
