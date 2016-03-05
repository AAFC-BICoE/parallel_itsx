#!/usr/bin/env python
import os
import errno
__author__ = 'mike knowles'
__all__ = ['make_path', 'itsxcmd', 'Bin', 'BinPacker', "parallel"]


class Bin:
    """Bin for holding sequences"""

    def __init__(self, capacity, contents=None):
        self.capacity = capacity
        self.contents = contents if contents else list()
        self.sum = sum(map(len, list()))

    def add(self, x):
        self.contents.append(x)
        self.sum += len(x)

    def __iter__(self):
        for i in self.contents:
            yield i

    def free_capacity(self):
        return self.capacity - self.sum

    def __delattr__(self, item):
        del self


class BinPacker:
    """ Uses first fit algorithm to solve the bin-packing problem
    """
    def __init__(self, record, cap):
        # Extra is ideal for small contigs
        self.bins = [Bin(cap)]
        for seq_record in record:
            # Add the item to the first bin that can hold it
            # If no bin can hold it, make a new bin
            item = len(seq_record)
            for xBin in self.bins:
                if item > cap:
                    if xBin.sum == 0:
                        xBin.add(seq_record)
                        xBin.capacity = item
                        break
                    # Sometimes, large contigs are bigger than cap
                if xBin.free_capacity() >= item:
                    xBin.add(seq_record)
                    break
                if self.bins.index(xBin) == len(self.bins) - 1:
                    self.bins.append(Bin(cap))

    def __iter__(self):
        for xBin in self.bins:
            yield xBin

    def __delattr__(self, item):
        for xBin in self.bins:
            del xBin

def make_path(inpath):
    """
    from: http://stackoverflow.com/questions/273192/check-if-a-directory-exists-and-create-it-if-necessary \
    does what is indicated by the URL
    :param inpath: string of the supplied path
    """
    try:
        # os.makedirs makes parental folders as required
        os.makedirs(inpath)
    # Except os errors
    except OSError as exception:
        # If the os error is anything but directory exists, then raise
        if exception.errno != errno.EEXIST:
            raise

if __name__ == '__main__':
    pass