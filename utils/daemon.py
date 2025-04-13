import os
import sys

def daemonize():
    """
    Daemonizes the current process.

    This function detaches the process from the terminal and runs it in the
    background as a daemon. It performs the following steps:
    1. Forks the process and exits the parent to create a background process.
    2. Creates a new session and becomes the session leader to detach from any
       terminal.
    3. Forks again and exits the parent to prevent the daemon from acquiring
       a controlling terminal.
    4. Closes the standard output and error file descriptors.

    This is typically used for running processes that don't require user interaction
    and should run in the background.
    """

    if os.fork() > 0: sys.exit(0)
    os.setsid()
    if os.fork() > 0: sys.exit(0)
    sys.stdout.close()
    sys.stderr.close()