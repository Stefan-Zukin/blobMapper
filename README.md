# blobMapper
BlobMapper is a tool which aids in building models from CryoEM or X-ray electron density maps. Often is is difficult to identify which protein chains are responsible for a given area of electron density. The best ways to identify these chains are by looking for patterns of noticeable large or small residues and trying to see which protein sequence could match that pattern. BlobMapper is a tool to help structural biologists turn these 'blobs' into residues.

# Basic Use
To use blobMapper, you need to first create a FASTA file containing the sequences to all the proteins that could be a part of the structure. As an example, if I were working with a nucleosome particle, my proteins would be H2A, H2B, H3, and H4, all combined into one FASTA file like this:

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

Then, to execute the script, you do\
`python3 blobmapper.py -m [number of allowable mismatches] -p [pattern] [path to fasta file]`

The parameter m is an optional value where you can input the number of allowable mismatches. If you leave it out, m defaults to 0, and the script will only show results that are perfect matches. As an example, if you set m to 1, then the script will show results that are perfect matches and results where one residue is not matched up correctly. This can be useful due to the ambiguity when trying to identify residues based on an electron map.

The parameter p is where you input your pattern to search for. This pattern has to be input using specific syntax.

## Pattern Syntax
Since the `>`, `=` and `<` operators have meaning in the unix terminal, the -p argument must be enclosed in quotations.

* Use the standard single letter codes to indicate a specific amino acid residue
* Use `>` to indicate a large residue. By default: W, F, Y, R, or H are considered large.
* Use `=` to indicate a medium sized residue. By default: M, L, I, Q, N, H and K are considered medium.
* Use `<` to indicate a small residue. By default: G, A, S, T, P, K, E, D and C are considered small.
* Use paranthesis to indicate one of multiple residues
  * For example, if you believe a residue is either F or Y, you can encode this specific option by writing `(FY)` to represent that residue.
* Use `X` to indicate any residue.
* Use numbers to indicate a stretch of `X` residues.

# Examples
The best way to understand the syntax is through examples. For the following I will assume I have my protein sequences in a file titled Fasta.seq.
\
If I'm looking at my map and I see two large residues, a space of 8 residues and then two more large residues, I could search for that by running\
`python3 blobmapper.py -p '>>8>>' Fasta.seq`

If I see a tryptophan, then a space of 5 residues, then what is either F or Y, then 7 more residues, then another tryptophan, I can search for that by running\
`python3 blobmapper.py -p 'W5(FY)7W' Fasta.seq`

