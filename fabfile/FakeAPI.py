''' Our fake fabric.api functions, that give nice colored output instead of running commands. 

    TODO:
     - be more correct about the arguments
     - be more correct about the execution
     - inclde (possibly) missing functions
'''

from fabric import colors
from fabric.api import env

def put(filename, destination=None):
    if destination is None:
        print " %s %s" % (colors.cyan(">"), filename)
    else:
        print " %s %s -> %s" % (colors.cyan(">"), filename, destination)

def get(filename, destination=None):
    if destination is None:
        print "%s %s" % (colors.cyan("<"), filename)
    else:
        print "%s %s -> %s" % (colors.cyan("<"), filename, destination)

def run(command, printit=True, *args):
    suffix = ['', ' || true'][bool(env['warn_only'])]
    cd = colors.cyan(env['cwd'])
    dollar = colors.green("$")
    res = "%s %s %s%s" % (cd, dollar, command, suffix)
    if printit:
        print res
    return res

def sudo(command, printit=True, *args):
    suffix = ['', ' || true'][bool(env['warn_only'])]
    cd = colors.cyan(env['cwd'])
    dollar = colors.yellow("# sudo")
    command = colors.yellow(command)
    res = "%s %s %s%s" % (cd, dollar, command, suffix)
    if printit:
        print res
    return res


# Old coloring (of WrappedShellCode object instance)

    #def __repr__(self):
        #color = None
        #res = []

        #if self.chdir:
            #res.append(self.chdir)

        #if self.run_func is 'run':
            #color = colors.cyan
            #res.append("$")
        #elif self.run_func is 'sudo':
            #color = colors.yellow
            #res.append("# sudo")
        #else:
            #color = colors.red
            #res.append("?")

        #if self.prefix:
            #res.append(self.prefix)

        #res.append(self.cmd)

        #if self.warn_only:
            #res.append(colors.white("|| true"))

        #return color(" ".join(res))


