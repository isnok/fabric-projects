'''  Execute scripts on remote hosts in different ways. '''

from os.path import basename

from fabfile.reality import whatsreal
from fabric.api import task

remote_tempdir = '/tmp'

@task
def user(filename):

    """ Upload and execute a script. """

    really = whatsreal()

    really.put(filename, remote_tempdir)
    remote_file = remote_tempdir + '/' + basename(filename)
    really.run('chmod +x %s' % remote_file)
    really.run('%s' % remote_file)
    really.run('rm %s' % remote_file)


@task
def sudo(filename):

    """ Upload a script and execute it with sudo. """

    really = whatsreal()

    really.put(filename, remote_tempdir)
    remote_file = remote_tempdir + '/' + basename(filename)
    really.run('chmod +x %s' % remote_file)
    really.sudo('%s' % remote_file)
    really.run('rm %s' % remote_file)

@task
def wrap(filename):

    """ Wrap a script with WrappedScriptFile and run it. """

    from fabfile.ShellWrappers import WrappedScriptFile
    script = WrappedScriptFile(filename)
    script.run()


@task
def psql(filename, user='postgres', database='postgres'):

    """ Upload a script and execute it in the psql shell. """

    really = whatsreal()

    really.put(filename, remote_tempdir)
    remote_file = basename(filename)
    really.run('psql -U %s -f /tmp/%s %s' % (user, remote_file, database))
    really.run('rm %s' % remote_file)
