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
- [Combine output format](#combine-output-format)
- [Investigating event-level conservation](#investigating-event-level-conservation)
- [Interconnection with VastDB web](#interconnection-with-vastdb-web)
- [Interconnection with Matt](#interconnection-with-matt)
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
 * python 2.7 or higher
   * scipy
 * bowtie 1.0.0 (Langmead et al., 2009), http://bowtie-bio.sourceforge.net/index.shtml
 * cutadapt 
 * R 3.1 or higher, with the following packages installed (see Installation Section):
   * optparse
   * RColorBrewer
   * reshape2
   * ggplot2 >= v2.0
   * MASS
   * devtools
   * [psiplot](https://github.com/kcha/psiplot)
 * Perl 5.10.1 or higher
 * GNU coreutils `sort` (all versions)
 * blastn
 
Installation
------------

~~~~
> git clone https://github.com/lionking0000/recYnH.git
~~~~
