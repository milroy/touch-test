#!/usr/bin/env python


import datetime
import os
import random
import string
import sys


def total_seconds (td):
    return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6


def main ():
    files = []
    start = datetime.datetime.now()
    print start, "Generating filenames in memory"
    for i in xrange(int(sys.argv[1])):
        files.append(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(40)))
    end = datetime.datetime.now()
    print end, "Generated {0} filenames".format(len(files))

    start = datetime.datetime.now()
    print start, "Ensuring directories"
    prefixes = set(filename[:2] for filename in files)
    for prefix in prefixes:
        try:
            os.mkdir(prefix)
        except OSError as ex:
            if ex.errno == 17:
                pass
            else:
                raise
    end = datetime.datetime.now()
    print end, "Ensured {0} directories".format(len(prefixes))

    start = datetime.datetime.now()
    print start, "Touching files"
    for filename in files:
        prefix, suffix = filename[:2], filename[2:]
        open(os.path.join(prefix, suffix), 'a').close()
    end = datetime.datetime.now()
    print end, "Touched {0} files ({1}/sec)".format(len(files), 1.0 * len(files) / total_seconds(end - start))


if __name__ == '__main__':
    main()
