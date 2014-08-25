#!/usr/perl

use Encode;

open IN,"citys.kml";
open OUT,">citys.txt.upd";

binmode OUT, ":encoding(gbk)";
binmode IN, ":encoding(utf8)";

my $i;

my ($inpm,$inpt);
my ($name,$desc,$lat,$lon);

$inpm=0;
$inpt=0;

$i=0;
while (<IN>)
{
	$i++;
	my $line;
	$line=$_;
	next if ($i<5);
	$line=substr($line,0,length($line)-1) if (substr($line,length($line)-1) eq "\n");
	
	my $p;
	$p=0;
	$p++ while ($p<length($line) && (substr($line,$p,1) eq ' '||substr($line,$p,1) eq "\t"));
	$line=substr($line,$p);
	
	if ($line eq "<Placemark>")
	{
		$inpm=1;
		$desc="";
	}
	elsif ($inpm && $line eq "<Point>")
	{
		$inpt=1;
	}
	elsif ($inpt && $line eq "</Point>")
	{
		$inpt=0;
	}
	elsif ($inpm && $line eq "</Placemark>")
	{
		$inpm=0;
		if (length($desc)>6)
		{
			print OUT substr($desc,0,6)."\t".$name."\t".substr($desc,6)."\t".$lat."\t".$lon."\t".(-5000)."\n";
	  }
	}
	elsif ($inpm && substr($line,0,6) eq "<name>" && substr($line,length($line)-7,7) eq "</name>")
	{
		$name=substr($line,6,length($line)-7-6);
#		print $name."\n";
	}
	elsif ($inpm && substr($line,0,13) eq "<description>" && substr($line,length($line)-14,14) eq "</description>")
	{
		$desc=substr($line,13,length($line)-14-13);
	}
	elsif ($inpt && substr($line,0,13) eq "<coordinates>" && substr($line,length($line)-14,14) eq "</coordinates>")
	{
		my $str;
		$str=substr($line,13,length($line)-14-13);
		($lon,$lat)=split(/,/,$str);
	}

}


close IN;
close OUT;