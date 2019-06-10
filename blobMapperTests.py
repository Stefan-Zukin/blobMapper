#!/usr/bin/python3
# coding: utf-8

import blobMapper as m
from blobMapper import location
import unittest

residues = ['R', 'K', 'D', 'E', 'Q', 'N', 'H', 'S', 'T', 'Y', 'C', 'W', 'M', 'A', 'I', 'L', 'F', 'V', 'P', 'G']
seq = list("MAPTISKRIKTLSVSRPIIYGNTAKKMGSVKPPNAPAEHTHLWTIFVRGPQNEDISYFIKKVVFKLHDTYPNPVRSIEAPPFELTETGWGEFDINIKVYFVEEANEKVLNFYHRLRLHPY")

class TestModelHelper(unittest.TestCase):
    

    def testEquals(self):
        for r in residues:
            self.assertTrue(m.equal(r, 'X'))
            self.assertTrue(m.equal(r, r))
        for r in ['A', 'C', 'Y']:
            self.assertTrue(m.equal(r, "(ACY)"))
        for r in ['A', 'C', 'Y']:
            self.assertFalse(m.equal(r, "(QTH)"))
        for r in ['Y', 'W', 'F', 'R']:
            self.assertTrue(m.equal(r, '>'))

    def testMatches(self):
        p = m.pattern("TISKRIK")
        self.assertEqual([location(4,0)], p.matches(seq))
        p = m.pattern("TIS(KRTHW)RIK")
        self.assertEqual([location(4,0)], p.matches(seq))
        p = m.pattern("W(TG)")
        self.assertEqual([location(43,0),location(89,0)], p.matches(seq))
        p = m.pattern("FXX")
        self.assertEqual([location(46,0),location(58,0),location(64,0),location(82,0),location(92,0),location(100,0),location(111,0)], p.matches(seq))
        p = m.pattern("F")
        self.assertEqual([location(46,0),location(58,0),location(64,0),location(82,0),location(92,0),location(100,0),location(111,0)], p.matches(seq))
        p = m.pattern("F(EV)")
        self.assertEqual([location(46,0),location(82,0),location(100,0)], p.matches(seq))
        p = m.pattern("F>")
        self.assertEqual([location(111,0)], p.matches(seq))
        p = m.pattern(">>")
        self.assertEqual([location(57,0),location(99,0), location(111,0), location(112,0), location(113,0)], p.matches(seq))
        p = m.pattern("T=<KRIK")
        self.assertEqual([location(4,0)], p.matches(seq))

    def testMismatches(self):
        p = m.pattern("TISKRIK")
        p.maxMismatches = 1
        self.assertEqual([location(4,0)], p.matches(seq))
        p = m.pattern("TQSKRIK")
        p.maxMismatches = 1
        self.assertEqual([location(4,1)], p.matches(seq))
        p = m.pattern("TQQKRIK")
        p.maxMismatches = 2
        self.assertEqual([location(4,2)], p.matches(seq))
        p = m.pattern("TQQKRIK")
        p.maxMismatches = 1
        self.assertNotEqual([location(4,2)], p.matches(seq))
        p = m.pattern("WISKRIK")
        p.maxMismatches = 1
        self.assertEqual([location(4,1)], p.matches(seq))
        p = m.pattern("WWWWRIK")
        p.maxMismatches = 4
        self.assertEqual([location(4,4)], p.matches(seq))
        p = m.pattern("WWWWWWPP")
        p.maxMismatches = 5
        self.assertEqual([], p.matches(seq))
        p = m.pattern("WWWWWWPP")
        p.maxMismatches = 6
        self.assertEqual([location(26,6), location(43,6), location(74,6)], p.matches(seq))

    
    def testFasta(self):
        f = m.fasta("/Users/stefanzukin/Desktop/Programming/Python/modelHelper/FASTA.seq")
        d = f.hasPattern("FFFFFF")
        for l in d:
            self.assertEqual(0, len(d[l]))
        d = f.hasPattern("X") 
        for l in d:
            self.assertNotEqual(0, len(d[l]))   
        d = f.hasPattern("10") 
        for l in d:
            self.assertNotEqual(0, len(d[l]))   
        d = f.hasPattern("SDTSRNDSDISIAGKDDIGIIANVDDITEKESAAANDNDENGKNEAGAK") 
        self.assertEqual([location(430,0)], d["EAF1"])
        d = f.hasPattern("TPSNAIEINDGSHKSGRSTRRSGSRS")
        self.assertEqual([location(3,0)], d["EPL1"])
        d = f.hasPattern("TPSNAIEI3SHKSGR4SGSRS")
        self.assertEqual([location(3,0)], d["EPL1"])
        d = f.hasPattern("(TPP)PSNA1EI3SHKSGR4SGSRS")
        self.assertEqual([location(3,0)], d["EPL1"])
        d = f.hasPattern("SNA1EI3SHKSGR4SGSRS")
        self.assertEqual([location(5,0)], d["EPL1"])

        #Testing Reverse
        d = f.hasReversePattern("X") 
        for l in d:
            self.assertNotEqual(0, len(d[l]))  
        d = f.hasReversePattern("PVASS")
        self.assertEqual([location(10,0)], d["EAF1"])
        d = f.hasReversePattern("P3SP")
        self.assertEqual([location(10,0)], d["EAF1"])


if __name__ == '__main__':
    unittest.main()