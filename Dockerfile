FROM rocker/r-ver:3.3.1

# File Author / Maintainer
MAINTAINER Jae-Seong Yang <jae-seong.yang@crg.eu>

# Install R packages
#COPY deps.R /usr/local
RUN echo "r <- getOption('repos'); r['CRAN'] <- 'http://cran.us.r-project.org'; options(repos = r);" > ~/.Rprofile
#RUN Rscript -e "source('http://bioconductor.org/biocLite.R');biocLite(c('limma','GSA','Biobase','edgeR','locfit','RCy3'))"
#RUN Rscript -e "install.packages(c('pheatmap','RColorBrewer','gProfileR','RJSONIO','httr','ggplot2'))"
RUN Rscript -e "install.packages(c('pheatmap','RColorBrewer'))"
RUN Rscript -e "install.packages(c('gtools','reshape2'))"
RUN Rscript -e "install.packages(c('psych','clipr'))"
RUN Rscript -e "install.packages(c('swfscMisc','PerformanceAnalytics'))"
RUN Rscript -e "install.packages(c('mixtools','pROC'))"
RUN Rscript -e "install.packages(c('outliers','readxl'))"
RUN Rscript -e "install.packages(c('d3heatmap','matrixStats'))"
#RUN Rscript /usr/local/deps.R

# Install external dependencies 
RUN apt-get update -qq && apt-get install -y --no-install-recommends python python-numpy python-scipy python-pip libpython2.7-dev bowtie
RUN apt-get install -y --no-install-recommends ncbi-blast+

# Install cutadapt
RUN pip install 'cutadapt==1.8.3'

# Install recYnH
COPY src/* /usr/local/bin/

# Clean cache
RUN apt-get clean
RUN set -x; rm -rf /var/lib/apt/lists/*
RUN apt-get clean ; apt-get remove --yes --purge build-essential

# Shared mounting
VOLUME /share
VOLUME /fastq
VOLUME /src






