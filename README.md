# Intro
python script for running simulations jobs on jlab farm.

# Requirement.
- Load clas12 packages in environment.
  - e.g. add to your ~/.cshrc :
  ```
  source /group/clas12/packages/setup.csh
  module load clas12/pro
  ```
- have CLASDIS_PDF environment set.
  - e.g. add to your ~/.cshrc :
  ```
  setenv  CLASDIS_PDF "/home/osoto/clasdis-nocernlib/pdf"
  ``` 

# Running one bunch.
`./make_swif_sim.py N`
This will create a swif workflow named `clasdis`, add N jobs to it and run it.

Each job consist of 10000 events. The result is a hipo file named cooked_n.hipo, n from 0 to N.

**!!!Change outdir in the header of the python script.!!!!**
# Running continuosly
`./keepN.py`
This will keep 100 jobs in the farm (queue + active = 100). You can change this number in the script setting the variable `MAXJOBS`.

Automatically it will create directories called H500_N, where N is the bunch number and will store 500 files maximum in each directory.

The file sim_status.txt will keep track of the state of the simulation, the last bunch number and job_id, hence, in case you exit the application, the next time you lunch will start in the point were it was. The sim_status.txt should be reset to 
```Bunch / job_i
0 / 0
```
before you start.

**!!!Change outdir in the header of the python script.!!!!**



