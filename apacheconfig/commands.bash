#! /bin/bash

sudo usermod –a -G “www-data” pi
cp apacheconfig/sysinfo.conf /etc/apache2/sites-available/sysinfo.conf

/usr/sbin/a2ensite sysinfo.conf
service apache2 reload