#===================================
# run this script as following
#
# sh docker_align_test.sh -i1 ../share/db/A463-MGj69.RBP-MAP.-150.fa -f1 /fastq/2017-11-17_MiSeq/23580-69-WD_S1_L001_R1_001.fastq.gz -f2 /fastq/2017-11-17_MiSeq/23580-69-WD_S1_L001_R2_001.fastq.gz -o ../share/output/2017-11-17_MiSeq -n S1_WD
# sh docker_align_test.sh -i1 ../share/db/A463-MGj69.RBP-MAP.-150.fa -f1 /fastq/2017-11-17_MiSeq/S1_WD_R1.fastq.gz -f2 /fastq/2017-11-17_MiSeq/S1_WD_R2.fastq.gz -o ../share/output/2017-11-17_MiSeq -n S1_WD
# 
# sh docker_align_test.sh -i1 ../share/db/A463-MGj69.RBP-MAP.-150.fa -f1 ../share/fastq/2017-11-17_MiSeq/S1_WD_R1.fastq.gz -f2 ../share/fastq//2017-11-17_MiSeq/S1_WD_R2.fastq.gz -o ../share/output/2017-11-17_MiSeq -n S1_WD
# sh docker_align_test.sh -i1 ../share/db/A463-MGj69.RBP-MAP.-150.fa -f1 ../share/fastq/2017-11-17_MiSeq/S2_QD_R1.fastq.gz -f2 ../share/fastq//2017-11-17_MiSeq/S2_QD_R2.fastq.gz -o ../share/output/2017-11-17_MiSeq2 -n S2_QD2
#
#===================================


dir=$(pwd)


echo "docker run -v $dir:/src  -v $dir/share:/share lionking0000/recynh:0.1 recYnH.py align $*"
docker run -a stdout -v $dir:/src  -v $dir/share:/share -v /Volumes/users/smaurer/sequencing_data/Mireia_Garriga:/fastq lionking0000/recynh:0.1 recYnH.py align $*


