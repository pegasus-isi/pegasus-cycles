# -*- coding: utf-8 -*-

from functools import wraps

from Pegasus.DAX3 import ADAG as Base
from Pegasus.DAX3 import *


class ADAG(Base):
    def job(self):
        def wrap(f):
            @wraps(f)
            def wrapped_f(*args, **kwargs):
                rv = f(*args, **kwargs)
                if rv:
                    self.addJob(rv)
                return rv

            return wrapped_f

        return wrap

    def resource_info(self, cpu=1, core=1, memory=1):
        def wrap(f):
            @wraps(f)
            def wrapped_f(*args, **kwargs):
                rv = f(*args, **kwargs)
                if rv:
                    if cpu != 1:
                        rv.profile(Namespace.PEGASUS, "cpu", cpu)
                    if core != 1:
                        rv.profile(Namespace.PEGASUS, "core", core)
                    if memory != 1:
                        rv.profile(Namespace.PEGASUS, "memory", memory)

                return rv

            return wrapped_f

        return wrap
