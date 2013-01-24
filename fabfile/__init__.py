''' The fabfile.

    One to install, one to maintain,
    one to configure, and one to reset.
    Or just one to deploy them all.
'''

project = __name__

# At first we load the config file.

from fabfile import ConfigHandling
config = ConfigHandling.load_config(project)

# Then we detect and import (if enabled) the project py files.

detected = []
enabled = []

import os
from fabfile import projects
subdirs = os.walk(os.curdir).next()[1]
for subdir in subdirs:
    if projects.is_project(subdir):
        detected.append(subdir)
        project_cfg = ConfigHandling.load_config(subdir)
        if projects.is_enabled(subdir):
            enabled.append(subdir)

from fabric.api import env

env['detected_projects'] = detected
env['enabled_projects'] = enabled

# import fabfile submodules
for module in config['enabled_submodules']:
    __import__("%s.%s" % (project, module))

# import enabled projects
for project in enabled:
    locals()[project] = __import__(project)


# Now we can create our hacked tasks from here.

import FabHacks
from fabric.api import task

for func in FabHacks.anons:
    locals()[func.__name__] = task(func)

for name, func in FabHacks.named.iteritems():
    sane_name = name.split('.')[-1]
    locals()[sane_name] = task(name=name)(func)
