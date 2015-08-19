#!/usr/bin/env python


import datetime
import logging
import os
import random
import string
import sys


def total_seconds (td):
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6


def main ():
    logging.basicConfig()

    logging.debug("Generating filenames in memory")
    filenames = list(generate_filenames(sys.argv[1]))
    logging.debug("Generated {0} filenames".format(len(filenames)))

    logging.debug("Ensuring directories")
    directories = ensure_directories(filenames)
    logging.debug("Ensured {0} directories".format(len(directories)))

    logging.debug("Touching files")
    seconds = count_seconds(lambda: touch_files(filenames))
    rate = 1.0 * len(filenames) / seconds
    logging.debug("Touched {0} files ({1}/sec)".format(len(filenames), rate))
    print rate


def count_seconds (func):
    start = datetime.datetime.now()
    func()
    end = datetime.datetime.now()
    return total_seconds(end - start)


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
    main()
