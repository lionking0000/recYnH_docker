#===================================
# run this script as following
#
# sh docker_merge_test.sh -m1 ../../share/output/example/S1_W.ppi.txt -m2 ../../share/output/example/S2_Q.ppi.txt
#
#===================================

dir=$(pwd)

echo "docker run -v $dir:/src  -v $dir/share:/share lionking0000/recynh:0.1 recYnH.py merge $*"
docker run -v $dir:/src  -v $dir/share:/share lionking0000/recynh:0.1 recYnH.py merge $*


#cd ./src
#python ./recYnH.py merge -m1 ../../share/output/test/recYnH.ppi.txt -m2 ../../share/output/test/recYnH.ppi.txt
