from fabric.tasks import Task
from fabric.colors import green, cyan


class CompositeTask(Task):

    """ A task composed of other tasks. """

    def __init__(self, name, desc='', tasks=None):
        self.name = name
        Task.__init__(self)
        self.todo = []
        if tasks is not None:
            for t in tasks:
                self.add_task(t)
        if desc:
            desc += " "
        self.__doc__ = desc
        if self.todo:
            self.__doc__ += "(%s)" % ", ".join([self.get_name(t) for t in self.todo])

    def get_name(self, task):
        if hasattr(task, 'name'):
            return cyan(task.name)
        else:
            return cyan('???')

    def add_task(self, task):
        self.todo.append(task)

    def __str__(self):
        return cyan("<%s: %s>" % (self.__class__.__name__, self.name))

    def execStarting(self):
        print "\n%s %s %s" % (self, green("starting up:"), self.__doc__)

    def printExecute(self, nextExecuted):
        print "\n%s %s %s" % (self, green("->"), nextExecuted)

    def run(self):
        #self.execStarting()
        for task in self.todo:
            self.printExecute(task)
            task.run()
