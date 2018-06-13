rec-YnH
==========

Table of Contents:

- [Summary](#summary)
- [Requirements](#requirements)
- [Installation](#installation)
	- [rec-YnH](#vast-tools-1)
- [Usage](#usage)
	- [Help](#help)
	- [Quick Usage](#quick-usage)
	- [Alignment](#alignment)
	- [Merging Outputs](#merging-outputs)
	- [Strand-specific RNAseq data](#strand-specific-rnaseq-data)
	- [Combining Results](#combining-results)
	- [Comparing PSIs Between Samples](#comparing-psis-between-samples)
	- [Differential Splicing Analysis](#differential-splicing-analysis)
	- [Plotting](#plotting)
	- [Simplifying Combine Table](#simplifying-combine-table)
- [Issues](#issues)
- [Contributions](#contributions)
- [Citation](#citation)
- [References](#references)
	
Summary
-------
This program is taking recYnH sequencing files and generating recYnH interaction score matrix to correponding genes.

Requirements
------------

rec-YnH requires the following software:
 * python 2.7 or higher, with the following packages installed (see Installation Section):
   * scipy, https://pypi.org/project/scipy/
 * cutadapt, http://cutadapt.readthedocs.io/en/stable/installation.html
 * blast+ 2.6.0 or higher, http://ftp.ncbi.nlm.nih.gov/blast/executables/blast+
 
 * R 3.1 or higher, with the following packages installed (see Installation Section):
   * optparse
   * RColorBrewer
   * reshape2
   * ggplot2 >= v2.0
   * MASS
   * devtools
   * [psiplot](https://github.com/kcha/psiplot)
 
 * bowtie 1.0.0 (Langmead et al., 2009), http://bowtie-bio.sourceforge.net/index.shtml
 
Installation
------------

~~~~
> git clone https://github.com/lionking0000/recYnH.git
~~~~

Alignment
------------

python recYnH.py -i1 ../share/db/A463-MGj69.RBP-MAP.-150.fa -f1 ../share/fastq/2017-11-17_MiSeq/S1_WD_R1.fastq.gz -f2 ../share/fastq//2017-11-17_MiSeq/S1_WD_R2.fastq.gz -o ../share/output/2017-11-17_MiSeq -n S1_WD

python recYnH.py -i1 ../share/db/A463-MGj69.RBP-MAP.-150.fa -f1 ../share/fastq/2017-11-17_MiSeq/S2_QD_R1.fastq.gz -f2 ../share/fastq//2017-11-17_MiSeq/S2_QD_R2.fastq.gz -o ../share/output/2017-11-17_MiSeq2 -n S2_QD2
