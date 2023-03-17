# Yggdrasil

### one pipeline to rule them all
![Suck it](images/logo_ygg.png "Best icon ever")
## Objective summary

Important: the pipeline should always be developed with the fact in mind that there will be cases
where we want to run it directly. Therefore it is both important to add and document command line
arguments. After we have a complete version one for sequencing only we should start writing tests.
As a rule of thumb, before we merge pull requests on main, we should perform these tests.

### Initialization

* Yggdrasil is a workflow written in nextflow using DSL 2
* It is initiated on LSENS once cron detects a ctg.sync.done file under a raw data directory in ../uploads
* cron will only pass the path to the raw data to Yggdrasil, everything else happens in Yggdrasil

### General Steps of the workflow

1. The CTG_samplesheet...csv is parsed looking for project ids and the raw data is symlinked into project specific directories
2. Bclconvert demuxes and produces per project output
...

We should probably forget about symlinking raw data, we are not planning to deliver the rawdata in the future!

