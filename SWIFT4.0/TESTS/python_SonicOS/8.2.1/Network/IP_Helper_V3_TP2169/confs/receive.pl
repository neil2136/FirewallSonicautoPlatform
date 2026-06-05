#!/usr/bin/perl

my $server_ip = "13.0.0.5";
my $server_subnet = "13.0.0.255";
my $interface = "eth0"; #server's NIC

my $SrcPort = $ARGV[0];

my $record = "/tmp/record.txt";

system "tcpdump -i $interface -A -nn -c 1 udp port $SrcPort and dst host \\\( $server_ip or $ARGV[1] or $server_subnet\\\) > $record &";
sleep 10;

open DATA, "< $record";
my @contents = <DATA>;
my $content = join "", @contents;
close DATA;
print "server: the tcpdump's content is:\n{$content}\n";
#if($content =~ /IP 13.0.0.3.(\d+)/)
if($content =~ /IP ((?:\d{1,3})\.(?:\d{1,3})\.(?:\d{1,3})\.(?:\d{1,3}))\.(\d+)/)
{
	#if($1 eq "13.0.0.3")
	if($1 eq "13.0.0.168" || $1 eq "192.168.168.169")
	{
		print "Server: get a unicast, it's from $1. Send a reply\n";
		print "sendip -v -p ipv4 -is $server_ip -id $1 -p udp -us $SrcPort -ud $2 $1 -d shanghai_automation_are_the_best\n";
		system "sendip -v -p ipv4 -is $server_ip -id $1 -p udp -us $SrcPort -ud $2 $1 -d shanghai_automation_are_the_best";
	}
	else
	{
		print "receive a multicast\n";
	}
}
else
{
	print "can not get dst port\n";
}

my $pidof = `pidof tcpdump`;
chomp $pidof;
#print "Server: tcpdump's pid is $pidof\n";
system "kill $pidof" if $pidof;
# system "rm -f $record";
