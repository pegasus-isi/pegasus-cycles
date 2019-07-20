# -*- coding: utf-8 -*-

from pegasus_cycles._pegasus import *

a = ADAG("pegasus-cycles", auto=True)


@a.job()
def gldas_to_cycles(
    latitude,
    longitude,
    output_file,
    start_date="2000-01-01",
    end_date="2019-03-01",
    gldas_path="hard-coded",
):
    """Transform GLDAS to Cycles."""
    j = Job("gldas-to-cycles")
    j.addArguments("--start-date", start_date)
    j.addArguments("--end-date", end_date)
    j.addArguments("--latitude", latitude)
    j.addArguments("--longitude", longitude)
    j.addArguments("--gldas-path", gldas_path)
    j.addArguments("--output", output_file)
    return j


@a.transformation()
@a.resource_info(cpu=0.25)
def baseline_transformation():
    """Cycles Baseline Transformation."""
    e1 = Executable("cycles-baseline")
    e1.addPFN(PFN("file://path/run", "a"))
    e2 = Executable("io.sh")
    e2.addPFN(PFN("file://path/io.sh", "a"))
    return [e1, e2]


@a.job()
def baseline():
    """Cycles Baseline."""
    return Job("cycles-baseline")


@a.transformation()
@a.resource_info(cpu=0.25)
def cycles_transformation():
    """Cycles Transformation."""
    e1 = Executable("cycles")
    e1.addPFN(PFN("file://path/run", "a"))
    e2 = Executable("io.sh")
    e2.addPFN(PFN("file://path/io.sh", "a"))
    return [e1, e2]


@a.job()
def cycles():
    """Cycles."""
    return Job("cycles")


@a.job()
def cycles_plus_10pct_nitrogen():
    """Cycles Plus 10 Percent Nitrogen."""
    return Job("cycles")


@a.transformation()
@a.resource_info(cpu=0.25)
def merge_transformation():
    """Cycles Baseline Transformation."""
    e1 = Executable("merge")
    e1.addPFN(PFN("file://path/run", "a"))
    return e1


@a.job()
def merge():
    """Merge."""
    return Job("merge")


@a.transformation()
@a.resource_info(cpu=0.25)
def visualize_transformation():
    """Cycles Baseline Transformation."""
    e1 = Executable("visualize")
    e1.addPFN(PFN("file://path/run", "a"))
    return e1


@a.job()
def visualize():
    """Cycles Visualize."""
    return Job("visualize")
