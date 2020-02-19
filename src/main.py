import os
import sys
import random
import numpy as np
import pandas as pd
from loguru import logger
import k_anonymity as ka
import p_anonymity as pa
from node import Node
from dataset import Dataset

# Global Variables
max_level = 6 # Max admitted level of a node in tree structure (KAPRA Algorithm)

def main(k_value=None, p_value=None, paa_value=None, dataset_path=None):
    """
    :param k_value:  Value of k attribute
    :param p_value:  Value of p attribute
    :param dataset_path:  Path to the dataset to anonymize (.csv)
    """

    # ----------------------------------------------------- Start Dataset Preparation
    logger.info("Preparing dataset")
    if os.path.isfile(dataset_path):
        # Read the time series from a .csv file
        time_series = pd.read_csv(dataset_path)

    # Get attributes names (columns)
    columns = list(time_series.columns)
    columns.pop(0)  # Remove first column (Country Code)
    # Save all maximum/minimum values for each column
    attributes_maximum_value = list()
    attributes_minimum_value = list()
    for column in columns:
        attributes_maximum_value.append(time_series[column].max())
        attributes_minimum_value.append(time_series[column].min())

    # Build a sort of hashmap - the keys are the Country Codes, the values are all the other columns (the tuple)
    time_series_dict = dict()

    # The function iterrows returns both index of the row and content of the current row
    # pylint: disable=W0612
    for index, row in time_series.iterrows():
        time_series_dict[row["CountryCode"]] = list(row["1960":"2015"])

    # ----------------------------------------------------- End Dataset Preparation

    # ----------------------------------------------------- Start KAPRA Algorithm
    logger.info("Start of KAPRA Algorithm")
    dataset = pa.KAPRA(time_series_dict, p_value, paa_value, max_level)
    logger.info("End of KAPRA Algorithm")
    # ----------------------------------------------------- End KAPRA Algorithm

    # ----------------------------------------------------- Start K-anonymity
    ka.create_k_groups(dataset, k_value, p_value, columns)
    # ----------------------------------------------------- End K-anonymity

    
            

 

if __name__ == "__main__":

    if len(sys.argv) == 5:
        k_value = int(sys.argv[1])
        p_value = int(sys.argv[2])
        paa_value = int(sys.argv[3])
        dataset_path = sys.argv[4]
        if k_value > p_value:
            main(k_value=k_value, p_value=p_value, paa_value=paa_value, dataset_path=dataset_path)
        else:
            print("[*] Usage: python kp-anonymity.py k_value p_value paa_value dataset.csv")
            print("[*] k_value should be greater than p_value")
    else:
        print("[*] Usage: python kp-anonymity.py k_value p_value paa_value dataset.csv")