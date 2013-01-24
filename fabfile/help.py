""" When asked for help we answer "RTFM!" """

from fabfile.FabHacks import maintask

@maintask  # @task(default=True)
def help():

    ''' Show ReadMe document. '''

    from fabric.api import local

    local('$PAGER README.md')

