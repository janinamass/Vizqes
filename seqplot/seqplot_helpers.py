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
            return (0,0,0)



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
