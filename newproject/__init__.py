''' Welcome to newproject's fab module. '''

import os

project = __name__


# At first we load the config file.

from fabfile import ConfigHandling
config = ConfigHandling.load_config(project)

# Then we define stuff that our submodules might use.

from fabric.colors import green, cyan, white, yellow, red

from fabfile.EyeCandy import confirm_settings
from fabric.api import task
from fabric.api import local

from fabric.api import hide

def getScript(name):
    for module in (): # local scripts, soon to come
        try:
            return getattr(module, name)
        except:
            pass
    raise KeyError('Could not find a script named %r.' % name)


# Then we look at our submodules.

mod_path = os.path.sep.join((os.curdir, project))

def is_submodule(filename):
    if filename.endswith('.py'):
        return True
    try:
        return '__init__.py' in os.listdir("%s%s%s" % (mod_path, os.path.sep, filename))
    except:
        return False

def get_submodules(path):
    modules = filter(is_submodule, os.listdir(path))
    modules.remove('__init__.py')
    return modules

detected = []
for modulefile in get_submodules(mod_path):
    mod_name = modulefile.replace('.py', '')
    detected.append(mod_name)
    if not mod_name in config['disabled_submodules']:
        module = "%s.%s" % (project, mod_name)
        try:
            __import__(module)
            print green("Imported %s" % module)
        except Exception, ex:
            print red("Caught an Exception importing %r:" % module)
            print ex.message


# Finally we define our tasks

@task
def show():

    """ List all available submodules of this project. """

    print
    print "Detected submodules of %s:" % cyan(project)
    for subdir in detected:
        if subdir in config['disabled_submodules']:
            abled_state = yellow("disabled")
            hint = "to %s run: %s.enable:%s" % (white('enable'), white(project), subdir)
        else:
            abled_state = green("enabled")
            hint = "to %s run: %s.disable:%s" % (white('disable'), white(project), subdir)

        print
        print "  %s (%s)" % (cyan(subdir), abled_state)
        print "    `- %s" % hint


@task
def disable(submodule=None):

    """ Disable a submodule of this project or the project itself. """

    with hide('running'):
        local('./clean.sh')

    if submodule is None:
        print "\n%s %s" % (green('Disabling project:'), cyan(project))
        config['project_enabled'] = False
        config.write()
    else:
        if submodule in config['enabled_submodules']:
            print "\n%s %s.%s" % (green('Disabling module:'), cyan(project), submodule)
            config['enabled_submodules'].remove(submodule)
            config.write()
        else:
            print "\n%s %s.%s" % (green('Already disabled:'), cyan(project), submodule)

@task
def enable(submodule):

    """ Enable one of newproject's disabled submodules. """

    print "\n%s %s.%s" % (green('Enabling module:'), cyan(project), submodule)
    if not submodule in config['enabled_submodules']:
        config['enabled_submodules'].append(submodule)
        config.write()
    else:
        print "\n%s %s.%s" % (green('Already enabled:'), cyan(project), submodule)


@task
def clone(name=None):

    """ Create a new project by cloning this one. """

    if name is None:
        name = "No_Name"
        default = False
    else:
        default = True

    confirm_settings({"clone to": name}, default=default, really=True)

    print green("\nCloning %s to %s." % (project, name))
    with hide('running'):
        local('cp -riv %s %s' % (project, name))
    local('sed -i 1s/%s/%s/ %s/__init__.py' % (project, name, name))

@task
def update(name):

    """ Update a project's __init__.py (and other needed stuff). (experimental) """

    print green('\nUpdating %s from %s.' % (name, project))
    with hide('running'):
        local('./clean.sh')
        local('cp -v %s/__init__.py %s/__init__.py' % (project, name))
        local('sed -i 1s/%s/%s/ %s/__init__.py' % (project, name, name))
        local('cp -i %s/project.cfg %s' % (project, name))
