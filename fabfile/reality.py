''' reality is the main source of fabric-projects' default behaviour of not executing tasks without explicitly stating that action should 'really' be taken. '''

##
#  Config value handling (or how to overdo getting one bool from the config into the env dict.)
##

from fabfile.ConfigHandling import get_bool

really = get_bool('fabfile', 'really')

from fabfile.EyeCandy import setenv

if really:
    setenv(really=really) # colored output
else:
    from fabric.api import env
    env['really'] = really


##
#  The tasks to control 'reallynes'
##

from fabfile.FabHacks import maintask


@maintask
def really():

    """ Enable command execution. """

    setenv(really=True)

@maintask
def notreally():

    """ Disable command execution. (default) """

    setenv(really=False)


##
#  The machinery for tasks to use this stuff.
##


from collections import namedtuple
from fabric import api
from fabfile import FakeAPI


Reality = namedtuple("Reality", ["put","get","run","sudo"])

yesreally = Reality(api.put, api.get, api.run, api.sudo)
notreally = Reality(FakeAPI.put, FakeAPI.get, FakeAPI.run, FakeAPI.sudo)

def whatsreal():

    ''' Returns current Reality. To be 'asked for' by tasks at execution time. '''

    return [notreally, yesreally][env['really']]


