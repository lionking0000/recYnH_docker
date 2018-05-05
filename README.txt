[What is recYnH?]

This program is taking recYnH sequencing files and generating recYnH interaction score matrix to correponding genes.

We assumed that the sequencing format is the same as we described in Nature Communication 2018 Paper.

# After setting proper parameter in recYnH.py file
# User can run the program as following command

# python recYnH.py -i [Input fasta file] -f1 [Input fastq file1] -f2 [Input fastq file2] -o [Output folder]

sh Y2H_Blastn.sh 2017-11-17_MiSeq S1_WD_R1 S1_WD_R2 ../data/A463-MGj69.RBP-MAP.-150 S1_W > qjobs/qjob_Sebastian_2017-11-17_MiSeq_S1_W1.sh

# Typical output

[ Starting recY2H Analysis ]
[ Read No-selection Sequence File ] ./data/XXXX.fastq.gz
[ Read Selection Sequence File ] ./data/YYYY.fastq.gz
[ Calculating recY2H Scores ]
[ Finishing recY2H Analysis ]


# It will gives recY2H Scores for all the sequences


[Output Files]


# How to use Docker

[Build image]

docker build -t recynh .

or

sh docker_build.sh

[Run image]

docker run -d -v ~/myshared:/share --name myynh recynh tail -f /dev/null

~/myshared is a shared volume used for convenience for placing input and output files

The command above keeps container running under the name myynh


# running interactive mode
docker run -v /Users/jyang/Dropbox/Code/recYnH/share:/share -ti recynh /bin/bash



#Mounting with volume
#docker run -v /home/toniher/tmp/ELMSeq/data:/input -ti elmseq /bin/bash
#Supposing a config file:
#docker run -v /home/toniher/tmp/ELMSeq/data:/input -v /home/toniher/myconfig.json:/etc/myconfig.json -ti elmseq /bin/bash


[Excute command]

docker exec myynh rec-Ynh.py -i /share/reads/SRR493366.fastq -o /share/out/test


# References & Related information

https://github.com/toniher/ELMSeq/blob/master/Dockerfile

