SeqPlot
=======

Plot overview of Multiple Sequence Alignments (MSA) using colored boxes


    ######################################
    # seqPlot.py
    ######################################
    usage:
        seqPlot.py -f multifasta alignment
    options:
         -f, --fasta=FILE    multifasta alignment (eg. "align.fas")

       [ -o, --outfile=STR   output file (png) ]
       [ -c, --colorscheme=STR STR in ("default", "clustal", "lesk",
                                       "cinema", "maeditor", "dna",
                                       "aacid") ]
       [ -x, --boxwidth=INT draw INT pixels per residue (x direction) ]
       [ -y, --boxheight=INT draw INT pixels per residue (y direction) ]

    adding identifiers:
       [ -s, --show_names    also draw sequence ids ]
       [ -F, --font_file=FONT path to truetype font (monospace fonts recommended) ]
