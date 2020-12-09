import subprocess
import json
import os
import pandas as pd

with open("./config/feature_config.json") as f:
    feature_config = json.load(f)

# get the location of R script
r_scipt_dir = feature_config["r_script_dir"]
# Kallisto out dir
kallisto_out_dir = feature_config["processed"]["kallisto"]
# dir for DESeq2 output dir
deseq_cts_matrix_dir = feature_config["features"]["deseq_cts_matrix_dir"]

def test_r():
    """
    test running the R script
    """
    print(r_scipt_dir)
    subprocess.call(["Rscript", "--vanilla", r_scipt_dir])

def make_cts():
    """
    This method doesn't have an input, but rather takes 352 abundance.tsv in the processed
    Kallisto directory, and makes a matrix that counts different subfeatures.
    """
    abundances_dirs = os.listdir(kallisto_out_dir)
    abundances_dirs.sort()
    # cols_name = pd.read_csv(os.path.join(kallisto_out_dir, abundances_dirs[0], "abundance.tsv"), sep="\t").target_id
    # print(cols_name)
    result = pd.DataFrame()
    for pair in abundances_dirs:
        abundances_dir = os.path.join(kallisto_out_dir, pair, "abundance.tsv")
        df = pd.read_csv(abundances_dir, sep="\t")
        df = df.set_index("target_id")
        est_counts = df.est_counts
        result[pair] = est_counts
    result.to_csv(deseq_cts_matrix_dir, sep="\t")
    # print(abundances_dir)
    return