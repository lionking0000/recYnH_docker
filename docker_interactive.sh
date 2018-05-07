dir=$(pwd)

echo "docker run -v $dir:/src -v $dir/share:/share -ti lionking0000/recynh:0.1 /bin/bash"
#docker run -v $dir:/src  -v $dir/share:/share -ti lionking0000/recynh:0.1 /bin/bash

echo "docker run -a stdout -v $dir:/src  -v $dir/share:/share -v /Volumes/users/smaurer/sequencing_data/Mireia_Garriga:/fastq -ti lionking0000/recynh:0.1 /bin/bash"
docker run -a stdout -v $dir:/src  -v $dir/share:/share -v /Volumes/users/smaurer/sequencing_data/Mireia_Garriga:/fastq -ti lionking0000/recynh:0.1 /bin/bash 

# python ./recYnH.py align -i1 ../share/db/A463-MGj69.RBP-MAP.-150.fa -f1 /fastq/2017-11-17_MiSeq/S1_WD_R1.fastq.gz -f2 /fastq/2017-11-17_MiSeq/S1_WD_R2.fastq.gz -o ../share/output/2017-11-17_MiSeq -n S1_WD