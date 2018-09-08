"""All system related functions."""

import os
import subprocess
import sys

COMMAND_PREFIX = ">>>"
COMMAND_INVOKED_CANNOT_EXECUTE = 126
KEYBOARD_INTERRUPT = 130


def __call(*popenargs, timeout=None, **kwargs):
    """Run command with arguments.  Wait for command to complete or
    timeout, then return the returncode attribute.

    The arguments are the same as for the Popen constructor.  Example:

    retcode = __call(["ls", "-l"])
    """
    proc = subprocess.Popen(*popenargs, **kwargs)
    try:
        return proc.wait(timeout=timeout)
    except KeyboardInterrupt:
        try:
            proc.send_signal(subprocess.signal.SIGINT)
            while proc.poll() is None:
                continue
        except Exception:
            proc.kill()
            raise
        finally:
            raise
    except Exception:
        proc.kill()
        raise


def __check_call(*popenargs, **kwargs):
    """Run command with arguments.  Wait for command to complete.  If
    the exit code was zero then return, otherwise raise
    CalledProcessError.  The CalledProcessError object will have the
    return code in the returncode attribute.

    The arguments are the same as for the call function.  Example:

    check_call(["ls", "-l"])
    """
    retcode = __call(*popenargs, **kwargs)
    if retcode:
        cmd = kwargs.get("args")
        if cmd is None:
            cmd = popenargs[0]
        raise subprocess.CalledProcessError(retcode, cmd)
    return 0


def execute(*args):
    """Execute the commands while printing it."""
    for command in args:
        try:
            assert isinstance(command, str)
            print(COMMAND_PREFIX, command)
            __check_call(command, shell=True)
        except subprocess.CalledProcessError as err:
            print(err)
            sys.exit(err.returncode)
        except AssertionError:
            print(
                "Command '%s' should be a string but given is of type: %s" % (
                    command, type(command)
                )
            )
            sys.exit(COMMAND_INVOKED_CANNOT_EXECUTE)
        except KeyboardInterrupt:
            print(
                "killing the command: '%s' and exiting the execution." % (
                    command
                )
            )
            sys.exit(KEYBOARD_INTERRUPT)


def set_environmental_variables(**kwargs):
    """Set all the evnironmental variables."""
    for key, value in kwargs.items():
        assert isinstance(value, str)
        os.environ[key] = value
