# BlobMapper
BlobMapper is a tool which aids in building models from CryoEM or X-ray electron density maps. Often it is difficult to identify which protein chains are responsible for a given area of map density; one of the best ways to identify these chains is by looking for patterns of noticeable large or small residues and trying to see which protein sequence could match that pattern. BlobMapper is a tool to help structural biologists turn these 'blobs' into protein chains.

# Basic Use
To use blobMapper, you need to first create a FASTA file containing the sequences of all the proteins that could be a part of the structure. As an example, if I were working with a nucleosome particle, my proteins would be H2A, H2B, H3, and H4, all combined into one FASTA file like this:

>\>H2A\
>MSGRGKQGGKARAKAKTRSSRAGLQFPVGRVRRLLRKGNYAERVGAGAPVYLAAVLEYLT\
>AEILELAGNAARDNKKTRIIPRHLQLAIRNDEELNKLLGKVTIAQGGVLPNIQAVLLPKK\
>TESHHKAKGK
>
>\>H2B\
>MPDPAKSAPAPKKGSKKAVTKVQKKDGKKRKRSRKESYSVYVYKVLKQVHPDTGISSKAM\
>GIMNSFVNDIFERIAGEASRLAHYNKRSTITSREIQTAVRLLLPGELAKHAVSEGTKAVT\
>KYTSSNPRNLSPTKPGGSEDRQPPPSQLSAIPPFCLVLRAGIAGQV
>
>\>H3\
>MARTKQTARKSTGGKAPRKQLATKAARKSAPSTGGVKKPHRYRPGTVALREIRRYQKSTE\
>LLIRKLPFQRLVREIAQDFKTDLRFQSAAIHAKRVTIMPKDIQLARRIRGERA
>
>\>H4\
>MSGRGKGGKGLGKGGAKRHRKVLRDNIQGITKPAIRRLARRGGVKRISGLIYEETRGVLK\
>VFLENVIRDAVTYTEHAKRKTVTAMDVVYALKRQGRTLYGFGG

Then, to execute the script, you run:

`python3 blobMapper.py -m [number of allowable mismatches] -p [pattern] [path to fasta file]`

The parameter p is where you input your pattern to search for. This pattern has to be input using specific syntax described below.

The parameter m is an optional value where you can input the number of allowable mismatches. If you leave it out, m defaults to 0, and the script will only show results that are perfect matches. As an example, if you set m to 1, then the script will show results that are perfect matches and results where one residue is not matched up correctly. This can be useful due to the ambiguity when trying to identify residues based on an electron map.

If I search the above sequences for a motif of phenylanine, followed by proline, followed by two unknown residues, followed by arginine, with the command `python3 blobMapper.py -p 'FPXXR' Fasta.seq` I will see these results:

>Forward:
>
>  Perfect Match:\
>  H2A: [26]
>
>
>Reverse:
>
>  Perfect Match:\
>    H3: [68]

These results show that in H2A, residue number 26 matches this pattern going forward and in H3 residue number 68 matches this pattern going in reverse. We can see that is true because H2A residue 26 going forward is `FPVGR` which matches the pattern and H3 residue 68 going in reverse is `FPLKR` which also matches the pattern.

## Pattern Syntax
Since the `>` operator and parentheses have meaning in the unix terminal, the -p argument must be enclosed in quotations.

* Use the standard single letter codes to indicate a specific amino acid residue
* Use `>` to indicate a large residue. By default: W, F, Y, R, or H are considered large.
* Use `=` to indicate a medium sized residue. By default: M, L, I, Q, N, H and K are considered medium.
* Use `<` to indicate a small residue. By default: G, A, S, T, P, K, E, D and C are considered small.
* Use single letter codes enclosed in parentheses to indicate one of multiple residues
  * For example, if you believe a residue is either F or Y, you can encode this specific option by writing `(FY)` to represent a residue that is either F or Y.
* Use `X` to indicate any residue.
* Use numbers to indicate a stretch of `X` residues.

# Examples
The best way to understand the syntax is through examples. For the following I will assume I have my protein sequences in a file titled Fasta.seq and that my terminal is positioned in a directory containing both blobmapper.py and Fasta.seq.

If I want to search for the sequence WFF, I can do that by running:

`python3 blobMapper.py -p 'WFF' Fasta.seq`

If I'm sure that the first residue is a tryptophan, but not sure that the following two are phenylalanine, I could broaden the search so that instead of searching for tryptophan followed by two phenylalanines, I am searching for tryptophan followed by two large residues. I can do that by running:

`python3 blobMapper.py -p 'W>>' Fasta.seq`

If I see a tryptophan, then two small residues, then an ambiguous residue, and then a large residue, I could search for that by running:

`python3 blobMapper.py -p 'W<<X>' Fasta.seq`

If I'm looking at my map and I see two large residues, a space of 8 ambiguous residues and then two more large residues, I could search for that by running:

`python3 blobMapper.py -p '>>8>>' Fasta.seq`

If I see a tryptophan, then a space of 5 residues, then what is either F or Y, then 7 more residues, then another tryptophan, I can search for that by running:

`python3 blobMapper.py -p 'W5(FY)7W' Fasta.seq`

If I see what I think is two tryptophans followed by 6 residues, and then a tyrosine but I am not completely sure, I would want to search with some mismatch allowance. I could do this search allowing for one mismatch by running:

`python3 blobMapper.py -m 1 -p 'WW6Y'`

# Other Notes
Since it is sometimes hard to determine which direction a chain is going based on electron density alone, the script will search your sequences both in the forward and reverse directions.

It is important to ensure that your peptide backbone is correct, without missing or inserted residues. As an example, if you search for `WF12W` and your sequence has `WF11W` it will not show as a result. This may be changed in the future to add misspacing tolerance, but as of now, it is important to maintain accuracy with the spacing between residues. If you are unsure of the spacing, you can manually try different, reasonable values of the spacing between two anchoring residues with an appropriate mismatch value.

I've found the best way to identify chains is by synthesizing guesses over long distances. Depending on the quality of your map, it can be hard to identify residues beyond classifying them as big, medium or small. However, this can be enough to identify chains. You can create a very specific search if you look for something like a big residue, a space of 15 residues, then a big residue, then a space of 23 residues followed by another big residue. The odds of a motif like this appearing randomly are quite low. Even if the map quality is good enough to identify characteristic residues such as tryptophan or arginine, this approach of searching for anchor residues over known distances can be very useful to identifying protein chains.
