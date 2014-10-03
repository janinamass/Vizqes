#!/usr/env/python
import sys
import getopt
import Image
import ImageDraw
from seqplot_helpers import Alignment
from seqplot_helpers import Colorizer



def main():
    """Main"""
    aln_file = None
    boxwidth = 1
    boxheight = 1
    colorscheme = "default"
    outfile = None
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:],
                                       "f:o:x:y:c:h",
                                       ["fasta=",
                                        "outifle",
                                        "boxwidth=",
                                        "boxheight=",
                                        "colorscheme=",
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


    draw(aln_file=aln_file, outfile=outfile, colorscheme=colorscheme, boxwidth=boxwidth, boxheight=boxheight)


def draw(aln_file, outfile, colorscheme, boxwidth, boxheight):
    #defaults
    width = 800
    height = 600
    boxwidth = boxwidth
    boxheight = boxheight
    al = Alignment(name="test", fasta=aln_file)
    print(al)


    height = len(al.members) * boxheight
    width = len(al.members[0].sequence) * boxwidth

    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)

    for y, member in enumerate(al.members):
        y *= boxheight
        for x, xs in enumerate(member.sequence):
            x *= boxwidth
            color = Colorizer.color(char=xs, colorscheme=colorscheme)
            for i in xrange(0, boxwidth):
                xd = x + i
                for j in xrange(0, boxheight):
                    yd = y + j
                    draw.point((xd, yd), fill=color)
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
        -o, --outfile=STR   output file (png)
        -c, --colorscheme=STR STR in ["default", "clustal", "lesk", "cinema", "shapely", "maeditor"] #todo
        -x, --boxwidth=INT draw INT pixels per residue (x direction)
        -y, --boxheight=INT draw INT pixels per residue (y direction)
    """)
    sys.exit(2)
############################################


if __name__ == "__main__":
    main()