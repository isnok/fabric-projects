''' Handling of new_style project config files. '''

from os import path
from configobj import ConfigObj
from fabric.api import env

main_cfg_key = 'projects_config'
main_cfg_file = 'projects.cfg'
project_cfgs_subkey = 'projects'
project_cfg_name = 'project.cfg'
env[project_cfgs_subkey] = {}

def load_config(project):

    """ Load config of project into env. """

    if project == 'fabfile':
        config = ConfigObj(main_cfg_file)
        env[main_cfg_key] = config
        sanitize = get_bool(project, 'sanitize_configs', False)
        get_bool(project, 'sanitize_configs', sanitize, True)
        config['eggproxies'] = get_list(config, 'eggproxies', None)
        return config

    config = ConfigObj('%s%s%s' % (project, path.sep, project_cfg_name))
    env[project_cfgs_subkey][project] = config
    return config

def get_config(project):
    if project == 'fabfile':
        return env[main_cfg_key]
    else:
        return env[project_cfgs_subkey][project]

def get_bool(project, key, sanitize=None, sane=None):

    """ Currently only works on top-level keys. """

    if sanitize is None:
        sanitize = env[main_cfg_key]['sanitize_configs']
    if sane is None:
        sane = False

    cfg = get_config(project)
    cfg_value = cfg.get(key)

    if type(cfg_value) is bool and not sanitize:
        return cfg_value

    if type(cfg_value) is bool:
        result = cfg_value
    else:
        if not sane:
            unsane = ('true', 'yes', 'ja', 'y')
        else:
            unsane = ('false', 'no', 'nein', 'n')
        if cfg_value and cfg_value.lower() in unsane:
            result = bool(not sane)
        else:
            result = bool(sane)
    if sanitize:
        if not str(result) == str(cfg_value):
            cfg[key] = bool(result)
            print "Sanitizing %r because of %r was %r. Correcting to %r." % (cfg.filename, key, cfg_value, sane)
            cfg.write()
    return bool(result)


def get_list(config, key, default):

    """ Get a list of values from projects config. """

    try:
        value = config[key]
        if not value:
            value = []
        elif type(value) is not list:
            value = [value]
    except:
        value = []

    return value

