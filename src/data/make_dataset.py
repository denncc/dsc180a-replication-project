# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
import json
import os

# get the config file
with open("./config/config.json") as f:
    config = json.load(f)

# set the output directory
fastq_output_dir = config["processed"]["fastq"]
fastqc_dir = config["tools"]["FastQC"]

# Kallisto tool dir
kallisto_dir = config["tools"]["kallisto"]
# Kallisto index file
kallisto_idx_dir = config["kallisto"]["index"]
# Kallisto out dir
kallisto_out_dir = config["kallisto"]["out_dir"]


# @click.command()
# @click.argument('input_filepath', type=click.Path(exists=True))
# @click.argument('output_filepath', type=click.Path())
# def main(input_filepath, output_filepath):
#     """ Runs data processing scripts to turn raw data from (../raw) into
#         cleaned data ready to be analyzed (saved in ../processed).
#     """
#     logger = logging.getLogger(__name__)
#     logger.info('making final data set from raw data')

# the function to retrieve the path for the datasets
def data_retrieve():
    data_dir = config["data"][0]
    datasets = os.listdir(data_dir)
    datasets.sort()
    reference = datasets[-3:]
    datasets = datasets[:-3]
    result = []
    for i in range(0, len(datasets), 2):
        result.append([os.path.join(data_dir, datasets[i]), os.path.join(data_dir, datasets[i + 1])])
    for i in range(len(reference)):
        reference[i] = os.path.join(data_dir, reference[i])
    return result, reference

# quality control the datasets using the FastQC
def run_fastqc(fastq_path, output_dir, options=["--extract",]):
    """
    Run the fastqc program on a specified fastq file and return the output directory path.

    Parameters
    ----------
    fastq_path : str
        Path to the fastq file to analyze.
    output_dir : str
        Directory where output will be written. It will be created if it does not exist.
    options : list of str (optional)
        Command-line flags and options to fastqc. Default is --extract.

    Returns
    -------
    output_dir : str
        The path to the directory containing the detailed output for this fastq file.
        It will be a subdirectory of the specified output dir.
    """

    command = "/opt/FastQC/fastqc {} -t 8 -o {} {}".format(' '.join(options), output_dir, fastq_path)
    # subprocess.check_call(command, shell=True)
    os.system(command)

    # Fastqc creates a directory derived from the basename
    fastq_dir = os.path.basename(fastq_path)
    fastq_dir = fastq_dir[0:-9]
    fastq_dir = fastq_dir + "_fastqc"

    # Delete the zip and html file and keep the uncompressed directory
    zip_file = os.path.join(output_dir, fastq_dir + ".zip")
    html_file = os.path.join(output_dir, fastq_dir + ".html")
    os.remove(zip_file)
    os.remove(html_file)


    output_dir = os.path.join(output_dir, fastq_dir)
    return output_dir

# quantify the sequences using kallisto
def kallisto_quant(output, input1, input2):
    '''
    Quantify the RNA-sequence using kallisto
    '''
    command = f"{kallisto_dir} quant -i {kallisto_idx_dir} -o {kallisto_out_dir} -t 8 {input1} {input2}"
    return output


# main function
def main():
    datas, reference = data_retrieve()
    sample = [datas[0], datas[1], datas[2]]
    # run fastq for analysis
    # for fastq in sample:
    #     run_fastqc(fastq[0], fastq_output_dir)
    #     run_fastqc(fastq[1], fastq_output_dir)
    print(sample)
    for fastq in sample:
        print(kallisto_quant(kallisto_out_dir, fastq[0], fastq[1]))

if __name__ == "__main__":

    print("Executing make_dataset.py on command line")

elif __name__ == 'src.data.make_dataset':
    # log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    # logging.basicConfig(level=logging.INFO, format=log_fmt)

    # # not used in this stub but often useful for finding various files
    # project_dir = Path(__file__).resolve().parents[2]

    # # find .env automagically by walking up directories until it's found, then
    # # load up the .env entries as environment variables
    # load_dotenv(find_dotenv())
    print("src/data/make_dataset.py is imported, and data is being processed")
    main()
    print("data processing is done")