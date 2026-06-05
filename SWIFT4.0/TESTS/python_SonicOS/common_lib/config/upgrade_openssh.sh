#!/usr/bin/env bash
mv /etc/ssh /etc/ssh.bak
mv /usr/bin/ssh /usr/bin/ssh.bak
mv /usr/sbin/sshd /usr/sbin/sshd.bak
yum -y remove openssh
cp /logs/wgu/openssh-7.4p1.tar.gz /tmp/
cd /tmp/
tar -zxvf openssh-7.4p1.tar.gz 
cd /tmp/openssh-7.4p1
./configure --prefix=/usr --sysconfdir=/etc/ssh --with-pam --with-zlib --with-ssl-dir=/usr/local/ssl --with-md5-passwords
make
make install
cp -f /logs/wgu/sshd_config /etc/ssh/sshd_config
cp /tmp/openssh-7.4p1/contrib/redhat/sshd.init /etc/init.d/sshd
chkconfig --add sshd
service sshd start
exit 0
