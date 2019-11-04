#!/bin/csh
mkdir eventfiles
./clasdis --trig 10000 --nmax 10000 --zpos -3.0 --zwidth 5 --raster 0 --w 3.92 20 --q 0.85 15
cat eventfiles/*.dat > lundFile.dat
setenv fname `basename eventfiles/*.dat`
gemc rga-fall2018.gcard -INPUT_GEN_FILE="LUND, lundFile.dat" -OUTPUT="evio, out.evio" -RUNNO=11 -USE_GUI=0 -N=10000;
$COATJAVA/bin/evio2hipo -r 11 -t -1.0 -s -1.0 -o output.hipo out.evio;
recon-util -i output.hipo -o cooked.hipo -c 2 -y /group/clas12/gemc/gcards/rga-fall2018.yaml;
$CLARA_HOME/plugins/clas12/bin/hipo-utils -filter -b "RUN*,MC*,REC*" -o skimmed.hipo cooked.hipo
