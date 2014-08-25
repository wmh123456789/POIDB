#!/usr/perl

use Encode;

open IN,"citys.txt";
open OUT,">citys.kml";

binmode IN, ":encoding(gbk)";
binmode OUT, ":encoding(utf8)";

my $i;


print OUT "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n";
print OUT "<kml xmlns=\"http://earth.google.com/kml/2.1\">\n";
print OUT "<Document>\n";
print OUT "<name>citys</name>\n";
print OUT "<open>1</open>\n";

$i=0;
my $firstprov;
my $firstreg;
$firstprov=1;
$firstreg=1;
while (<IN>)
{
	$i++;
	my $line;
	$line=$_;
	$line=substr($line,0,length($line)-1) if (substr($line,length($line)-1) eq "\n");
	my @ws;
	@ws=split(/\t/,$line);
	next if (@ws<6);
	if (substr($ws[0],0,1) eq "9" && substr($ws[0],4)=="00")
	{
		print OUT "  </Folder>\n" if (!$firstreg);
		print OUT "</Folder>\n" if (!$firstprov);
		print OUT "<Folder>\n";
		print OUT "  <name>".$ws[1]."</name>\n";
		$firstprov=0;
		$firstreg=1;
	}
	elsif (substr($ws[0],0,1) eq "9")
	{
		print OUT "  </Folder>\n" if (!$firstreg);
		print OUT "  <Folder>\n";
		print OUT "  <name>".$ws[1]."</name>\n";
		$firstreg=0;
	}
	elsif (substr($ws[0],2) eq "0000")
	{
		print OUT "  </Folder>\n" if (!$firstreg);
		print OUT "</Folder>\n" if (!$firstprov);
		print OUT "<Folder>\n";
		print OUT "  <name>".$ws[1]."</name>\n";
		$firstprov=0;
		$firstreg=1;
	}
	elsif (substr ($ws[0],4) eq "00")
	{
		print OUT "  </Folder>\n" if (!$firstreg);
		print OUT "  <Folder>\n";
		print OUT "  <name>".$ws[1]."</name>\n";
		$firstreg=0;
	}
	
	next if ($ws[3] eq "");
	print OUT "    <Placemark>\n";
	print OUT "      <name>".$ws[1]."</name>\n";
	print OUT "      <description>".$ws[0].$ws[2]."</description>\n";
	print OUT "      <Point>\n";
	print OUT "        <coordinates>".$ws[4].",".$ws[3].",0</coordinates>\n";
	print OUT "      </Point>\n";
	print OUT "      <Region>\n";
	print OUT "        <LatLonAltBox>\n";
	print OUT "          <north>".($ws[3]+0.5)."</north>\n";
	print OUT "          <south>".($ws[3]-0.5)."</south>\n";
	print OUT "          <east>".($ws[4]+0.5)."</east>\n";
	print OUT "          <west>".($ws[4]-0.5)."</west>\n";
	print OUT "          <minAltitude>0</minAltitude>\n";
	print OUT "          <maxAltitude>0</maxAltitude>\n";
	print OUT "        </LatLonAltBox>\n";
	print OUT "        <Lod>\n";
	my $lod;
	if (substr($ws[0],0,1) eq "9" && substr($ws[0],4)eq"01")
	{
		$lod=4;
	}
	elsif (substr($ws[0],0,1) eq "9" && substr($ws[0],4)ne"01")
	{
		$lod=64;
	}
	elsif (substr($ws[0],2) eq "0000")
	{
		$lod=4;
	}
	elsif (substr ($ws[0],2) eq "0100")
	{
		$lod=4;
	}
	elsif (substr ($ws[0],4) eq "00")
	{
		$lod=64;
	}
	else
	{
		$lod=256;
	}
	
	print OUT "          <minLodPixels>".$lod."</minLodPixels>\n";
	print OUT "          <maxLodPixels>100000000</maxLodPixels>\n";
	print OUT "          <minFadeExtent>0</minFadeExtent>\n";
	print OUT "          <maxFadeExtent>0</maxFadeExtent>\n";
	print OUT "        </Lod>\n";
	print OUT "      </Region>\n";
	print OUT "    </Placemark>\n";
}

print OUT "  </Folder>\n" if (!$firstreg);
print OUT "</Folder>\n" if (!$firstprov);

print OUT "</Document>\n";
print OUT "</kml>\n";


close IN;
close OUT;