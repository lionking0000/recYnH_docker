dir=$(pwd -P)
#docker run -v /Users/jyang/Dropbox/Code/recYnH/share:/share -ti recynh /bin/bash
#echo "docker run -v /Users/jyang/Dropbox/Code/recYnH/share:/share -ti lionking0000/recynh:0.1 /bin/bash"
#docker run -v /Users/jyang/Dropbox/Code/recYnH/share:/share -ti lionking0000/recynh:0.1 /bin/bash
#docker run -v /Users/jyang/Downloads/recYnH/share:/share -ti lionking0000/recynh:0.1 /bin/bash

echo "docker run -v $dir:/src -v $dir/share:/share -ti lionking0000/recynh:0.1 /bin/bash"
docker run -v $dir:/src  -v $dir/share:/share -ti lionking0000/recynh:0.1 /bin/bash
