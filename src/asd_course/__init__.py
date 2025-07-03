from .base_module import BaseTask

def __load_lab_modules():
    import importlib
    import os
    import sys
    import inspect

    cur_loc = __path__[0]

    for name in os.listdir(cur_loc):
        if name != "base_module" and os.path.isdir(f"{cur_loc}/{name}"):
            mod = importlib.import_module(f".{name}", "asd_course")
            for name, obj in inspect.getmembers(mod):
                if isinstance(obj, (BaseTask)):
                    sys.modules[__name__].__setattr__(name, obj)


__load_lab_modules()
