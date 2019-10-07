#!/usr/bin/env python
import glob
import os
from sys import argv
import subprocess
import shlex
from subprocess import Popen, PIPE
from time import sleep

############## global setting ###########
outdir=""
outdir_temp="/volatile/clas/claseg2/osoto/sim/hipo/H500"
app="/home/osoto/clasdis-nocernlib/clasdis"
script="run_chain.csh"
gcard="/group/clas12/gemc/gcards/rga-fall2018.gcard"
WF="clas12sim_cont"
curr_status_file = "/home/osoto/sim_status.txt"
MAXJOBS = 100
DEBUG=False
#################################################
##### add job to workflow
def add_job(wf,c=0):
    global outdir, app, script
    jname = wf + "_" + str(c)
    cmd = "swif add-job -workflow " + wf + " -ram 2000mb -project clas12 -track simulation -disk 8000mb "
    cmd = cmd + " -name " + jname
    cmd = cmd + " -output skimmed.hipo " + outdir + "/" + "skimmed_" + str(c) + ".hipo"
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

#### check running jobs ############
def check_wf():
    global WF
    states = []
    problems = []
    jobs = []
    cmd='swif status "' + WF +  '" -jobs' 
    ret = Popen(shlex.split(cmd),stdout=PIPE)
    out,err = ret.communicate()
    out = out.strip()
    for l in out.split('\n'):
        if "id" in l.split():
            jobid = l.split()[-1]
            if jobid not in jobs:
                jobs.append(jobid)
        if "auger_current_state" in l.split():
            states.append(l.split()[-1])
        if "problem" in l.split():
            problems.append(l.split()[-1])

    act = states.count('ACTIVE')
    pend = states.count('PENDING')
    succ = states.count('DONE')
    fail = len(problems)
    total = len(jobs)
    return (act,pend,succ,fail,total)

######## main routine ####

def main():
    global WF, outdir, outdir_temp, MAXJOBS
    create_wf()
    run_wf()
    ret = Popen(shlex.split("cat " + curr_status_file),stdout=PIPE)
    out, err = ret.communicate()

    bunch =  int(out.strip().split('\n')[-1].split('/')[0])
    job_i =  int(out.strip().split('\n')[-1].split('/')[1])
    outdir = outdir_temp + "_" + str(bunch)
    cmd = "mkdir -p " + outdir
    print cmd
    subprocess.call(cmd,shell=True)

    while True:
        if job_i==500:
            bunch += 1
            job_i = 0
            outdir = outdir_temp + "_" + str(bunch)
            cmd = "mkdir -p " + outdir
            print cmd
            subprocess.call(cmd,shell=True)


        act,pend,succ,fail,total = check_wf()

        print 'T / A / P / C / F'
        print str(total) + ' / ' + str(act) + ' / ' + str(pend) + ' / ' + str(succ) + ' / ' + str(fail)
        
        add_job(WF,job_i)
        while (total - succ - fail) > MAXJOBS:
            sleep(10)
            act,pend,succ,fail,total = check_wf()
            
        job_i +=1
        fout = open(curr_status_file,"w")
        fout.write("Bunch / job_i\n")
        fout.write(str(bunch) + " / " + str(job_i))
        fout.close()
        sleep(1)
        
    
if __name__=="__main__":
    main()
