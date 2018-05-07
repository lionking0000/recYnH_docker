
dir=$(pwd)

echo "docker run -d -v /Users/jyang/Dropbox/Code/recYnH/share:/share --name myynh lionking0000/recynh:0.1 tail -f /dev/null"
#docker run -d -v /Users/jyang/Dropbox/Code/recYnH/share:/share --name myynh lionking0000/recynh:0.1 tail -f /dev/null
docker run -d -v $dir:/src  -v $dir/share:/share -v /Volumes/users/smaurer/sequencing_data/Mireia_Garriga:/fastq --name myynh lionking0000/recynh:0.1 tail -f /dev/null

# [ running with this daemon ]
#echo "docker exec myynh Y2H_Blastn.sh 2017-11-17_MiSeq S1_WD_R1.10000 S1_WD_R2.10000 ./db/A463-MGj69.RBP-MAP.-150 S1_W"
#docker exec myynh Y2H_Blastn.sh 2017-11-17_MiSeq S1_WD_R1.10000 S1_WD_R2.10000 ./db/A463-MGj69.RBP-MAP.-150 S1_W

#docker exec myynh /bin/bash -c "cd /src/src/; python ./recYnH.py align -i1 ../share/db/A463-MGj69.RBP-MAP.-150.fa -f1 /fastq/2017-11-17_MiSeq/23580-69-WD_S1_L001_R1_001.fastq.gz -f2 /fastq/2017-11-17_MiSeq/23580-69-WD_S1_L001_R2_001.fastq.gz -o ../share/output/2017-11-17_MiSeq -n S1_WD"

