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

# Running.
`./make_swif_sim.py N`

This will create a swif workflow named `clasdis`, add N jobs to it and run it.

Each job consist of 10000 events. The result is a hipo file named cooked_n.hipo, n from 0 to N.

!!!Change outdir in the header of the python script.!!!!

