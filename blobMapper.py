import glob
import argparse
import os
import time

maxMismatches = 0


def parseArgs():
    """Parses arguments and returns them as an args object"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'path', nargs=1, help='the path of the fasta file')
    parser.add_argument(
        '-p', nargs=1, type=str, default="X", help='Define the pattern to search for')
    parser.add_argument(
        '-m', nargs=1, type=int, default=[0], help='Use this argument to define the number of allowable mismatches, defualts to 0')
    args = parser.parse_args()
    return args


def equal(residue, input):
    residue = residue.upper()
    if(input == "X"):
        return True
    elif(input == residue):
        return True
    elif(input == ">"):
        return residue == "W" or residue == "F" or residue == "Y" or residue == "R" or residue == "H"
    elif(input == "="):
        return residue == "M" or residue == "L" or residue == "I" or residue == "Q" or residue == "N" or residue == "H" or residue == "K"
    elif(input == "<"):
        return residue == "G" or residue == "A" or residue == "S" or residue == "T" or residue == "P" or residue == "K" or residue == "E" or residue == "D" or residue == "C"
    if(len(input) > 1):
        l = list(input)
        for i in l:
            if (residue == i):
                return True
    return False


class location():
    """A location is an object to track location of a match in a protein sequence
    and also allow me to keep track of mismatch levels"""

    def __init__(self, value, mismatches):
        self.value = value
        self.mismatches = mismatches

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.value == other.value and self.mismatches == other.mismatches


class pattern():

    def __init__(self, pattern):
        self.pattern = pattern
        self.l = self.listify()
        self.maxMismatches = maxMismatches

    def listify(self):
        """Converts the pattern into a list of protein residues including X"""
        l = []
        reading = False
        readingDigit = False
        temp = ""
        for i in self.pattern:
            if(str.isdigit(i)):
                readingDigit = True
            if(readingDigit):
                if(str.isdigit(i)):
                    temp += i
                else:
                    num = int(temp)
                    for x in range(num):
                        l.append("X")
                    temp = ""
                    readingDigit = False
            if(i == ")"):
                reading = False
                l.append("(" + temp.upper() + ")")
                temp = ""
            elif reading:
                temp += i
            elif(i == "("):
                reading = True
            else:
                if(not readingDigit):
                    l.append(i.upper())
        if(temp.isdigit()):
            num = int(temp)
            for x in range(num):
                l.append("X")
        return l

    def next(self):
        return self.l.pop(0)

    def hasNext(self):
        return len(self.l) > 0

    def matches(self, input):
        startPoint = False
        matchPoints = []
        index = 0
        for i in input:
            if(index + len(self.l) <= len(input)):
                startPoint = True
            if(startPoint):
                mismatches = 0
                for x in range(len(self.l)):
                    if(not equal(input[index + x], self.l[x])):
                        mismatches += 1
                    if(mismatches > self.maxMismatches):
                        break
                if(mismatches <= self.maxMismatches):
                    matchPoints.append(location(index+1, mismatches))
                startPoint = False
            index += 1
        return matchPoints


class fasta():

    def __init__(self, path):
        self.path = path
        self.chains = {}
        self.__read()

    def __read(self):
        """Reads FASTA into lists, and puts each list into the chains dictionary where the chain name is the key"""
        protName = ""
        with open(self.path, "r") as fasta:
            characters = []
            for line in fasta:
                line = line.rstrip()  # Remove trailing \n
                if(line.startswith('>')):
                    if(protName != ""):
                        self.chains[protName] = characters
                    protName = line.split(">")[1].upper()
                    characters = []
                else:
                    for char in line:
                        characters.append(char)
            self.chains[protName] = characters

    def get(self, chain):
        """Returns a list of amino acids for the given chain"""
        return self.chains[chain.upper()]

    def hasPattern(self, pat):
        """Returns a dictionary, where the keys are the chain names and the values
        are lists of each location where the pattern is found"""
        p = pattern(pat)
        candidates = {}
        for i in self.chains:
            candidates[i] = p.matches(self.chains[i])
        return candidates

    def hasReversePattern(self, pat):
        """Returns a dictionary, where the keys are the chain names and the values
        are lists of each location where the pattern is found"""
        p = pattern(pat)
        candidates = {}
        for i in self.chains:
            matches = p.matches(self.chains[i][::-1])
            for x in range(len(matches)):
                matches[x] = location(
                    len(self.chains[i]) - (matches[x].value) + 1, matches[x].mismatches)
            candidates[i] = matches
        return candidates


def printResults(f):
    """Prints the results from parsing the fasta file for the pattern"""

    def printCandidates(cand):
        """Print the formatted output from an input list of locations"""
        for m in range(maxMismatches + 1):
            if(m == 1):
                print("  " + str(m) + " Mismatch:")
            else:
                print("  " + str(m) + " Mismatches:")
            for i in cand:
                toPrint = []
                for c in cand[i]:
                    if(c.mismatches == m):
                        toPrint.append(c)
                if(len(toPrint) > 0):
                    print("    " + i, end=": ")
                    print(toPrint)
            print('')

    candidates = f.hasPattern(args.p[0])
    revCandidates = f.hasReversePattern(args.p[0])
    print("Forward:")
    print("")
    printCandidates(candidates)
    print("")
    print("Reverse:")
    print("")
    printCandidates(revCandidates)


if __name__ == '__main__':
    start = time.time()
    args = parseArgs()
    maxMismatches = args.m[0]
    relPath = args.path[0]
    absPath = os.path.abspath(relPath)
    f = fasta(absPath)
    printResults(f)
    print('It took', time.time()-start, 'seconds.')
