from fabric.api import settings
from fabric import colors
from fabfile import reality


class WrappedShellCommand:

    def __init__(self, cmd, run_func="run", chdir="", warn_only=False, prefix=""):
        self.cmd = cmd
        self.run_func = run_func
        self.chdir = chdir
        self.warn_only = warn_only
        self.prefix = prefix

    def __str__(self):
        clsstr = colors.cyan("<%s:" % self.__class__.__name__)
        cmdstr = getattr(reality.notreally, self.run_func)(self.cmd, printit=False)
        endstr = colors.cyan(" ;>")
        return clsstr + cmdstr + endstr

    def settings(self):
        return settings(
                warn_only=self.warn_only,
                cwd=self.chdir,
                prefix=self.prefix
            )

    def execute(self, stack=None):
        really = reality.whatsreal()
        run = getattr(really, self.run_func)
        with self.settings():
            run(self.cmd)


from CompositeTasks import CompositeTask


class WrappedShellCode(CompositeTask):

    """ A linewise fab-wrapped shell script. """

    def __init__(self, name, desc, script, chdir="", warn_only=0, prefix=""):
        CompositeTask.__init__(self, name, desc=desc)
        self.chdir = chdir
        self.warn_only = bool(warn_only)
        self.prefix = prefix
        self.add_script(script)

    def add_file(self, filename, *args, **kw):
        self.add_script(open(filename).read(), *args, **kw)

    def add_script(self, cmd_str, *args, **kw):
        cmd_lst = cmd_str.replace("\n", ";").split(';')
        for cmd in cmd_lst:
            self.add_cmd(cmd.strip(), *args, **kw)

    def add_cmd(self, cmd, chdir=None, warn_only=None, prefix=None):
        if chdir is None:
            chdir = self.chdir
        if warn_only is None:
            warn_only = self.warn_only
        if prefix is None:
            prefix = self.prefix

        run_func = "run"
        if cmd[:5] == "sudo ":
            run_func = "sudo"
            cmd = cmd[5:]
        if cmd and not cmd[0] == "#":
            self.todo.append(WrappedShellCommand(cmd, run_func, chdir, warn_only, prefix))

    def run(self):
        self.execStarting()
        print
        for task in self.todo:
            task.execute()

from os.path import basename
from fabric.colors import green

class WrappedScriptFile(WrappedShellCode):

    """ A convenience class to wrap shell script files. """

    instances = {}

    def __new__(cls, filename, *args, **kw):
        if filename.startswith('./'):
            filename = filename[2:]
        if not filename in cls.instances:
            new = super(WrappedShellCode, cls).__new__(cls, filename, *args, **kw)
            cls.instances[filename] = new
        else:
            print "Double script:", filename
        return cls.instances[filename]

    def __init__(self, filename, *args, **kw):
        name = '%s' % basename(filename).replace(".sh", "")
        for lineno, line in enumerate(open(filename).readlines()):
            if lineno == 2:
                break
        desc = "%s (%s)" % (line[:-1], green(filename))
        script = open(filename).read()
        WrappedShellCode.__init__(self, name, desc, script, *args, **kw)
