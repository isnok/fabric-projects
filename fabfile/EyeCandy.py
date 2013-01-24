from fabric import colors
from fabric.api import env

def confirm_settings(settings, default=True, really=False):

    """ Show and confirm relevant variables. """

    from fabric.contrib.console import confirm
    from fabric.api import abort

    print
    print colors.green("About to run:"), env['command']
    print
    fmt = "    %-" + str(9+max([len(k) for k in settings.keys()])) + "s = %s"
    for key, value in sorted(settings.iteritems()):
        print fmt % (colors.magenta(key), colors.cyan(value))
    print
    if env['really'] or really:
        if not confirm("Proceed with these settings?", default=default):
            abort("Settings not confirmed.")
        else:
            print colors.green("\nSettings OK, starting:\n")
    else:
        print colors.green("\nNot doing it 'really', so here you go:\n")


def setenv(**kwargs):

    """ Task to set 'env' variables from the command line. """

    for (key, value) in kwargs.iteritems():
        if key in env:
            print "%s: env['%s'] = %s (was: %s)" %(colors.red("SetEnv"), colors.magenta(key), colors.cyan(value), colors.cyan(env[key]))
        else:
            print "%s: env['%s'] = %s" %(colors.green("SetEnv"), colors.magenta(key), colors.cyan(value))
        env[key] = value
