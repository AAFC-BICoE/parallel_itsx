#!/usr/bin/env python
from Bio.Application import AbstractCommandline, _Switch, _Argument, _Option

__author__ = 'mike knowles'


class _BooleanOption(_Option):
    pass


class ITSx(AbstractCommandline):
    """Base ITSx wrapper"""

    def __init__(self, cmd="ITSx", **kwargs):
        assert cmd is not None
        self.parameters = [
            _Switch(["-h", "h"],
                    "Print USAGE and DESCRIPTION;  ignore other arguments."),
            _Switch(["--help", "help"],
                    "Print USAGE, DESCRIPTION and ARGUMENTS description; "
                    "ignore other arguments."),
            _Switch(["--bugs", "bugs"],
                    "displays the bug fixes and known bugs in this version of ITSx"),
            _Option(["-i", "i"],
                    "DNA FASTA input file to investigate",
                    filename=True,
                    equate=False),
            _Option(["-o", "o"],
                    "Base for the names of output file(s)",
                    filename=True,
                    equate=False),
            _Option(["-p", "p"],
                    "A path to a directory of HMM-profile collections representing ITS conserved regions, default is "
                    "in the same directory as ITSx itself",
                    filename=True,
                    equate=False),
            _BooleanOption(["--date", "date"],
                           "Adds a date and time stamp to the output directory, off (F) by default"),
            _BooleanOption(["--reset", "reset"],
                           "Re-creates the HMM-database before ITSx is run, off (F) by default"),
        ]

        extra_parameters = [
            # Sequence Selection Options
            _BooleanOption(["--allow_reorder", "allow_reorder"],
                           "Allows profiles to be in the wrong order on extracted sequences, off (F) by default"),
            _BooleanOption(["--complement", "complement"],
                           "Checks both DNA strands against the database, creating reverse complements, "
                           "on (T) by default"),
            _BooleanOption(["--multi_thread", "multi_thread"],
                           "Multi-thread the HMMER-search, on (T) if number of CPUs (--cpu option > 1), else off (F) "
                           "by default"),
            _BooleanOption(["--heuristics", "heuristics"],
                           "Selects whether to use HMMER's heuristic filtering, off (F) by default"),
            _Option(["-t", "t"],
                    "Profile set to use for the search, see the User's Guide (comma-separated), default is all",
                    equate=False),
            _Option(["--allow_single_domain", "allow_single_domain"],
                    "Allow inclusion of sequences that only find a single domain, given that they meet the given "
                    "E-value and score thresholds, on with parameters 1e-9,0 by default",
                    equate=False),
            _Option(["--selection_priority", "selection_priority"],
                    "Selects what will be of highest priority when determining the origin of the sequence, "
                    "default is sum"),
            _Option(["-E", "E"],
                    "Domain E-value cutoff for a sequence to be included in the output, default = 1e-5",
                    equate=False),
            _Option(["-S", "S"],
                    "Domain score cutoff for a sequence to be included in the output, default = 0",
                    equate=False),
            _Option(["-N", "N"],
                    "The minimal number of domains that must match a sequence before it is included, default = 2",
                    equate=False),
            _Option(["--search_eval", "search_eval"],
                    "The E-value cutoff used in the HMMER search, high numbers may slow down the process, "
                    "cannot be used with the --search_score option, default is 0.01",
                    equate=False),
            _Option(["--search_score", "search_score"],
                    "The score cutoff used in the HMMER search, low numbers may slow down the process, cannot be used "
                    "with the --search_eval option, default is to used E-value cutoff, not score",
                    equate=False),

            _Option(["--cpu", "cpu"],
                    "the number of CPU threads to use, default is 1",
                    equate=False),

            # Output Options
            _BooleanOption(["--summary", "summary"],
                           "Summary of results output, on (T) by default"),
            _BooleanOption(["--graphical", "graphical"],
                           "'Graphical' output, on (T) by default"),
            _BooleanOption(["--fasta", "fasta"],
                           "FASTA-format output of extracted ITS sequences, on (T) by default"),
            _BooleanOption(["--preserve", "preserve"],
                           "Preserve sequence headers in input file instead of printing out ITSx headers, off (F) by "
                           "default"),
            _BooleanOption(["--only_full", "only_full"],
                           "If true, output is limited to full-length regions, off (F) by default"),
            _BooleanOption(["--concat", "concat"],
                           "Saves a FASTA-file with concatenated ITS sequences (with 5.8S removed), off (F) by "
                           "default"),
            _BooleanOption(["--positions", "positions"],
                           "Table format output containing the positions ITS sequences were found in, "
                           "on (T) by default"),
            _BooleanOption(["--table", "table"],
                           "Table format output of sequences containing probable ITS sequences, off (F) by default"),
            _BooleanOption(["--not_found", "not_found"],
                           "Saves a list of non-found entries, on (T) by default"),
            _BooleanOption(["--detailed_results", "detailed_results"],
                           "Saves a tab-separated list of all results, off (F) by default"),
            _BooleanOption(["--truncate", "truncate"],
                           "Truncates the FASTA output to only contain the actual ITS sequences found, "
                           "on (T) by default"),
            _BooleanOption(["--silent", "silent"],
                           "Supresses printing progress info to stderr, off (F) by default"),
            _BooleanOption(["--save_raw", "save_raw"],
                           "Saves all raw data for searches etc. instead of removing it on finish, off (F) by default"),
            _Option(["--anchor", "anchor"],
                    "Saves an additional number of bases before and after each extracted region. If set to 'HMM' all "
                    "bases matching the corresponding HMM will be output, default = 0",
                    equate=False),
            _Option(["--partial", "partial"],
                    "Saves additional FASTA-files for full and partial ITS sequences longer than the specified "
                    "cutoff, default = 0 (off)",
                    equate=False),
            _Option(["--minlen", "minlen"],
                    "Minimum length the ITS regions must be to be outputted in the concatenated file (see above), "
                    "default = 0",
                    equate=False),
            _Option(["--save_regions", "save_regions"],
                    "A comma separated list of regions to output separate FASTA files for, 'ITS1,ITS2' by default",
                    equate=False)
        ]
        try:
            # Insert extra parameters - at the start just in case there
            # are any arguments which must come last:
            self.parameters = extra_parameters + self.parameters
        except AttributeError:
            # Should we raise an error?  The subclass should have set this up!
            self.parameters = extra_parameters
        AbstractCommandline.__init__(self, cmd, **kwargs)


if __name__ == '__main__':
    print ITSx(graphical="T")
    pass
