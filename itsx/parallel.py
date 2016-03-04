#!/usr/bin/env python
from Bio import SeqIO
from threading import Thread
from glob import glob
from itsx import *
import os
import shutil
from itsxcmd import ITSx

__author__ = 'mike knowles'


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


class ITSx(object):

    def __init__(self, args, **kwargs):
        from Queue import Queue
        self.threads = args.cpus
        self.path = args.output
        del args.output
        self.itsxargs = kwargs
        self.smallqueue = Queue()
        self.itsxqueue = Queue()
        for _ in range(len(self.threads)):
            # Send the threads to the merge method. :args is empty as I'm using
            threads = Thread(target=self.parallel, args=())
            # Set the daemon to true - something to do with thread management
            threads.setDaemon(True)
            # Start the threading
            threads.start()
        self.smallqueue.join()

    def parallel(self):
        while True:
            filename, output = self.itsxqueue.get()
            ITSx(i=filename, o=output, **self.itsxargs)
            execute("-i {} -o {} -t {} --debug --cpu {} -N 2 --detailed_results T --preserve T".format(
                *self.itsxqueue.get()))
            self.itsxqueue.task_done()

    def run(self):
        import math
        while True:
            ss = self.smallqueue.get()
            cap = int(math.ceil(float(sample.assembly.TotalLength)/self.threads))
            cap += int(cap/2e4)
            baselist = []
            with open(fasta) as fastafile:
                record = SeqIO.parse(bestassemblyfile, "fasta")
                for i, batch in enumerate(BinPacker(record, cap)):
                    base = os.path.join(sample.general.ITSxresults, str(i+1))
                    output = os.path.join(base, "{0:s}_group_{1:d}".format(sample.name, i + 1))
                    make_path(base)
                    filename = output + ".fasta"
                    with open(filename, "w") as handle:
                        SeqIO.write(list(batch), handle, "fasta")
                    output = os.path.splitext(filename)[0]
                    self.itsxqueue.put((filename, output))
                    baselist.append(output)
            self.itsxqueue.join()
            finalfiles = glob()
            for output in finalfiles:
                # Low level file i/o operation to quickly append files without significant overhead
                if hasattr(os, 'O_BINARY'):
                    o_binary = getattr(os, 'O_BINARY')
                else:
                    o_binary = 0
                output_file = os.open(output, os.O_WRONLY | o_binary | os.O_CREAT)
                for intermediate in baselist:
                    input_filename = intermediate[finalfiles.index(output)]
                    input_file = os.open(input_filename, os.O_RDONLY | o_binary)
                    while True:
                        input_block = os.read(input_file, 1024 * 1024)
                        if not input_block:
                            break
                        os.write(output_file, input_block)
                    os.close(input_file)
                os.close(output_file)
            if all(map(os.path.isfile, finalfiles)):
                if os.stat(finalfiles[0]).st_size:
                    with open(finalfiles[0]) as pos:
                        self.parse(sample, pos)
                summarylines = self.summary(baselist)
                with open(os.path.join(sample.general.ITSxresults, sample.name + '.summary.txt'), 'w+') as full:
                    full.writelines(summarylines)
            else:
                print_function("ERROR: No output generated for " + sample.name, self.start)
            # for intermediate, folder in baselist:
                # shutil.rmtree(folder)
            self.smallqueue.task_done()

    @staticmethod
    def summary(baselist):
        '''
        Compile summary report is generated by adding up all the values in temp .summary.txt files
        :param baselist: list of folders and temporary files
        :return: compiled summary report
        '''
        import re
        summarylines = list()
        regex = re.compile('\d+$')
        for intermediate in baselist:
            with open(intermediate[-1]) as summary:
                if summarylines:
                    for idx, line in enumerate(summary):
                        match = regex.search(line)
                        if match:
                            summatch = regex.search(summarylines[idx])
                            start = match.start() if match.start() <= summatch.start() else summatch.start()
                            summarylines[idx] = '{0:s}{1:d}\n'.format(summarylines[idx][:start],
                                                                      int(match.group(0)) + int(summatch.group(0)))
                else:
                    summarylines = summary.readlines()
        return summarylines

def execute(command, outfile="", **kwargs):
    """
    Allows for dots to be printed to the terminal while waiting for a long system call to run
    :param command: the command to be executed
    :param outfile: optional string of an output file
    from https://stackoverflow.com/questions/4417546/constantly-print-subprocess-output-while-process-is-running
    """
    import sys
    import time
    # Initialise count
    count = 0
    # Initialise the starting time
    start = int(time.time())
    maxtime = 0
    # Removing Shell=True to prevent excess memory use thus shlex split if needed
    if type(command) is not list and "shell" not in kwargs:
        import shlex
        command = shlex.split(command)
    # Run the commands - direct stdout to PIPE and stderr to stdout
    # DO NOT USE subprocess.PIPE if not writing it!
    if outfile:
        process = Popen(command, stdout=PIPE, stderr=STDOUT, **kwargs)
    else:
        DEVNULL = open(os.devnull, 'wb')
        process = Popen(command, stdout=DEVNULL, stderr=STDOUT, **kwargs)
    # Write the initial time
    sys.stdout.write('[{:}] '.format(time.strftime('%H:%M:%S')))
    # Create the output file - if not provided, then nothing should happen
    writeout = open(outfile, "ab+") if outfile else ""
    # Poll process for new output until finished
    while True:
        # If an output file name is provided
        if outfile:
            # Get stdout into a variable
            nextline = process.stdout.readline()
            # Print stdout to the file
            writeout.write(nextline)
        # Break from the loop if the command is finished
        if process.poll() is not None:
            break
        # Adding sleep commands slowed down this method when there was lots of output. Difference between the start time
        # of the analysis and the current time. Action on each second passed
        currenttime = int(time.time())
        if currenttime - start > maxtime:
            # Set the max time for each iteration
            maxtime = currenttime - start
            # Print up to 80 dots on a line, with a one second delay between each dot
            if count <= 80:
                sys.stdout.write('.')
                count += 1
            # Once there are 80 dots on a line, start a new line with the the time
            else:
                sys.stdout.write('\n[{:}] .'.format(time.strftime('%H:%M:%S')))
                count = 1
    # Close the output file
    writeout.close() if outfile else ""
    sys.stdout.write('\n')

if __name__ == '__main__':
    pass
