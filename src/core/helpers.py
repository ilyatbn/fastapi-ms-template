import inspect
import threading
from typing import Any


lock = threading.Lock()
class Singleton(type):
    _instances: Any = {}
    _init: Any = {}

    def __init__(cls, name, bases, dct):
        cls._init[cls] = dct.get('__init__', None)

    def __call__(cls, *args, **kwargs):
        init = cls._init[cls]
        if init is not None:
            args_list = list(args)
            for idx, arg in enumerate(args_list):
                args_list[idx] = str(arg)
            tmp_kwargs = {}
            for arg_key, arg_value in kwargs.items():
                tmp_kwargs[arg_key] = str(arg_value)
            key = (cls, frozenset(inspect.getcallargs(init, None, *args_list, **tmp_kwargs).items()))
        else:
            key = cls
        if key not in cls._instances:
            with lock:
                cls._instances[key] = super().__call__(*args, **kwargs)
        return cls._instances[key]

