import os
import numpy as np
import pandas as pd
import sys
from loguru import logger
import random


def compute_normalized_certainty_penalty_on_ai(table=None, maximum_value=None, minimum_value=None):
    # TODO check if |Ai| should be calculate on original table or not
    """
    Compute NCP(T)
    :param table:  The table used to calculate NCP
    :return:  The NCP of the passed table
    """
    z_1 = list()
    y_1 = list()
    a = list()
    for index_attribute in range(0, len(table[0])):
        temp_z1 = 0
        temp_y1 = float('inf')
        for row in table:
            if row[index_attribute] > temp_z1:
                temp_z1 = row[index_attribute]
            if row[index_attribute] < temp_y1:
                temp_y1 = row[index_attribute]
        z_1.append(temp_z1)
        y_1.append(temp_y1)
        a.append(abs(maximum_value[index_attribute] - minimum_value[index_attribute]))
    ncp_t = 0
    for index in range(0, len(z_1)):
        try:
            ncp_t += (z_1[index] - y_1[index]) / a[index]
        except ZeroDivisionError:
            ncp_t += 0
    ncp_T = len(table)*ncp_t
    return ncp_T

def find_tuple_with_maximum_ncp(fixed_tuple, time_series_tmp, key_fixed_tuple, maximum_value, minimum_value, excluded_row=None):
    # While we search the couple which maximizes the NCP, we exclude the last checked row
    time_series = time_series_tmp.copy()
    if excluded_row != None:
        del time_series[excluded_row]
    
    """
    By scanning all tuples once, we can find tuple t1 that maximizes NCP(fixed_tuple, t1)
    :param fixed_tuple:
    :param time_series:
    :param key_fixed_tuple:
    :return:
    """
    max_value = 0
    tuple_with_max_ncp = None
    # pylint: disable=W0612
    for key, value in time_series.items():
        if key != key_fixed_tuple:
            ncp = compute_normalized_certainty_penalty_on_ai([fixed_tuple, time_series[key]], maximum_value, minimum_value)
            if ncp >= max_value:
                max_value = ncp
                tuple_with_max_ncp = key
    return tuple_with_max_ncp

def get_list_min_and_max_from_table(table):
    """
    From a table get a list of maximum and minimum value of each attribut
    :param table:
    :return: list_of_minimum_value, list_of_maximum_value
    """

    attributes_maximum_value = table[0]
    attributes_minimum_value = table[0]

    for row in range(1, len(table)):
        for index_attribute in range(0, len(table[row])):
            if table[row][index_attribute] > attributes_maximum_value[index_attribute]:
                attributes_maximum_value[index_attribute] = table[row][index_attribute]
            if table[row][index_attribute] < attributes_minimum_value[index_attribute]:
                attributes_minimum_value[index_attribute] = table[row][index_attribute]

    return attributes_minimum_value, attributes_maximum_value

def k_anonymity_top_down_approach(time_series=None, k_value=None, columns_list=None, maximum_value=None,
                                  minimum_value=None, time_series_k_anonymized=None):
    """
    k-anonymity based on work of Xu et al. 2006,
    Utility-Based Anonymization for Privacy Preservation with Less Information Loss
    :param time_series:  Time-series to anonymize
    :param k_value:  Value of k attribute
    """
    if len(time_series) < 2*k_value:
        logger.info("End Recursion")
        time_series_k_anonymized.append(time_series)
        return
    else:
        # TODO compute max and minumum_value for each recursive methods

        # Partition time_series into two exclusive subsets group_u and group_v
        # such that group_u and group_v are more local than time_series,
        # and either group_u or group_v have at least k tuples
        logger.info("Start partition with size {}".format(len(time_series)))
        keys = list(time_series.keys())
        
        # Pick random tuple
        random_tuple = keys[random.randint(0, len(keys) - 1)]
        logger.info("Get random tuple (u1) {}".format(random_tuple))

        # Search for the couple of tuples (u,v) which maximizes NCP(u,v)
        rounds = 6
        current_row = random_tuple
        last_row = random_tuple

        # pylint: disable=W0612
        for round in range(0, rounds):
            tmp_row = find_tuple_with_maximum_ncp(time_series[current_row], time_series, current_row, maximum_value, minimum_value)
            last_row = current_row
            current_row = tmp_row
            
        # The couple (u,v) is (current_row, last_row)
        # Now we use u,v as seeds to create two groups with lower certainty penality
        group_u = dict()
        group_v = dict()
        group_u[current_row] = time_series[current_row]
        del time_series[current_row]
        group_v[last_row] = time_series[last_row]
        del time_series[last_row]
        index_keys_time_series = [x for x in range(0, len(list(time_series.keys())))]
        random.shuffle(index_keys_time_series)
        keys = [list(time_series.keys())[x] for x in index_keys_time_series]
        # Pick a random row from time_series and add it to group with lower NCP
        for key in keys:
            row_temp = time_series[key]
            group_u_values = list(group_u.values())
            group_v_values = list(group_v.values())
            group_u_values.append(row_temp)
            group_v_values.append(row_temp)
            # max_temp_value_u, min_temp_value_u = get_list_min_and_max_from_table(group_u_values)
            # max_temp_value_v, min_temp_value_v = get_list_min_and_max_from_table(group_v_values)

            ncp_u = compute_normalized_certainty_penalty_on_ai(group_u_values, maximum_value, minimum_value)
            ncp_v = compute_normalized_certainty_penalty_on_ai(group_v_values, maximum_value, minimum_value)

            if ncp_v < ncp_u:
                group_v[key] = row_temp
            else:
                group_u[key] = row_temp
            del time_series[key]

        if (len(group_u) < k_value) or (len(group_v) < k_value):
            if len(group_u) < k_value:
                bad_group = group_u
                good_group = group_v
            else:
                bad_group = group_v
                good_group = group_u

            missing_rows = k_value - len(bad_group)
            for i in range(0, missing_rows):
                index_keys_good_group = [x for x in range(0, len(list(good_group.keys())))]
                keys = [list(good_group.keys())[x] for x in index_keys_good_group]
                min_ncp = float('inf')
                min_ncp_index = ''
                for key in keys:
                    row_temp = good_group[key]
                    bad_group_values = list(bad_group.values())
                    bad_group_values.append(row_temp)
                
                    new_ncp = compute_normalized_certainty_penalty_on_ai(bad_group_values, maximum_value, minimum_value)
                    if new_ncp < min_ncp:
                        min_ncp = new_ncp
                        min_ncp_index = key

                bad_group[min_ncp_index] = good_group[min_ncp_index]
                del good_group[min_ncp_index]

        logger.info("Group u: {}, Group v: {}".format(len(group_u), len(group_v)))
        if len(group_u) > k_value:
            # Recursive partition of group_u
            # maximum_value, minimum_value = get_list_min_and_max_from_table(list(group_u.values()))
            k_anonymity_top_down_approach(time_series=group_u, k_value=k_value, columns_list=columns_list,
                                          maximum_value=maximum_value, minimum_value=minimum_value,
                                          time_series_k_anonymized=time_series_k_anonymized)
        else:
            time_series_k_anonymized.append(group_u)

        if len(group_v) > k_value:
            # Recursive partition of group_v
            # maximum_value, minimum_value = get_list_min_and_max_from_table(list(group_v.values()))
            k_anonymity_top_down_approach(time_series=group_v, k_value=k_value, columns_list=columns_list,
                                          maximum_value=maximum_value, minimum_value=minimum_value,
                                          time_series_k_anonymized=time_series_k_anonymized)
        else:
            time_series_k_anonymized.append(group_v)
