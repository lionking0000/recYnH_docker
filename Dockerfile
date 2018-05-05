FROM rocker/r-ver:3.3.1
#FROM biocorecrg/debian-perlbrew-pyenv

# File Author / Maintainer
MAINTAINER Jae-Seong Yang <jae-seong.yang@crg.eu>

ARG BOWTIE_VERSION=1.2.1.1

#ARG DEBIAN_FRONTEND=noninteractive

# Install external dependencies 
RUN apt-get update -qq && apt-get install -y --no-install-recommends apt-utils python curl libcurl4-openssl-dev libssl-dev libsqlite3-dev libxml2-dev qpdf git python-pip libpython2.7-dev 

# Install bowtie 
RUN cd /usr/local; curl --fail --silent --show-error --location --remote-name https://github.com/BenLangmead/bowtie/releases/download/v$BOWTIE_VERSION/bowtie-${BOWTIE_VERSION}-linux-x86_64.zip
RUN cd /usr/local; unzip -d /usr/local bowtie-${BOWTIE_VERSION}-linux-x86_64.zip
RUN cd /usr/local; rm bowtie-${BOWTIE_VERSION}-linux-x86_64.zip

# Let's put in PATH
RUN cd /usr/local/bin; ln -s ../bowtie-${BOWTIE_VERSION}/bowtie* .


# Install R packages
COPY deps.R /usr/local

RUN Rscript /usr/local/deps.R

# Install pip and cutadapt required libraries
#RUN apt-get install --yes \
#        python-pip \
#        libpython2.7-dev


# Install cutadapt
RUN pip install 'cutadapt==1.8.3'



# Install recYnH
COPY src/* /usr/local/bin/

#RUN cd /usr/local; curl --fail --silent --show-error --location --remote-name https://github.com/vastgroup/vast-tools/archive/v${VASTTOOLS_VERSION}.tar.gz
#RUN cd /usr/local; tar zxf v${VASTTOOLS_VERSION}.tar.gz
#RUN cd /usr/local; rm v${VASTTOOLS_VERSION}.tar.gz
#VOLUME /VASTDB
#RUN cd /usr/local/vast-tools-${VASTTOOLS_VERSION}; ln -s /VASTDB .
#RUN cd /usr/local/vast-tools-${VASTTOOLS_VERSION}; ./install.R

# Let's put in PATH
#RUN cd /usr/local/bin; ln -s ../vast-tools-${VASTTOOLS_VERSION}/vast-tools .

# Clean cache
RUN apt-get clean
RUN apt-get remove --yes --purge build-essential
RUN set -x; rm -rf /var/lib/apt/lists/*

# Shared mounting
VOLUME /share

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8