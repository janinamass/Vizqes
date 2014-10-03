import sys

class Alignment(object):
    """ Store alignment information """
    def __init__(self, name=None, fasta=None):
        self.name = name
        self.fasta = fasta
        self.members = []
        self.attach_sequences()

    def __repr__(self):
        ids = self.members
        return "Alignment:{},{}".format(self.name, ids)

    def __len__(self):
        try:
            return len(self.members[0].sequence)
        except TypeError as err:
            sys.stderr.write(err)
            sys.stderr.write("attach_sequences first")
            return 0

    def attach_sequences(self):
        """Read fasta file, create Sequence objects and attach them to self.members"""
        print("FASTA:", self.fasta)
        for seq in FastaParser.read_fasta(self.fasta):
            new_seq = Sequence(name=seq[0], sequence=seq[1])
            self.members.append(new_seq)


class Sequence(object):
    def __init__(self, name="", sequence=None, is_foreground=False):
        self.name = name
        self.sequence = sequence

    def __repr__(self):
        return "Sequence: {}".format(self.name)


class FastaParser(object):
    @staticmethod
    def read_fasta(fasta, delim=None, as_id=0):
        """read from fasta fasta file 'fasta'
        and split sequence id at 'delim' (if set)\n
        example:\n
        >idpart1|idpart2\n
        ATGTGA\n
        and 'delim="|"' returns ("idpart1", "ATGTGA")
        """
        name = ""
        fasta = open(fasta, "r")
        while True:
            line = name or fasta.readline()
            if not line:
                break
            seq = []
            while True:
                name = fasta.readline()
                name = name.rstrip()
                if not name or name.startswith(">"):
                    break
                else:
                    seq.append(name)
            joined_seq = "".join(seq)
            line = line[1:]
            if delim:
                line = line.split(delim)[as_id]
            yield (line.rstrip(), joined_seq.rstrip())
        fasta.close()

###########################################


class Colorizer():
    """ Color residues """
    # color schemes adapted from
    # http://www.bioinformatics.nl/~berndb/aacolour.html
    @staticmethod
    def cinema(char):
        if char in ["H", "K", "R"]:
            return (0, 0, 200)
        elif char in ["D", "E"]:
            return (200, 0 , 0)
        elif char in ["S", "T", "N", "Q"]:
            return (0, 200, 0)
        elif char in ["A", "V", "L", "I", "M"]:
            return (255, 255, 255)
        elif char in ["F", "W", "Y"]:
            return (255, 0, 255)
        elif char in ["P","G"]:
            return (165, 42, 42)
        elif char in ["C"]:
            return (255, 255, 0)
        elif char in ["B", "Z", "X"]:
            return (190, 190, 190)

    @staticmethod
    def lesk(char):
        if char in ["G", "A", "S", "T"]:
            return (255, 165, 0)
        elif char in ["C", "V", "I", "L", "P", "F", "Y", "M", "W"]:
            return (0, 255, 0)
        elif char in ["N", "Q", "H", "M"]:
            return (255, 0, 255)
        elif char in ["D", "E"]:
            return (255, 0, 0)
        elif char in ["K", "R"]:
            return (0, 0, 255)
        else:
            return (23, 23, 23)


    @staticmethod
    def clustal(char):
        if char in ["G", "P", "S", "T"]:
            return (255, 165, 0)
        if char in [ "H", "K", "R"]:
            return (255, 0, 0)
        if char in ["F", "W", "Y", "B"]:
            return (0, 0, 255)
        if char in ["I", "L", "M", "V"]:
            return (0, 255, 0)
        else:
            return (23, 23, 23)



        pass

    @staticmethod
    def shapely(char):
        pass

    @staticmethod
    def maeditor(char):
        pass

    colors = {
    "A": (32, 178, 170),  #light green
    "G": (32, 178, 170),  #light green
    "C": (0, 200, 0),  #green
    "D": (0, 100, 0),  #dark green
    "E": (0, 100, 0),  #dark green
    "N": (0, 100, 0),  #dark green
    "Q": (0, 100, 0),  #dark green
    "I": (0, 0, 200),  #Blue
    "L": (0, 0, 200),  #Blue
    "M": (0, 0, 200),  #Blue
    "V": (0, 0, 200),  #Blue
    "F": (218, 112, 214), #orchid
    "W": (218, 112, 214), #orchid
    "Y": (218, 112, 214), #orchid /Lilac
    "H": (0, 0, 100),  #Dark blue
    "K": (255, 165, 0),	 #Orange
    "R": (255, 165, 0),
    "P": (255, 192, 203), #	Pink
    "S": (255, 0, 0),  #
    "T": (255, 0, 0), #Red
    "-": (242, 242, 242),
    "X": (23, 23, 23)
    }

    @staticmethod
    def color(char, colorscheme=None):
        if not colorscheme:
            return Colorizer.colors[char]
        else:

            colorfunc = None
            if colorscheme:
                if colorscheme == "cinema":
                    colorfunc = Colorizer.cinema
                elif colorscheme == "lesk":
                    colorfunc = Colorizer.lesk
                elif colorscheme == "clustal":
                    colorfunc = Colorizer.clustal
                elif colorfunc == "shapely":
                    colorfunc = Colorizer.shapely
                elif colorscheme == "maeditor" or colorscheme == "default":
                    colorfunc = Colorizer.maeditor

            return colorfunc(char)
