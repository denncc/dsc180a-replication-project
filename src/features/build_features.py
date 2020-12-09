import subprocess
import json

with open("./config/feature_config.json") as f:
    feature_config = json.load(f)

# get the location of R script
r_scipt_dir = feature_config["r_script_dir"]

def test_r():
    """
    test running the R script
    """
    print(r_scipt_dir)
    subprocess.call(["Rscript", "--vanilla", r_scipt_dir])