from newproject import getScript

from fabric.api import task

@task
def test():
    print "Juppa!", getScript
