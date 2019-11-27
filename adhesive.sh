#!/bin/sh

echo '#############################################################################'
echo '# adhesive containerized build starting'
echo '#############################################################################'

docker run -it \
    --rm \
    -v /tmp:/tmp \
    -v $HOME:$HOME \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v /etc/passwd:/etc/passwd:ro \
    -v /etc/group:/etc/group:ro \
    -e HOME=$HOME \
    -w $(pwd) \
    -u $(id -u):$(id -g) \
    $(id -G | perl -pe 's/(\d+)/--group-add \1/g') \
    germaniumhq/adhesive:0.12.0 \
    adhesive $@

