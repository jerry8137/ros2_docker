FROM ubuntu:focal

RUN apt-get update && apt-get install -y \
  wget \
  bzip2 \
  ca-certificates \
  sudo \
  vim \
  libglu1-mesa \
  mesa-utils \
  software-properties-common \
  curl \
  locales \
  && rm -rf /var/lib/apt/lists/*
RUN locale-gen en_US en_US.UTF-8 && \
  update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
ENV LANG=en_US.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

RUN add-apt-repository universe
RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
RUN apt-get update && apt-get install -y --no-install-recommends \
  ros-foxy-desktop \
  python3-argcomplete
RUN apt-get install -y ros-dev-tools

# setup non-root user
ARG UNAME=user
ARG UID=1000
ARG GID=1000
RUN groupadd -g $GID -o $UNAME
RUN useradd -m -u $UID -g $GID -s /bin/bash $UNAME
RUN echo "$UNAME ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
RUN echo "source /opt/ros/foxy/setup.bash" >> /home/$UNAME/.bashrc

USER $UNAME
CMD ["/bin/bash"]
