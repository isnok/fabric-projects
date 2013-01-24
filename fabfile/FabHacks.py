''' Hacks. Some major, some minor. '''

from inspect import isfunction

anons = []
named = {}

last_name = None


def maintask(*args):

    global last_name
    func_or_name = args[0]

    if isfunction(func_or_name):
        anons.append(func_or_name)
        return func_or_name

    def wrap_named(func):
        global last_name
        named[last_name] = func
        last_name = None
        return func

    if type(func_or_name) is str:
        last_name = func_or_name
        return wrap_named


# private hack:

from fabric.api import env

if env['user'] == 'km':
    env['user'] = 'kmartini'
