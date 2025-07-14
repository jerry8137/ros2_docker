#!/usr/bin/env bash

# xhost +SI:localuser:$(id -un)
nix-shell -p xorg.xhost --run "xhost +local:"

docker run -it --rm \
    --env="DISPLAY" \
    --env="QT_QPA_PLATFORM=xcb" \
    --env="QT_X11_NO_MITSHM=1" \
    --env="WAYLAND_DISPLAY=${WAYLAND_DISPLAY}" \
    --env="XDG_RUNTIME_DIR=/tmp":rw \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --volume="$XDG_RUNTIME_DIR/$WAYLAND_DISPLAY:/tmp/$WAYLAND_DISPLAY:rw" \
    --ipc=host \
    --privileged \
    jros:foxy bash
