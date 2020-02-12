import os
import numpy as np
import pandas as pd
import sys
from loguru import logger
import random
#from node import Node
#from dataset_anonymized import DatasetAnonymized
max_level = 4

def main(k_value=None, p_value=None, paa_value=None, dataset_path=None):
    print(k_value)
    print(p_value)
    print(paa_value)
    

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