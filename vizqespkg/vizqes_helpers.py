import sys

GAP = '-'


class Alignment(object):
    """ Store alignment information """
    def __init__(self, name=None, fasta=None):
        self.name = name
        self.fasta = fasta
        self.members = []
        self.attach_sequences()
        self.gap_pos = []
        self.mismatch_pos = []
        self.match_pos = []
        self.match_gap_pos = []

    def calc_numbers(self):
        for i in range(0, len(self)):
            curpos = [m.sequence[i] for m in self.members]
            if GAP in curpos:
                self.gap_pos.append(i)
            nongap = [c for c in curpos if c != GAP]
            cpset = set(curpos)
            if len(cpset) > 1 and GAP not in cpset:
                self.mismatch_pos.append(i)
            elif len(cpset) == 1 and GAP not in cpset:
                self.match_pos.append(i)
            elif len(cpset) == 2 and GAP in cpset and len(nongap) > 2:
                self.match_gap_pos.append(i)

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

    @staticmethod
    def shapely(char):
        pass

    @staticmethod
    def maeditor(char):
        if char in ["A", "G"]:
            return (32, 178, 170)
        elif char in ["C"]:
            return (0, 255, 0)
        elif char in ["D", "E", "N", "Q"]:
            return (0, 100, 0)
        elif char in ["I", "L", "M", "V"]:
            return (0, 0, 255)
        elif char in ["F", "W", "Y"]:
            return (218, 112, 214)
        elif char in ["H"]:
            return (0, 0, 100) #Dark blue
        elif char in ["K", "R"]:
            return (255, 165, 0)
        elif char in ["P"]:
            return (255, 192, 203)
        elif char in ["S", "T"]:
            return (255, 0, 0)
        elif char in ["-"]:
            return (242, 242, 242)
        elif char in ["X"]:
            return (23, 23, 23)
        else:
            return (0, 0, 0)

    # unique color for each amino acid
    @staticmethod
    def aacid(char):
        if char in ["A"]:
            return 235, 0, 124
        elif char in ["R"]:
            return 255, 13,  0
        elif char in ["N"]:
            return 149,  0, 219
        elif char in ["D"]:
            return 159, 247, 0
        elif char in ["C"]:
            return 50, 238, 0
        elif char in ["Q"]:
            return 0, 216, 180
        elif char in ["E"]:
            return 180, 249, 0
        elif char in ["G"]:
            return 251,  0, 29
        elif char in ["H"]:
            return 255, 44, 0
        elif char in ["I"]:
            return 255, 133, 0
        elif char in ["L"]:
            return 239, 0, 101
        elif char in ["K"]:
            return 0, 226, 84
        elif char in ["M"]:
            return 0, 190, 114
        elif char in ["F"]:
            return 0,100,183
        elif char in ["P"]:
            return 101, 232, 0
        elif char in ["S"]:
            return 255, 76, 0
        elif char in ["T"]:
            return 107, 23, 153
        elif char in ["W"]:
            return 156, 16, 144
        elif char in ["Y"]:
            return 183, 221, 23
        elif char in ["V"]:
            return 230,230, 24
        elif char in ["-"]:
            return 255, 255, 255
        elif char in ["X"]:
            return 180, 180, 180

    @staticmethod
    def feature(char):

        if char in ["match"]:
            return 0, 255, 0
        elif char in ["mismatch"]:
            return 255, 0,  0
        elif char in ["gap_match"]:
            return 0,  0, 255
        elif char in ["gap"]:
            return 0, 0, 0

     #DNA
    @staticmethod
    def dna_color(char):
        if char in ["A"]:
            return 255, 0, 0
        elif char in ["a"]:
            return 127, 0, 0
        elif char in ["T"]:
            return 0, 255, 0
        elif char in ["t"]:
            return 0, 175, 0
        elif char in ["G"]:
            return 0, 0, 255
        elif char in ["g"]:
            return 0, 0, 175
        elif char in ["C"]:
            return 255, 255, 0
        elif char in ["c"]:
            return 175, 175, 0
        elif char in ["-"]:
            return 180, 180, 180
        else:
            sys.stderr.write("Found character: {}\n".format(char))
            raise WrongInputException

    @staticmethod
    def color(char, colorscheme=None):
        colorfunc = Colorizer.maeditor
        if colorscheme:
            if colorscheme == "cinema":
                colorfunc = Colorizer.cinema
            elif colorscheme == "lesk":
                colorfunc = Colorizer.lesk
            elif colorscheme == "clustal":
                colorfunc = Colorizer.clustal
            elif colorscheme == "shapely":
                colorfunc = Colorizer.shapely
            elif colorscheme == "dna":
                colorfunc = Colorizer.dna_color
            elif colorscheme == "aacid":
                colorfunc = Colorizer.aacid
            elif colorscheme == "maeditor" or colorscheme == "default":
                colorfunc = Colorizer.maeditor
            elif colorscheme == "feature":
                colorfunc = Colorizer.feature
        return colorfunc(char)


class WrongInputException(Exception):
    pass


