#!/usr/bin/env python


import argparse
import datetime
import logging
import os
import random
import string
import sys
import timeit
from multiprocessing import Pool


def parser ():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', dest="files", type=int, help="number of files to touch per process")
    parser.add_argument('-p', dest="processes", type=int, help="number of processes")
    parser.add_argument('-d', '--debug', action='store_true', help="turn on debug logging")
    parser.set_defaults(debug=False)
    return parser


def do_test (numfiles):
    logger.debug("Generating filenames in memory")
    filenames = list(generate_filenames(numfiles))
    logger.debug("Generated {0} filenames".format(len(filenames)))

    logger.debug("Ensuring directories")
    directories = ensure_directories(filenames)
    logger.debug("Ensured {0} directories".format(len(directories)))

    logger.debug("Touching files")
    seconds = count_seconds(lambda: touch_files(filenames))

    return seconds


def count_seconds (func):
    start = timeit.default_timer()
    func()
    end = timeit.default_timer()
    return (end - start)


def touch_files (filenames):
    for filename in filenames:
        prefix, suffix = filename[:2], filename[2:]
        touch_file(os.path.join(prefix, suffix))


def touch_file (filename):
    open(filename, 'a').close()


def generate_filenames (num):
    for _ in xrange(int(num)):
        yield generate_filename()


def generate_filename ():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(40))


def ensure_directories (filenames):
    prefixes = set(filename[:2] for filename in filenames)
    for prefix in prefixes:
        try:
            os.mkdir(prefix)
        except OSError as ex:
            if ex.errno == 17:
                pass
            else:
                raise
    return prefixes


if __name__ == '__main__':

# In case this should be logged to file
    logging.basicConfig(format="%(asctime)s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    logger = logging.getLogger()    

    args = parser().parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    filesperproc = args.files
    numprocs = args.processes

    p = Pool(numprocs)
    
    pstart = timeit.default_timer()
    times = p.map(do_test, [filesperproc for i in range(numprocs)])
    runtime = timeit.default_timer() - pstart

    cpu_seconds = sum(times)
    total_files = numprocs*filesperproc

    total_rate = total_files / runtime

    print "Seconds per process: {}".format(times)
    print "Total time to write {0} files: {1} CPU wallclock seconds".format(total_files, cpu_seconds)
    print "Actual time: {0} seconds, rate: {1} files/second".format(runtime, total_rate)
    