import numpy as np
from loguru import logger
from node import Node
from dataset import Dataset



def KAPRA(time_series_dict=None, p_value=None, paa_value=None, max_level=None):
    """
    Implementation of KAPRA Algorithm for time-series anonymization and pattern preservation
    """
    dataset = Dataset()
    # Append all dataset to anonymized dataset --> in KAPRA algorithm the root node is all the dataset
    dataset.data.append(time_series_dict)
    # Lists containing good/bad nodes
    good_leaf_nodes = list()
    bad_leaf_nodes = list()
    # Create root node and start splitting it
    logger.info("Start recursive splitting")
    node = Node(level=1, group=time_series_dict, paa_value=paa_value)
    node.start_splitting(p_value, max_level, good_leaf_nodes, bad_leaf_nodes)
    logger.info("Finish recursive splitting")
    logger.info("Start recycling bad leaves")
    dataset.recycle_bad_leaves(good_leaf_nodes, bad_leaf_nodes, p_value, paa_value)
    logger.info("End recycling bad leaves")


    
