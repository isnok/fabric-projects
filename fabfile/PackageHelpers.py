''' Convenience through object orientation '''


from fabfile.ShellWrappers import WrappedShellCode


class DebianPackages(WrappedShellCode):

    """ Some debian packages to be installed. """

    def __init__(self, name, desc, packages):
        install_cmd = "aptitude -q install %s" % (" ".join(packages))
        #install_cmd = "apt-get install %s" % (" ".join(packages))
        WrappedShellCode.__init__(self, name, desc, install_cmd, sudo=True)


class GitRepository(WrappedShellCode):

    """ A git repo to be cloned. """

    def __init__(self, name, desc, repo, dest, **kw):
        clone_cmd = 'git clone %s %s' % (dest, repo, dest)
        WrappedShellCode.__init__(self, name, desc, clone_cmd, **kw)


from fabfile.reality import whatsreal
from fabfile.CompositeTasks import CompositeTask
from fabric.api import settings
from fabric.api import prefix


class PipPackages(CompositeTask):

    """ Some python pip packages to be installed (via eggproxy). """

    eggproxies = None

    def __init__(self, name, desc, packages, prefix="true"):
        CompositeTask.__init__(self, name, desc=desc)
        self.packages = packages
        self.prefix = prefix

    def run(self):
        self.execStarting()
        print
        map(self.install, self.packages)

    def install(self, package):
        really = whatsreal()
        for eggproxy in self.eggproxies:
            with settings(prefix(self.prefix), warn_only=True):
                res = really.sudo('pip install --index=%s %s' % (eggproxy, package))
                if type(res) is not str and res.succeeded:
                    return
        with settings(prefix(self.prefix)):
            really.sudo('pip install %s' % package)


from os.path import basename, dirname

class DeployConfig(CompositeTask):

    """ A class to deploy config files. """

    def __init__(self, name, configfile, destination=None, desc='no description'):
        self.configfile = configfile
        if destination is None:
            destination = "/etc/" + basename(configfile)
        self.destination = destination
        CompositeTask.__init__(self, name, desc)

    def run(self):
        really = whatsreal()
        really.put(self.configfile)
        really.sudo('mkdir -p %s' % dirname(self.destination))
        really.sudo('mv -i %s %s' % (basename(self.configfile), self.destination))
