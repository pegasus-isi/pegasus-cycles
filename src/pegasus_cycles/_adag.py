# -*- coding: utf-8 -*-

from pegasus_cycles._pegasus import *

a = ADAG("pegasus-cycles", auto=True)


@a.job()
@a.resource_info(cpu=2)
def gldas_to_cycles(lat, lon):
    """Transform GLDAS to Cycles."""
    return Job("gldas-to-cycles")


@a.job()
def baseline():
    """Cycles Baseline."""
    return Job("cycles-baseline")


@a.job()
def cycles():
    """Cycles."""
    return Job("cycles")


@a.job()
def cycles_plus_10pct_nitrogen():
    """Cycles Plus 10 Percent Nitrogen."""
    return Job("cycles")


@a.job()
def merge():
    """Merge."""
    return Job("merge")


@a.job()
def visualize():
    """Cycles Baseline."""
    return Job("visualize")
