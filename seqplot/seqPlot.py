#!/usr/env/python
import sys
import os
import getopt
import Image
import ImageDraw
import ImageFont
from seqplot.seqplot_helpers import Alignment
from seqplot.seqplot_helpers import Colorizer



def main():
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
        usage()
    for o, a in opts:
        if o in ("-f", "--fasta"):
            aln_file = a
        elif o in ("-h", "--help"):
            usage()
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
        usage()

    colorschemes = ["default", "maeditor", "cinema", "lesk", "clustal"]
    if not colorscheme in colorschemes:
        sys.stderr.write("No such colorscheme: {}\n"
                         "available: {}\n falling back to default".format(colorscheme, ",".join(colorschemes)))
        colorscheme = "default"

    draw(aln_file=aln_file, outfile=outfile, colorscheme=colorscheme, boxwidth=boxwidth,
         boxheight=boxheight, show_names=show_names, fontpath=fontpath)


def draw(aln_file, outfile, colorscheme, boxwidth, boxheight, show_names=False, fontpath=None):
    #defaults
    width = 800
    height = 600
    boxwidth = boxwidth
    boxheight = boxheight
    offset = 0
    font = None
    #read in fasta
    al = Alignment(name=aln_file, fasta=aln_file)
    names = [m.name for m in al.members]
    if show_names:
        if fontpath:
            font = ImageFont.truetype(fontpath, boxheight)
        else:
            font = ImageFont.truetype(os.path.dirname(__file__)+os.sep+"data"+os.sep+"FreeMono.ttf", boxheight)
        offset = font.getsize(max(names, key=len))[0]

    height = len(al.members) * boxheight
    width = len(al.members[0].sequence) * boxwidth + offset

    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    yd = None

    for y, member in enumerate(al.members):
        y *= boxheight
        for x, xs in enumerate(member.sequence):
            x *= boxwidth
            color = Colorizer.color(char=xs, colorscheme=colorscheme)
            for i in xrange(0, boxwidth):
                xd = x + i + offset
                for j in xrange(0, boxheight):
                    yd = y + j
                    draw.point((xd, yd), fill=color)
        if show_names:
            draw.text((0, yd-boxheight), member.name, font=font, fill=(0, 0, 0))

    if not outfile:
        img.save(aln_file+".png", "png")
    else:
        img.save(outfile, "png")


def usage():
    print("""
    ######################################
    # seqPlot.py
    ######################################
    usage:
        seqPlot.py -f multifasta alignment
    options:
         -f, --fasta=FILE    multifasta alignment (eg. "align.fas")

       [ -o, --outfile=STR   output file (png) ]
       [ -c, --colorscheme=STR STR in ("default", "clustal", "lesk",
                                       "cinema", "maeditor") ]
       [ -x, --boxwidth=INT draw INT pixels per residue (x direction) ]
       [ -y, --boxheight=INT draw INT pixels per residue (y direction) ]

    adding identifiers:
       [ -s, --show_names    also draw sequence ids ]
       [ -F, --font_file=FONT path to truetype font (monospace fonts recommended) ]
    """)
    sys.exit(2)
############################################


if __name__ == "__main__":
    main()
