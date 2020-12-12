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
# covariates dir from the SRAruntable
covariates = feature_config["features"]["covariates"]
covariates_dir = covariates["dir"]
covariates_in_cols = covariates["columns"]["in_cols"]
covariates_out_cols = covariates["columns"]["out_cols"]
disorders = covariates["disorders"]
brain_regions = covariates["brain_regions"]
abbr = covariates["disorders_abbr"]
num_cov = covariates["num"]
# sraruntable_dir table dir
sraruntable_dir = feature_config["sraruntable_dir"]

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
        result[pair] = est_counts.round(0).astype(int)
    result.to_csv(deseq_cts_matrix_dir, sep="\t")
    # print(abundances_dir)
    return

<<<<<<< HEAD
def make_cts_test():
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
        result[pair] = est_counts.round(0).astype(int)
    result.to_csv(deseq_cts_matrix_dir, sep="\t")
    # print(abundances_dir)
    return

def make_coldata():
=======
def make_subcoldata():
>>>>>>> 234f32d4a5f180d6b009daf6dbc9bdfed7db9844
    """
    This methood doesn't have an input, but rather takes in SraRunTable.csv to build the input covariates for 
    DESeq object
    """
    df = pd.read_csv(sraruntable_dir).set_index("Run")
    df = df[covariates_in_cols].rename(dict(zip(covariates_in_cols, covariates_out_cols)), axis = 1)
    print("Determine if there is null value in the csv. \n", df.isna().sum())
    df.pH = df.pH.fillna(df.pH.mean())
    print("Determine again if there is null value. \n", df.isna().sum())    
    df.to_csv(covariates_dir)
    cts_df = pd.read_csv(deseq_cts_matrix_dir, sep="\t").set_index("target_id")
    print(cts_df)
    for i in range(num_cov):
        for j in range(num_cov):
            cond = (df.brain_region == brain_regions[i]) & (df.Disorder.isin(["Control", disorders[j]]))

            subcoldata = df[cond]
            subcoldata_name = "subcoldata_" + brain_regions[i] + "_" + abbr[j] + ".csv"
            subcoldata_dir = "./data/features/subcoldata/" + subcoldata_name

            subcts_name = "subcts_" + brain_regions[i] + "_" + abbr[j] + ".csv"
            subcts_cond = cond[cond != 0].index.tolist()
            subcts = cts_df[subcts_cond]
            subcts_dir = "./data/features/subcts/" + subcts_name
            
            print(subcoldata_dir, subcts_dir)
            subcoldata.to_csv(subcoldata_dir)
            subcts.to_csv(subcts_dir)
    return


def make_lfc_data():
    """
    This method doesn't have an input, but rather takes in the lrt result of R and 
    make them suitable for visualiztion
    """
    lrt_dirs = feature_config["features"]["lrt"]
    outdir = feature_config["lfc_data_dir"]
    res = pd.DataFrame()
    for lrt_dir in lrt_dirs:
        df = pd.read_csv(lrt_dir, index_col=0)
        name = lrt_dir[26:-4]
        res[name] = df["log2FoldChange"]
    print(res)
    res.to_csv(outdir)
    return


def main():
    """
    Main function to call on other methods in this file
    """
<<<<<<< HEAD
    if not os.path.exists("./data/features"):
        os.makedirs("./data/features")
    make_cts()
    # make_coldata()
    return


def test():
    """
    Test function to check build features
    """
    make_cts_test()
=======
    # make_cts()
    # make_subcoldata()
    make_lfc_data()
    return
>>>>>>> 234f32d4a5f180d6b009daf6dbc9bdfed7db9844
