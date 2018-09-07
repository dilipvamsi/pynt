"""All system related functions."""

import os
import subprocess
import sys

COMMAND_PREFIX = ">>>"
COMMAND_INVOKED_CANNOT_EXECUTE = 126


def execute(*args):
    """Execute the commands while printing it."""
    for command in args:
        try:
            assert isinstance(command, str)
            print(COMMAND_PREFIX, command)
            subprocess.check_call(command, shell=True)
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


def set_environmental_variables(**kwargs):
    """Set all the evnironmental variables."""
    for key, value in kwargs.items():
        assert isinstance(value, str)
        os.environ[key] = value
