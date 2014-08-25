#!/usr/perl

my %citys;

open IN1,"citys.txt";

my $i;
$i=0;
while(<IN1>)
{
	$i++;
	my $line;
	$line=$_;
	$line=substr($line,0,length($line)-1) if (substr($line,length($line)-1) eq "\n");
	my @ws;
	@ws=split(/\t/,$line);
	next if (@ws<6);
	@{$citys{$ws[0]}}=@ws;	
#	print @{$citys{$ws[0]}};
}

close IN1;

open IN2,"citys.txt.upd";

$i=0;
while(<IN2>)
{
	$i++;
	my $line;
	$line=$_;
	$line=substr($line,0,length($line)-1) if (substr($line,length($line)-1) eq "\n");
	my @ws;
	@ws=split(/\t/,$line);
	next if (@ws<6);
	$citys{$ws[0]}[3]=int($ws[3]*1e6)/1e6;
	$citys{$ws[0]}[4]=int($ws[4]*1e6)/1e6;
}

close IN2;


open OUT,">citys.txt.new";

my $code;

foreach $code (sort keys %citys)
{
  my @ws;
	@ws=@{$citys{$code}};
	print OUT $code."\t".$ws[1]."\t".$ws[2]."\t".$ws[3]."\t".$ws[4]."\t".$ws[5]."\n";
	#print $code;
  #print join(' ',@{$citys{$code}})."\n";
}

close OUT;

