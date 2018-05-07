dir=$(pwd)

echo "docker run -v $dir:/src -v $dir/share:/share -ti lionking0000/recynh:0.1 /bin/bash"
docker run -v $dir:/src  -v $dir/share:/share -ti lionking0000/recynh:0.1 /bin/bash
