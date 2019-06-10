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

##Pattern Syntax
