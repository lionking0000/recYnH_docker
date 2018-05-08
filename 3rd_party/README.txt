blastn and makeblastdb files were downloaded from ncbi ftp as following command and then extracted.

wget ftp://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.6.0/ncbi-blast-2.6.0+-x64-linux.tar.gz

We initially used "RUN apt-get install -y --no-install-recommends ncbi-blast+" command to install blastn but it seems that it leaks memory so we changed to use this way.
