# imports
import os
import csv
import sys
import numpy as np
from scripts.utils import fingerprints_molmap
from molmap.feature.fingerprint import Extraction, mapkey

# parse arguments
input_file = sys.argv[1]
output_file = sys.argv[2]


root = os.path.dirname(os.path.abspath(__file__))
#sys.path.append(os.path.join(root, "/bidd-molmap/"))


mp = fingerprints_molmap()
# The map only keeps MACCS, ErG and PubChem bits, but the default extractor computes all
# 12 fingerprint types, in order. MAP4 (last) crashes on molecules without atom pairs, such
# as a single ion like [Y+3], and fails the whole batch. Drop MHFP6 and MAP4, which run
# after PubChem and are not used. Keep the types before PubChem: they change the RDKit mol
# in place and so affect the MACCS/ErG/PubChem bits; dropping them would change outputs.
mp.extract = Extraction(feature_dict={k: {} for k in mapkey if k not in ("MHFP6", "MAP4")})


def _to_vector(fmap):
    fmap = np.sum(fmap, axis=-1)
    return fmap.reshape(-1)


# my model
def my_model(smiles_list):
    try:
        X = mp.batch_transform(smiles_list)
        return [_to_vector(x) for x in X]
    except Exception:
        # One bad input (e.g. an invalid SMILES) makes the whole batch fail, so retry
        # one molecule at a time and return an empty row only for the inputs that fail.
        outputs = []
        for smi in smiles_list:
            try:
                outputs += [_to_vector(mp.transform(smi))]
            except Exception:
                outputs += [None]
        return outputs


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
        if o is None:
            writer.writerow([""] * len(header))
        else:
            writer.writerow([int(o_) for o_ in o])