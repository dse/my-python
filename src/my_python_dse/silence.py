import os

stderr_fd = None                # also tells us if silent is on
disabled = False

if "DISABLE_SILENCE" in os.environ:
    disabled = True

def silence(flag=True):
    global disabled, stderr_fd
    if disabled:
        pass
    elif flag is None:
        # Disable permanently.  Future attemps to turn silence off or
        # back on do nothing.
        silence(False)
        disabled = True
    elif flag:                  # turn silence on
        if stderr_fd is None:
            stderr_fd = os.dup(2)
            os.close(2)
    else:                       # turn silence off
        if stderr_fd is not None:
            os.dup2(stderr_fd, 2)
            stderr_fd = None

def on():
    silence(True)

def off():
    silence(False)

def disable():
    silence(None)

def is_silent():
    global stderr_fd
    return stderr_fd is None
