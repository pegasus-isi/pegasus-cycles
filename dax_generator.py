#!/usr/bin/env python3

import os
import pegasus_cycles
from pegasus_cycles.__main__ import *
from string import Template


def _generate_tc():
    print("TC")
    with open("tc.template") as t_tc_file:
        src = Template(t_tc_file.read())
        tc_data = {
            "work_dir": os.getcwd()
        }
        result = src.substitute(tc_data)
        with open("tc", "w") as f:
            f.write(result)


if __name__ == '__main__':
    logging.info("Create transformation catalog")
    _generate_tc()

    dax()
