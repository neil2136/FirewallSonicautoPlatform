#!/usr/bin/perl
print "chdir '/root/iphelper/'\n";
chdir "/root/iphelper/" or die "Cannot chdir to /root/iphelper/:$!";
sleep 1;

$cmd = "tar zxvf netcat-0.7.1.tar.gz";
print "$cmd\n";
system "$cmd";
sleep 1;

print "chdir '/root/iphelper/netcat-0.7.1'\n";
chdir "/root/iphelper/netcat-0.7.1/" or die "Cannot chdir to /root/iphelper/netcat-0.7.1:$!";
sleep 1;

$cmd = "./configure";
print "$cmd\n";
system "$cmd";
sleep 1;

$cmd = "make";
print "$cmd\n";
system "$cmd";
sleep 1;

$cmd = "make install ";
print "$cmd\n";
system "$cmd";
sleep 1;
