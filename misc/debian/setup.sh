#!/bin/sh
# Intended for Ubuntu 18.0.4 local OS to prep dev env
apt-get update
apt-get -y install wget libaio1 alien
wget http://yum.oracle.com/repo/OracleLinux/OL7/oracle/instantclient/x86_64/getPackage/oracle-instantclient18.3-basic-18.3.0.0.0-2.x86_64.rpm
wget http://yum.oracle.com/repo/OracleLinux/OL7/oracle/instantclient/x86_64/getPackage/oracle-instantclient18.3-sqlplus-18.3.0.0.0-2.x86_64.rpm
alien -d oracle-instantclient18.3-basic-18.3.0.0.0-2.x86_64.rpm
alien -d oracle-instantclient18.3-sqlplus-18.3.0.0.0-2.x86_64.rpm
rm *.rpm
dpkg -i oracle-instantclient18.3-basic_18.3.0.0.0-3_amd64.deb
dpkg -i oracle-instantclient18.3-sqlplus_18.3.0.0.0-3_amd64.deb
rm *.deb
sh -c "echo /usr/lib/oracle/18.3/client64/lib > /etc/ld.so.conf.d/oracle-instantclient.conf"
ldconfig
