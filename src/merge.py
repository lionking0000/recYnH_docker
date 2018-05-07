import os
VERBOSE = False

def run_cmd( cmd ):
    if VERBOSE: print cmd
    os.system( cmd )

def run( args ):
    print args.program # the experiments type ('Y2H'|'Y3H')
    print args.matrix1 # the interaction matrix of selection condition
    print args.matrix2 # the interaction matrix of non-selection condition
    print args.output # the output folder name

    if args.matrix2 == None:
        args.matrix2 = args.matrix1
    
    cmd = "Rscript ./visualization.R %s %s %s %s" % ( args.program, args.matrix1, args.matrix2, args.output )
    run_cmd( cmd )
