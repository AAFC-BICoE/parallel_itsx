#!/usr/bin/env python
from Bio.Application import AbstractCommandline, _Switch, _Option
__doc__ = '''Provides ITSx wrapper for 1.0.11'''
__author__ = 'mike knowles'


class _ValOption(_Option):
    def __str__(self):
        """Return the value of this option for the commandline.
    
        Includes a trailing space.
        """
        # Note: Before equate was handled explicitly, the old
        # code would do either "--name " or "--name=value ",
        # or " -name " or " -name value ".  This choice is now
        # now made explicitly when setting up the option.
        if self.value:
            v = str(self.value)
            if self.equate:
                return "%s=%s " % (self.names[0], v)
            else:
                return "%s %s " % (self.names[0], v)
        else:
            return ""


class ITSxCommandLine(AbstractCommandline):
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
            _ValOption(["-i", "i"],
                       "DNA FASTA input file to investigate",
                       filename=True,
                       equate=False),
            _ValOption(["-o", "o"],
                       "Base for the names of output file(s)",
                       filename=True,
                       equate=False),
            _ValOption(["-p", "p"],
                       "A path to a directory of HMM-profile collections representing ITS conserved regions, "
                       "default is "
                       "in the same directory as ITSx itself",
                       filename=True,
                       equate=False),
            _ValOption(["--date", "date"],
                       "Adds a date and time stamp to the output directory, off (F) by default",
                       equate=False),
            _ValOption(["--reset", "reset"],
                       "Re-creates the HMM-database before ITSx is run, off (F) by default",
                       equate=False),
        ]

        extra_parameters = [
            # Sequence Selection Options
            _ValOption(["--allow_reorder", "allow_reorder"],
                       "Allows profiles to be in the wrong order on extracted sequences, off (F) by default",
                       equate=False),
            _ValOption(["--complement", "complement"],
                       "Checks both DNA strands against the database, creating reverse complements, "
                       "on (T) by default",
                       equate=False),
            _ValOption(["--multi_thread", "multi_thread"],
                       "Multi-thread the HMMER-search, on (T) if number of CPUs (--cpu option > 1), else off (F) "
                       "by default",
                       equate=False),
            _ValOption(["--heuristics", "heuristics"],
                       "Selects whether to use HMMER's heuristic filtering, off (F) by default",
                       equate=False),
            _ValOption(["-t", "t"],
                       "Profile set to use for the search, see the User's Guide (comma-separated), default is all",
                       equate=False),
            _ValOption(["--allow_single_domain", "allow_single_domain"],
                       "Allow inclusion of sequences that only find a single domain, given that they meet the given "
                       "E-value and score thresholds, on with parameters 1e-9,0 by default",
                       equate=False),
            _ValOption(["--selection_priority", "selection_priority"],
                       "Selects what will be of highest priority when determining the origin of the sequence, "
                       "default is sum"),
            _ValOption(["-E", "E"],
                       "Domain E-value cutoff for a sequence to be included in the output, default = 1e-5",
                       equate=False),
            _ValOption(["-S", "S"],
                       "Domain score cutoff for a sequence to be included in the output, default = 0",
                       equate=False),
            _ValOption(["-N", "N"],
                       "The minimal number of domains that must match a sequence before it is included, default = 2",
                       equate=False),
            _ValOption(["--search_eval", "search_eval"],
                       "The E-value cutoff used in the HMMER search, high numbers may slow down the process, "
                       "cannot be used with the --search_score option, default is 0.01",
                       equate=False),
            _ValOption(["--search_score", "search_score"],
                       "The score cutoff used in the HMMER search, low numbers may slow down the process, "
                       "cannot be used "
                       "with the --search_eval option, default is to used E-value cutoff, not score",
                       equate=False),

            _ValOption(["--cpu", "cpu"],
                       "the number of CPU threads to use, default is 1",
                       equate=False),

            # Output Options
            _ValOption(["--summary", "summary"],
                       "Summary of results output, on (T) by default",
                       equate=False),
            _ValOption(["--graphical", "graphical"],
                       "'Graphical' output, on (T) by default",
                       equate=False),
            _ValOption(["--fasta", "fasta"],
                       "FASTA-format output of extracted ITS sequences, on (T) by default",
                       equate=False),
            _ValOption(["--preserve", "preserve"],
                       "Preserve sequence headers in input file instead of printing out ITSx headers, off (F) by "
                       "default",
                       equate=False),
            _ValOption(["--only_full", "only_full"],
                       "If true, output is limited to full-length regions, off (F) by default",
                       equate=False),
            _ValOption(["--concat", "concat"],
                       "Saves a FASTA-file with concatenated ITS sequences (with 5.8S removed), off (F) by "
                       "default",
                       equate=False),
            _ValOption(["--positions", "positions"],
                       "Table format output containing the positions ITS sequences were found in, "
                       "on (T) by default",
                       equate=False),
            _ValOption(["--table", "table"],
                       "Table format output of sequences containing probable ITS sequences, off (F) by default",
                       equate=False),
            _ValOption(["--not_found", "not_found"],
                       "Saves a list of non-found entries, on (T) by default",
                       equate=False),
            _ValOption(["--detailed_results", "detailed_results"],
                       "Saves a tab-separated list of all results, off (F) by default",
                       equate=False),
            _ValOption(["--truncate", "truncate"],
                       "Truncates the FASTA output to only contain the actual ITS sequences found, "
                       "on (T) by default",
                       equate=False),
            _ValOption(["--graph_scale", "graph_scale"],
                       "Sets the scale of the graphical output. If the provided value is zero, "
                       "a percentage view is shown. Default is 0",
                       equate=False),
            _ValOption(["--silent", "silent"],
                       "Supresses printing progress info to stderr, off (F) by default",
                       equate=False),
            _ValOption(["--save_raw", "save_raw"],
                       "Saves all raw data for searches etc. instead of removing it on finish, off (F) by default",
                       equate=False),
            _ValOption(["--anchor", "anchor"],
                       "Saves an additional number of bases before and after each extracted region. If set to 'HMM' "
                       "all "
                       "bases matching the corresponding HMM will be output, default = 0",
                       equate=False),
            _ValOption(["--partial", "partial"],
                       "Saves additional FASTA-files for full and partial ITS sequences longer than the specified "
                       "cutoff, default = 0 (off)",
                       equate=False),
            _ValOption(["--minlen", "minlen"],
                       "Minimum length the ITS regions must be to be outputted in the concatenated file (see above), "
                       "default = 0",
                       equate=False),
            _ValOption(["--save_regions", "save_regions"],
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
    print ITSxCommandLine(graphical="T")
    pass
