# Parallel ITSx


[Installation]: setup.py
[Git]: https://github.com/MikeKnowles/parallel_itsx
[parallel.py]: itsx/parallel.py
[threading]: https://docs.python.org/2/library/threading.html
[queue]: https://docs.python.org/2/library/queue.html
[SeqIO]: http://biopython.org/wiki/SeqIO
[bin packing]: https://en.wikipedia.org/wiki/Bin_packing_problem
[ITSx]: http://microbiology.se/software/itsx/

This is a wrapper for [ITSx] to add a more effective parallel implementation of ITSx.

Therefore, this Python (=<2.7.6) package requires ITSx in the `$PATH` to function.
In addition, all the same requirements for ITSx still apply.

### Installation

After cloning the git:

```commandline
git clone  https://github.com/MikeKnowles/parallel_itsx
```

Install the python package:

```commandline
cd parallel_itsx
python setup.py install
```

parallel_its will now be in your `$PATH`

### Execution

The script takes exactly the same parameters at ITSx as passes them directly

The only differences are mostly in [parallel.py] which uses the python [threading] and [queue] python 2.7.6 modules:

* To split the input fasta using Biopython's [SeqIO] into relatively equal parts using a first-fit algorithm to solve the [bin packing] problem
* The split fasta files are then processed individually by the [ITSx] module in seperate folders
* The result [ITSx] files are concatinated into the main directory specified on execution
    * The `summary.txt` file is updated from each folder by [parallel.py] so it appears to be the output from regualar [ITSx]

#### Caveats

The nature of these scripts rely on the user specifying a folder, if the folder does not exist it will be created on execution


#### Full list of options

```
usage: parallel_itsx [-h] -i {file} -o {file} [-p {directory}]
                     [--date {T or F}] [--reset {T or F}]
                     [-t {character code}] [-E {value}] [-S {value}]
                     [-N {value}]
                     [--selection_priority {sum, domains, eval, score}]
                     [--search_eval {value}] [--search_score {value}]
                     [--allow_single_domain {e-value,score or F}]
                     [--allow_reorder {T or F}] [--complement {T or F}]
                     [--cpu {value}] [--multi_thread {T or F}]
                     [--heuristics {T or F}] [--summary {T or F}]
                     [--graphical {T or F}] [--fasta {T or F}]
                     [--preserve {T or F}]
                     [--save_regions {SSU,ITS1,5.8S,ITS2,LSU,all,none}]
                     [--anchor {integer or HMM}] [--only_full {T or F}]
                     [--partial {integer}] [--concat {T or F}]
                     [--minlen {integer}] [--positions {T or F}]
                     [--table {T or F}] [--not_found {T or F}]
                     [--detailed_results {T or F}] [--truncate {T or F}]
                     [--silent {T or F}] [--graph_scale {value}]
                     [--save_raw {T or F}]

ITSx -- Identifies ITS sequences and extracts the ITS region by Johan
Bengtsson-Palme et al., University of Gothenburg Version: 1.0.11
-----------------------------------------------------------------

optional arguments:
  -h, --help            show this help message and exit
  -i {file}             DNA FASTA input file to investigate
  -o {file}             Base for the names of output file(s)

ITSx commands:
  Commands actually passed to ITSx

  -p {directory}        A path to a directory of HMM-profile collections
                        representing ITS conserved regions, default is in the
                        same directory as ITSx itself
  --date {T or F}       Adds a date and time stamp to the output directory,
                        off (F) by default
  --reset {T or F}      Re-creates the HMM-database before ITSx is run, off
                        (F) by default
  -t {character code}   Profile set to use for the search, see the User's
                        Guide (comma-separated) default is all
  -E {value}            Domain E-value cutoff for a sequence to be included in
                        the output, default = 1e-5
  -S {value}            Domain score cutoff for a sequence to be included in
                        the output, default = 0
  -N {value}            The minimal number of domains that must match a
                        sequence before it is included, default = 2
  --selection_priority {sum, domains, eval, score}
                        Selects what will be of highest priority when
                        determining the origin of the sequence, default is sum
  --search_eval {value}
                        The E-value cutoff used in the HMMER search, high
                        numbers may slow down the process, cannot be used with
                        the --search_score option, default is 0.01
  --search_score {value}
                        The score cutoff used in the HMMER search, low numbers
                        may slow down the process, cannot be used with the
                        --search_eval option, default is to used E-value
                        cutoff, not score
  --allow_single_domain {e-value,score or F}
                        Allow inclusion of sequences that only find a single
                        domain, given that they meet the given E-value and
                        score thresholds, on with parameters 1e-9,0 by default
  --allow_reorder {T or F}
                        Allows profiles to be in the wrong order on extracted
                        sequences, off (F) by default
  --complement {T or F}
                        Checks both DNA strands against the database, creating
                        reverse complements, on (T) by default
  --cpu {value}         the number of CPU threads to use, default is 1
  --multi_thread {T or F}
                        Multi-thread the HMMER-search, on (T) if number of
                        CPUs (--cpu option > 1) else off (F) by default
  --heuristics {T or F}
                        Selects whether to use HMMERs heuristic filtering, off
                        (F) by default
  --summary {T or F}    Summary of results output, on (T) by default
  --graphical {T or F}  'Graphical' output, on (T) by default
  --fasta {T or F}      FASTA-format output of extracted ITS sequences, on (T)
                        by default
  --preserve {T or F}   Preserve sequence headers in input file instead of
                        printing out ITSx headers, off (F) by default
  --save_regions {SSU,ITS1,5.8S,ITS2,LSU,all,none}
                        A comma separated list of regions to output separate
                        FASTA files for, 'ITS1,ITS2' by default
  --anchor {integer or HMM}
                        Saves an additional number of bases before and after
                        each extracted region. If set to 'HMM' all bases
                        matching the corresponding HMM will be output, default
                        = 0
  --only_full {T or F}  If true, output is limited to full-length regions, off
                        (F) by default
  --partial {integer}   Saves additional FASTA-files for full and partial ITS
                        sequences longer than the specified cutoff, default =
                        0 (off)
  --concat {T or F}     Saves a FASTA-file with concatenated ITS sequences
                        (with 5.8S removed) off (F) by default
  --minlen {integer}    Minimum length the ITS regions must be to be outputted
                        in the concatenated file (see above) default = 0
  --positions {T or F}  Table format output containing the positions ITS
                        sequences were found in, on (T) by default
  --table {T or F}      Table format output of sequences containing probable
                        ITS sequences, off (F) by default
  --not_found {T or F}  Saves a list of non-found entries, on (T) by default
  --detailed_results {T or F}
                        Saves a tab-separated list of all results, off (F) by
                        default
  --truncate {T or F}   Truncates the FASTA output to only contain the actual
                        ITS sequences found, on (T) by default
  --silent {T or F}     Supresses printing progress info to stderr, off (F) by
                        default
  --graph_scale {value}
                        Sets the scale of the graph output, if value is zero,
                        a percentage view is shown, default = 0
  --save_raw {T or F}   Saves all raw data for searches etc. instead of
                        removing it on finish, off (F) by default
```