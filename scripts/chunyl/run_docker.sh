SCRIPTPATH="/data/chunyl"
IMAGE=pytorch/pytorch:2.0.1-cuda11.7-cudnn8-devel

docker run \
--runtime=nvidia \
-it --rm \
--net host \
--volume $SCRIPTPATH:/workspace \
--interactive --tty $IMAGE /bin/bash