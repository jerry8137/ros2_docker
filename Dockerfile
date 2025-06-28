FROM osrf/ros:jazzy-desktop-full

RUN apt-get update && apt-get install -y \
    wget \
    bzip2 \
    ca-certificates \
    sudo \
    vim \
    && rm -rf /var/lib/apt/lists/*

# setup non-root user
ARG UNAME=user
ARG UID=1000
ARG GID=1000
RUN groupadd -g $GID -o $UNAME
RUN useradd -m -u $UID -g $GID -s /bin/bash $UNAME
RUN echo "user ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
USER $UNAME
CMD ["/bin/bash"]
