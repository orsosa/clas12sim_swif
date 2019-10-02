#!/usr/bin/env python
import glob
import os
from sys import argv
import subprocess
############## global setting ###########
outdir="/volatile/clas/claseg2/osoto/sim/hipo"
app="/home/osoto/clasdis-nocernlib/clasdis"
script="run_chain.csh"
gcard="/group/clas12/gemc/gcards/rga-fall2018.gcard"
WF="clasdis_sim"
DEBUG=False
#################################################
##### add job to workflow
def add_job(wf,c=0):
    global outdir, app, script
    jname = wf + "_" + str(c)
    cmd = "swif add-job -workflow " + wf + " -ram 2000mb -project clas12 -track simulation -disk 8000mb "
    cmd = cmd + " -name " + jname
    cmd = cmd + " -output cooked.hipo " + outdir + "/" + "cooked_" + str(c) + ".hipo"
    cmd = cmd + " -input " + app.split("/")[-1] + " file:" + app
    cmd = cmd + " -input " + gcard.split("/")[-1] + " file:" + gcard
    cmd = cmd + " -script " + script
    if DEBUG : print (cmd)
    subprocess.call(cmd,shell=True)

######### create workflow #####
def create_wf():
    global WF
    cmd="swif create " + WF
    if DEBUG : print (cmd)
    subprocess.call(cmd,shell=True)

#### run workflow ############
def run_wf():
    global WF
    cmd="swif run -workflow " + WF
    subprocess.check_call(cmd.split(" "))

######## main routine ####

def main():
    global WF
    Njobs = 2
    if (len(argv)>1):
        try:
            Njobs = int(argv[1])
        except ValueError:
            print ("!!!!!!!!!invalid Number of jobs. sending 2 instead.!!!!!")
            Njobs = 2
    print("sending " + str(Njobs) + " jobs")
    create_wf()
    c=0
    for k in range(Njobs):
        add_job(WF,c)
        c = c+1

if __name__=="__main__":
    main()
    run_wf()
