# This Python script Merges 2 pairs by adding NNNNNNs
# This script uses ideas for parsing FASTQ from here http://news.open-bio.org/news/2009/12/interleaving-paired-fastq-files-with-biopython/
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import sys
#import itertools

ForwardName = str(sys.argv[1])  # forward reads file
ReverseName = str(sys.argv[2])  # reverse reads file
mergedName = str(sys.argv[3])  # output file
print ("Forward Name is " + ForwardName)
print ("Reverse Name is " + ReverseName)
print ("Merged output is " + mergedName)

insert = "N" * 300  # assumed insert size TODO pass as argument Crazy TODO add random DNA instead of NNNN


def merge(iter1, iter2):
    for (forward, reverse) in zip(iter1, iter2):
        assert forward.id == reverse.id
    allSeq = str(forward.seq + insert + reverse.seq.reverse_complement())
    seqfasta = SeqRecord(Seq(allSeq), id=forward.id) # Choosing to go with forward ID as the fasta header for, might parse it out in the future.
    yield seqfasta


records_f = SeqIO.parse(open(ForwardName,"rU"), 'fastq') # Input format can be changed here TODO add argument
records_r = SeqIO.parse(open(ReverseName,"rU"), 'fastq') # Input format can be changed here TODO add argument

handle = open(mergedName, "w")
count = SeqIO.write(merge(records_f, records_r), handle, 'fasta') #Fastq won't work because the quality data is lost
handle.close()
print ("Wrote %i entries to  %s" % (count, mergedName))
