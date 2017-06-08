import functools
import subprocess

from ..app import build_app
from ..exceptions import CobExecutionError
from ..bootstrapping import ensure_project_bootstrapped


def appcontext_command(func):
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        ensure_project_bootstrapped()
        with build_app().app_context():
            return func(*args, **kwargs)

    return new_func


def exec_or_error(*args, **kwargs):
    returned = subprocess.Popen(*args, **kwargs)
    if returned.wait() != 0:
        raise CobExecutionError('Error executing command')
    return returned
