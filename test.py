#!/usr/bin/env python

import sys
import os
import time
import tempfile

from move import Move, MovePyProj

def main(inputfile):
    if not os.path.isfile(inputfile):
        sys.exit("{} is not a file".format(inputfile))
        
    output = tempfile.NamedTemporaryFile(delete=False)
    cls = Move(inputfile, output.name)

    start = time.time()
    for i in range(3):
        # cls.by_seconds(1)
        time.sleep(2)
    print ("Time elapsed: {}".format(time.time() - start))
    
    os.unlink(output.name)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Input file name not defined")
    main(sys.argv[1])
