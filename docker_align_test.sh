dir=$(pwd)
#cd ./src
#python ./recYnH.py align -i1 ../share/db/A463-MGj69.RBP-MAP.-150.fa -f1 ../share/fastq/S1_WD_R1.10000.fastq.gz -f2 ../share/fastq/S1_WD_R2.10000.fastq.gz -o ../share/output/test

#echo "docker run -v $dir:/src -v $dir/share:/share -ti lionking0000/recynh:0.1 /bin/bash"
#docker run -v $dir:/src  -v $dir/share:/share -ti lionking0000/recynh:0.1 /bin/bash
#echo "docker run -v $dir:/src  -v $dir/share:/share -ti lionking0000/recynh:0.1 /bin/bash -c 'cd /src/src/; python ./recYnH.py align -i1 ../share/db/A463-MGj69.RBP-MAP.-150.fa -f1 ../share/fastq/S1_WD_R1.10000.fastq.gz -f2 ../share/fastq/S1_WD_R2.10000.fastq.gz -o ../share/output/test'"
#docker run -v $dir:/src  -v $dir/share:/share lionking0000/recynh:0.1 /bin/bash -c "cd /src/src/; python ./recYnH.py align -i1 ../share/db/A463-MGj69.RBP-MAP.-150.fa -f1 ../share/fastq/S1_WD_R1.10000.fastq.gz -f2 ../share/fastq/S1_WD_R2.10000.fastq.gz -o ../share/output/test"


echo "docker run -v $dir:/src  -v $dir/share:/share lionking0000/recynh:0.1 /bin/bash -c 'cd /src/src/; python ./recYnH.py align $*'"
docker run -v $dir:/src  -v $dir/share:/share lionking0000/recynh:0.1 /bin/bash -c "cd /src/src/; python ./recYnH.py align $*"
