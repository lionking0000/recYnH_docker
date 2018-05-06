FROM publicisworldwide/python-conda

# File Author / Maintainer
MAINTAINER Jae-Seong Yang <jae-seong.yang@crg.eu>

# Install R packages
#COPY deps.R /usr/local

#RUN Rscript /usr/local/deps.R

# Install cutadapt
#RUN pip install 'cutadapt==1.8.3'
RUN conda install -c bioconda cutadapt --yes
RUN conda install -c bioconda bowtie --yes
RUN conda install -c anaconda scipy --yes
RUN conda install -c bioconda blast --yes
RUN conda install -c r r --yes
RUN conda clean -a --yes

# Install recYnH
COPY src/* /usr/local/bin/

# Clean cache
RUN set -x; rm -rf /var/lib/apt/lists/*

# Shared mounting
VOLUME /share
VOLUME /src
