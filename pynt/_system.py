"""All system related functions."""

from __future__ import print_function

import glob
import os
import subprocess
import shutil
import sys

COMMAND_PREFIX = ">>>"
COMMAND_INVOKED_CANNOT_EXECUTE = 126


def __stdout_print(*args, **kwargs):
    print(*args, **kwargs)
    sys.stdout.flush()


def __stderr_print(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    sys.stderr.flush()


def execute(*args):
    """Execute the commands while __stdout_printing it."""
    for command in args:
        try:
            assert isinstance(command, str)
            __stdout_print(COMMAND_PREFIX, command)
            subprocess.check_call(command, shell=True)
        except subprocess.CalledProcessError as err:
            __stdout_print(err)
            sys.exit(err.returncode)
        except AssertionError:
            __stderr_print(
                "Command '%s' should be a string but given is of type: %s" % (
                    command, type(command)
                )
            )
            sys.exit(COMMAND_INVOKED_CANNOT_EXECUTE)


def set_environmental_variables(**kwargs):
    """Set all the evnironmental variables."""
    for key, value in kwargs.items():
        assert isinstance(value, str)
        __stdout_print(COMMAND_PREFIX, 'pynt-export %s=%s' % (key, value))
        os.environ[key] = value


def rm(*wild_card_strings, **kwargs):
    """Linux rm functionality.

    Parameters
    ----------
    ignore_if_doesnt_exist : bool, optional
        Don't raise any error when file or directory doesn't exist.
        (default is True)
    ignore_if_unable_to_delete : bool, optional
        Don't raise any error when unable to delete a file or directory.
        (default is False)

    Raises
    ------
    Exception
        Is raised when file doesn't exist and ignore_if_doesnt_exist is False.

    """
    ignore_if_doesnt_exist = kwargs.get("ignore_if_doesnt_exist", True)
    ignore_if_unable_to_delete = \
        kwargs.get("ignore_if_unable_to_delete", False)
    for wild_card_string in wild_card_strings:
        file_paths = glob.glob(wild_card_string)
        if not ignore_if_doesnt_exist:
            __stdout_print(">>> pynt-rm -r %s" % wild_card_string)
            if len(file_paths) is 0:
                raise IOError(
                    "'%s' No such file or directory exists" % wild_card_string
                )
        else:
            __stdout_print(">>> pynt-rm -rf %s" % wild_card_string)
        for file_path in file_paths:
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception:
                if not ignore_if_unable_to_delete:
                    raise
