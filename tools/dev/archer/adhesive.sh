#!/bin/sh

echo '#############################################################################'
echo '# adhesive containerized build starting'
echo '#############################################################################'

# PYTHONUSERSITE disables adding the .local into sys.path, so our $HOME mount
# doesn't screw up.

docker run -it \
    --rm \
    -v /tmp:/tmp \
    -v $HOME:$HOME \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v /etc/passwd:/etc/passwd:ro \
    -v /etc/group:/etc/group:ro \
    -e HOME=$HOME \
    -e PYTHONNOUSERSITE=1 \
    -w $(pwd) \
    -u $(id -u):$(id -g) \
    $(id -G | perl -pe 's/(\d+)/--group-add \1/g') \
    germaniumhq/adhesive:1.4.15 \
    adhesive $@

