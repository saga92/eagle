FROM ubuntu:14.04

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -y install openssh-server pwgen

RUN mkdir -p /var/run/sshd && \
    sed -i "s/UsePrivilegeSeparation.*/UsePrivilegeSeparation no/g" /etc/ssh/sshd_config && \
    sed -i "s/UsePAM.*/UsePAM no/g" /etc/ssh/sshd_config && \
    sed -i "s/PermitRootLogin.*/PermitRootLogin yes/g" /etc/ssh/sshd_config

RUN echo "root:root" | chpasswd

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]
