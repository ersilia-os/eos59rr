# imports
import os
import csv
import sys
import numpy as np
from scripts.utils import fingerprints_molmap

# parse arguments
input_file = sys.argv[1]
output_file = sys.argv[2]


root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(root, "/bidd-molmap/"))


mp = fingerprints_molmap()


# my model
def my_model(smiles_list):
    X = mp.batch_transform(smiles_list)
    X = np.sum(X, axis=3)
    X = X.reshape(X.shape[0], X.shape[1]*X.shape[2])
    return X


# read SMILES from .csv file, assuming one column with header
with open(input_file, "r") as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    smiles_list = [r[0] for r in reader]

# run model
outputs = my_model(smiles_list)

#check input and output have the same lenght
input_len = len(smiles_list)
output_len = len(outputs)
assert input_len == output_len

header = []
for i in range(37):
    for j in range(36):
        header += ["row_{0}_col_{1}".format(str(i).zfill(2), str(j).zfill(2))]

# write output in a .csv file
with open(output_file, "w") as f:
    writer = csv.writer(f)
    writer.writerow(header)  # header
    for o in outputs:
        writer.writerow(o)