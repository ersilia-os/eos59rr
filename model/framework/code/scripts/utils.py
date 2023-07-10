import sys
import os

root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(root, "../bidd-molmap/"))

import molmap

metric = "cosine"


descriptors_filename = os.path.abspath(os.path.join(root, "../../../checkpoints/descriptor.mp"))
fingerprints_filename = os.path.abspath(os.path.join(root, "../../../checkpoints/fingerprint.mp"))


def _get_descriptors_molmap():
    return molmap.MolMap(ftype="descriptor", metric=metric, split_channels=False)

def fit_descriptors_molmap():
    mp = _get_descriptors_molmap()
    mp.fit(method="umap", verbose=2)
    mp.save(descriptors_filename)

def descriptors_molmap():
    mp = _get_descriptors_molmap()
    return mp.load(filename=descriptors_filename)

def _get_fingerprints_molmap():
    bitsinfo = molmap.feature.fingerprint.Extraction().bitsinfo
    flist = bitsinfo[
        bitsinfo.Subtypes.isin(["MACCSFP", "PharmacoErGFP", "PubChemFP"])
    ].IDs.tolist()
    return molmap.MolMap(ftype="fingerprint", metric=metric, flist=flist, split_channels=False)

def fit_fingeprints_molmap():
    mp = _get_fingerprints_molmap()
    mp.fit(method="umap", verbose=2)
    mp.save(fingerprints_molmap)

def fingerprints_molmap():
    mp = _get_fingerprints_molmap()
    return mp.load(filename=fingerprints_filename)

