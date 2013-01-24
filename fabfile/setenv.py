from fabric.api import hosts
from fabfile import EyeCandy
from fabfile.FabHacks import maintask

setenv = maintask(hosts('localhost')(EyeCandy.setenv))

