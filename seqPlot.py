#!/usr/bin/env python

import sys
import os
import getopt

from seqplot import seqplot_main
here = os.path.dirname(__file__)


def main():
    """Main"""
    """Main"""
    aln_file = None
    boxwidth = 1
    boxheight = 1
    colorscheme = "default"
    outfile = None
    fontpath = None
    show_names = False
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:],
                                       "f:F:o:x:y:c:sh",
                                       ["fasta=",
                                        "font_file",
                                        "outifle",
                                        "boxwidth=",
                                        "boxheight=",
                                        "colorscheme=",
                                        "show_names",
                                        "help"])
    except getopt.GetoptError as err:
        print(str(err))
        seqplot_main.usage()
    for o, a in opts:
        if o in ("-f", "--fasta"):
            aln_file = a
        elif o in ("-h", "--help"):
            seqplot_main.usage()
        elif o in ("-o", "--outfile"):
            outfile = a
            if not outfile.endswith(".png"):
                outfile += ".png"
        elif o in ("-x", "--boxwidth"):
            boxwidth = int(a)
        elif o in ("-y", "--boxheight"):
            boxheight = int(a)
        elif o in ("-c", "--colorscheme"):
            colorscheme = a
        elif o in ("-F", "--font_file"):
            fontpath = a
        elif o in ("-s", "--show_names"):
            show_names = True
        else:
            print(o)
            assert False, "unhandled option"
    if not aln_file:
        seqplot_main.usage()

    colorschemes = ["default", "maeditor", "cinema", "lesk", "clustal", "aacid", "dna"]
    if not colorscheme in colorschemes:
        sys.stderr.write("No such colorscheme: {}\n"
                         "available: {}\n falling back to default".format(colorscheme, ",".join(colorschemes)))
        colorscheme = "default"

    seqplot_main.draw(aln_file=aln_file, outfile=outfile, colorscheme=colorscheme, boxwidth=boxwidth,
         boxheight=boxheight, show_names=show_names, fontpath=fontpath)


if __name__ == "__main__":
    main()
