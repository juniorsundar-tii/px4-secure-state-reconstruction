FROM ros:humble

# Set noninteractive mode for APT to avoid prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install prerequisites
RUN apt update && apt install -y \
        wget \
        curl \
        pip \
        lsb-release \
        gnupg \
        software-properties-common \
        && rm -rf /var/lib/apt/lists/*

RUN apt update && apt install -y \
        iproute2 \
        python3-colcon-common-extensions \
        python3-pip \
        ros-humble-plotjuggler-ros \
        libxcb-xinerama0 \
        && rm -rf /var/lib/apt/lists/*

RUN sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list'

RUN wget https://packages.osrfoundation.org/gazebo.key -O - | apt-key add -

RUN apt-get update && apt-get install -y \
        libgz-transport13-dev \
        && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install setuptools==58.2.0 numpy==1.21.5 control cvxopt jinja2

ARG USERNAME=ssr
# On Linux, replace with your actual UID, GID if not the default 1000
ARG USER_UID=1100
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
        && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME -s /bin/bash \
        && mkdir -p /home/$USERNAME/.vscode-server /home/$USERNAME/.vscode-server-insiders \
        && chown ${USER_UID}:${USER_GID} /home/$USERNAME/.vscode-server* \
        # && mkdir -p /etc/sudoers.d/$USERNAME \
        && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
        && chmod 0440 /etc/sudoers.d/$USERNAME

USER $USERNAME

WORKDIR /workspace/px4-secure-state-reconstruction
