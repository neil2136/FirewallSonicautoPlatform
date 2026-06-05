#!/usr/bin/perl
use Getopt::Long;
use strict;
use Net::SSH::Expect;

#set $ENV{'remote_server_ip'} in global_v_json.cfg
my $remote_server_ip = '192.0.1.22';
my $remote_server_username = 'root';
my $remote_server_passwd = 'password';
my $remote_file_path = "/root/iphelper";

my $interface = "eth0";
my $local_ip = "192.168.168.169";
my $local_broadcast_ip = "192.168.168.255";

my $TESTCASE_PATH = "/root/iphelper";

my $DstPort = 53;
my $SrcPort = 36646;

my $record_data = "/tmp/listening_port.txt";
my $child_output = "/tmp/child_output.txt";
my $file = "/tmp/ChildReady.txt";

my $result = GetOptions	(	"pd=i"		=> \$DstPort,
                        	"ps=i"		=> \$SrcPort,
                        	"is=s"		=> \$local_ip,
                        	"id=s"		=> \$local_broadcast_ip,
                        	"int=s"		=> \$interface,
                        	"server=s"	=> \$remote_server_ip,
                        	"user=s"	=> \$remote_server_username,
                        	"passwd=s"	=> \$remote_server_passwd,
						);

print "remote_server_ip is $remote_server_ip\n";

my $id = fork();
if(!$id)
{
	print "Child ID: $id\n";
	my $ssh = Net::SSH::Expect->new (
										host => "$remote_server_ip",
										password=> "$remote_server_passwd",
										user => "$remote_server_username",
										timeout => 10,
										raw_pty => 1,
									);

	my $login_output = $ssh->login();
	print "Child: login success and output is:\n{$login_output}\n";
	
	open FH,"> $file";
	print FH "Child ID: $id\n";
	print "Child: create file $file\n";
	close FH;

	my $log = $ssh->exec("perl $remote_file_path/receive.pl $DstPort $local_broadcast_ip");
	$ssh->close();
	
	open CHILD, "> $child_output";
	print CHILD "$log";	
	print "Child: finish\n";
	
}
else
{
	print "Parent ID: $id\n";
	system "netcat -u -l -p $SrcPort > $record_data &";
	print "Parent: wait for $file\n";
	
	my $mac = `ifconfig $interface`;
	if($mac =~ /HWaddr\s+([0-9a-f]{2}):([0-9a-f]{2}):([0-9a-f]{2}):([0-9a-f]{2}):([0-9a-f]{2}):([0-9a-f]{2})/i)
	{
		$mac = $1.$2.$3.$4.$5.$6;
		print "Parent: the mac address of $interface is $mac\n";
	}
	else
	{
		print "Parent: can not get Mac Address, ERROR!\n";
		#������
	}
	
	foreach (1 .. 32)
	{
		if(-s $file)
		{
			print "Parent: find child process login remote PC successfully\n";
			sleep 1;
			# system "rm -f $file";
			last;
		}
		else
		{
			print "Parent: wait $_ second(s)\n";
			sleep 1;
		}
		
		if($_ == 32)
		{
			print "Parent: can't find $file\n";
			#�������
		}
		
	}
	
	sleep 4;
	print "Parent: send a udp request\n";
	if($local_broadcast_ip =~ /\d+\.\d+\.\d+\.255/)
	{
		print "$TESTCASE_PATH/subbroadcast -i $interface -m $mac -s ${local_ip}.$SrcPort -d ${local_broadcast_ip}.$DstPort -p hello_shanghai_automation\n";
		my $send_udp = `$TESTCASE_PATH/subbroadcast -i $interface -m $mac -s ${local_ip}.$SrcPort -d ${local_broadcast_ip}.$DstPort -p hello_shanghai_automation`;
	}
	else
	{
		print "sendip -v -p ipv4 -is $local_ip -id $local_broadcast_ip -p udp -us $SrcPort -ud $DstPort $local_broadcast_ip -d hello_shanghai_automation\n";
		my $sendip = `sendip -v -p ipv4 -is $local_ip -id $local_broadcast_ip -p udp -us $SrcPort -ud $DstPort $local_broadcast_ip -d hello_shanghai_automation`;
	}
	
	sleep 6;
	my $pidof = `pidof netcat`;
	#print "get \$pidof is $pidof\n";
	#chomp $pidof;
	system "kill $pidof" if $pidof;
	
	foreach (1 .. 40)
	{
		if(-s $child_output)
		{
			sleep 2;
			open CHILD, "< $child_output";
			my @output = <CHILD>;
			close CHILD;
			print "Parent: find the file $child_output\nThe remote server's log is \n{@output}\n";
			# system "rm -f $child_output";
			last;
		}
		else
		{
			sleep 1;
			print "Parent: wait $_ second(s) for the child output file: $child_output\n";
		}
		
		if($_ == 40)
		{
			print "can not get the remote server's information\n";
			#�������
		}
	}
	
	sleep 2;
	open DATA, "< $record_data";
	my @content = <DATA>;
	close DATA;
	print "Parent: client PC received data is {@content}\n";
	# system "rm -f $record_data";
}
