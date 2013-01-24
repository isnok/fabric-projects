''' Magic Script Importer '''

def is_sql_script(filename):
    return filename.endswith('.sql')

def sql_varname(filename):
    return filename.replace('.sql', '')

def is_shell_script(filename):
    return filename.endswith('.sh')

def shell_varname(filename):
    return filename.replace('.sh', '')


import os
from functools import partial
from fabric.api import task
from fabric.colors import green

def loadScripts(project, subdir):
    result = {}
    for kind in ('psql', 'user',):
        result.update(loadScriptsOfKind(kind, project, subdir))
    return result

def loadScriptsOfKind(kind, project, subdir):

    # upload scripts

    from fabfile.scripts import psql
    from fabfile.scripts import user

    if kind == 'psql':
        isscript = is_sql_script
        varname = sql_varname
        execfun = psql
    elif kind == 'user':
        isscript = is_shell_script
        varname = shell_varname
        execfun = user

    scriptpath = os.path.sep.join((os.curdir, project, subdir))
    scripts = filter(isscript, os.listdir(scriptpath))
    result = {}
    for script in scripts:
        scriptfile = scriptpath + os.path.sep + script
        func = partial(execfun, scriptfile)
        func.__doc__ = "%s(%s)" % (execfun.__doc__, green(os.path.sep.join((scriptpath,script))))
        result[varname(script)] = task(name=varname(script))(func)

    del user
    del psql

    return result


