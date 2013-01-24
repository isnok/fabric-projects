from fabfile.FabHacks import maintask
from fabfile import ConfigHandling
from fabric.api import hosts
from fabric.api import env
from fabric import colors
import os


def is_project(subdir):
    if  subdir == 'fabfile':
        return True
    return set(["__init__.py", "project.cfg"]).issubset(os.listdir(subdir))


def is_enabled(project):
    if project == 'fabfile':
        return False
    return ConfigHandling.get_bool(project, 'project_enabled')


@maintask
@hosts('localhost')
def show():

    """ List projects and some of their config properties. """

    print
    print "Detected projects:"
    for subdir in env['detected_projects']:
        if subdir in env['enabled_projects']:
            abled_state = colors.green("enabled")
            hint = "to %s run: disable:%s" % (colors.white('disable'), subdir)
        else:
            abled_state = colors.yellow("disabled")
            hint = "to %s run: enable:%s" % (colors.white('enable'), subdir)

        print
        print "  %s (%s)" % (colors.cyan(subdir), abled_state)
        print "    `- %s" % hint


@maintask
@hosts('localhost')
def enable(project=None):

    """ Enable a project. """

    if project is None:
        show()
        return
    print
    config = ConfigHandling.get_config(project)
    if ConfigHandling.get_bool(project, 'project_enabled') == True:
        print "Already enabled: %s" % colors.cyan(project)
        show()
        return
    print "Enabling: %s" % colors.cyan(project)
    config['project_enabled'] = True
    config.write()


@maintask
@hosts('localhost')
def disable(project=None):

    """ Disable a project. """

    if project is None:
        show()
        return
    print
    config = ConfigHandling.get_config(project)
    if ConfigHandling.get_bool(project, 'project_enabled') == False:
        print "Already disabled: %s" % colors.cyan(project)
        show()
        return
    print "Disabling: %s" % colors.cyan(project)
    config['project_enabled'] = False
    config.write()
