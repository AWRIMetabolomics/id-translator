#! /usr/bin/env python3

# Given a `hmdb_metabolites.xml` file, a dict (json) of "primary_key":[list_of_secondary_keys] - that is, a dictionary of primary HMDB accession numbers, with their respective secondary accession numbers, and save it all in a `json`. This does not need to be done frequently.
# Get the input XML file from (link "All Metabolites" XML file): https://hmdb.ca/downloads
# Necessary because MetaboAnalyst sometimes returns secondary accession numbers instead of primary ones, and a GET request to `https://hmdb.ca/metabolites/{hmdb_id}.xml` won't work for secondary HMDB accession numbers (browser behaviour: auto-redirect to primary accession number, which confuses the GET request, causing it to return javascript gibberish with status code 200). 
# Also neater, I think: primary HMDB IDs are stable over time, so better for ID purposes. 
# Written by don teng, 2022-dec-1
# runtime: approx 200s. 

# ========== Usage ==========
# python3 get_hmdb_accession_dict.py -i path/to/hmdb_metabolites.xml -o path/to/output_dict.json

# ========== Start! ==========
import time
import numpy as np
import pandas as pd
import json
import sys
import getopt
#import os
import subprocess

#pd.set_option('display.max_rows', 500)

#path_to_hmdb_xml = "/Users/dteng/Documents/zdata/hmdb_metabolites_14jun2022.xml"
#path_out_json = "hmdb_id_dict.json"

def get_io_paths():
    path_in = ""
    path_out = ""
    
    argv = sys.argv[1:]
    opts, args = getopt.getopt(argv, "i:o:")
    
    for opt, arg in opts:
        if opt in ["-i", "--input"]:
            path_in = arg
        elif opt in ["-o", "--output"]:
            path_out = arg
            
    return path_in, path_out


path_to_hmdb_xml, path_out_json = get_io_paths()

# -------------------- run! --------------------
# -------------------- user input params --------------------
path_to_hmdb_xml = "/Users/dteng/Documents/zdata/hmdb_metabolites_14jun2022.xml"
path_out_json = "hmdb_id_dict.json"

# -------------------- run! --------------------
t0 = time.perf_counter()

cmd = f'grep -n "<metabolite>" {path_to_hmdb_xml}'
myoutput = subprocess.run(cmd, shell=True, capture_output=True)
output_str = myoutput.stdout.decode('ascii')
cmd = f'grep -n "<accession>" {path_to_hmdb_xml}'
myoutput = subprocess.run(cmd, shell=True, capture_output=True)
output2 = myoutput.stdout.decode('ascii')
output_str += output2

# parse stdout output into a list of lists
c = output_str.split("\n")
c2 = []
for i in range(len(c[:-1])):
    if len(c[i]) > 0:
        new_line = c[i].replace(" ", "").replace("\n", "").replace("<accession>", "").replace("</accession>", "").split(":")
        new_line[0] = int(new_line[0])
        c2.append(new_line)

# put in df to sort
df = pd.DataFrame(data=c2, columns=["line_num", "line_value"]).sort_values(by="line_num").reset_index(drop=True)
m = df.values

temp_ls = "|".join(m[1:, 1]).split("|<metabolite>|")
temp_ls = [x.split("|") for x in temp_ls]

hmdb_accession_dict = {}
for row in temp_ls:
    hmdb_accession_dict[row[0]] = row
    
print("%.2fs" % (time.perf_counter() - t0))


# write out
with open(path_out_json, "w") as f:
    json.dump(hmdb_accession_dict, f)
