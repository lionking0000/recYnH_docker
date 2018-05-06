import os
VERBOSE = False

def run_cmd( cmd ):
    if VERBOSE: print cmd
    os.system( cmd )

def run( args ):
    cmd = "Rscript ./visualization.R"
    run_cmd( cmd )