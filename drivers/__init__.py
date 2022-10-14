
def new():
    import os
    import importlib

    __all__ = []

    #auto-load all drivers
    for name in os.listdir('drivers'):
        if name.endswith('.py') and not name.startswith('__'):
            if name[:-3] not in __all__:
                module_name = 'drivers.' + name[:-3]
                #module = importlib.__import__(module_name)
                module = importlib.import_module(module_name)
                __all__.append(name[:-3])




def old():
    from os.path import dirname, basename, isfile
    from os import listdir
    import glob
    modules = glob.glob(dirname(__file__)+"/*.py")
    __all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]

    modules = listdir(dirname(__file__))
    for module in modules:
        if module == '__init__.py' or module[-3:] != '.py':
            continue
        __import__(module[:-3], locals(), globals())

    del module

new()
