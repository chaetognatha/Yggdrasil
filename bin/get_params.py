#!/usr/bin/env python
import pathlib
import re
import sys
# get raw path from nextflow
raw = pathlib.Path(f'{sys.argv[1]}')
print(raw)
# grab the first one, shouldn't be more lying around
samplesheet = next(raw.glob('CTG_*.csv'))
print(samplesheet)
# first open file
with open(samplesheet, 'r') as f:
    # read the samplesheet into string
    ss = f.read()
print(ss)
# use regex to capture [BCLConvert_Data]()[*]
# the right way
try:
    pattern = re.compile(r'\[BCLConvert_Data\],{0,}\n(.*)\]?', re.DOTALL)
    data = pattern.findall(ss)[0]

# or the wrong way
except:
    print('legacy mode')
    pattern = re.compile(r'.*\[Data\],{0,}\n(.*)\]?', re.DOTALL)
    data = pattern.findall(ss)[0]

# find the Sample_Project column and extract unique values
my_split = data.split('\n')

# search in the first item
for i, item in enumerate(my_split[0].split(',')):
    if item == 'Sample_Project':
        # get the index of the column
        col = i

# make set with unique values in the column
projectids = set()
for item in my_split[1:]:
    item = item.split(',')
    if len(item) >= col:
        projectids.add(item[col])

# write to file
with open('projectids.txt', 'w') as f:
    f.write('\n'.join(projectids))

# find the flowcell
# the flowcell is printed by the sequencer
# to RunParameters.xml
with open(raw / 'RunParameters.xml', 'r') as f:
    rp = f.read()

#  use regex to capture <FlowCellSerialNumber>AACGHWHM5</
pattern = re.compile(r'.*<FlowCellSerial\w+>(\w+)\<\/', re.DOTALL)
flowcell = pattern.findall(rp)[0]

# write to file
with open('flowcell.txt', 'w') as f:
    f.write(flowcell)

# find the pipeline to run
# look for the pipeline name in the samplesheet
# under [Yggdrasil_Settings]
pattern = re.compile(r'.*Yggdrasil_Settings\].*Pipeline,(\w+)', re.DOTALL)
pipeline = pattern.findall(ss)[0]

# write to file
with open('pipeline.txt', 'w') as f:
    f.write(pipeline)

# also write out the content of samplesheet
with open('SampleSheet.csv', 'w') as f:
    f.write(ss)