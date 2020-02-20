import numpy as np
from loguru import logger
from node import Node
import k_anonymity as ka

class Dataset:
    def __init__(self, data: list = list(), p_data: list = list(), kp_data: list = list(), pr: dict = dict(),
                 final_data: dict = dict()):
        self.data = data
        self.p_data = p_data
        self.kp_data = kp_data
        self.pr = pr
        self.final_data = final_data

    def compute_anonymized_data(self):
        """
        create dataset ready to be anonymized
        :return:
        """
        logger.info("Start creation dataset anonymized")
        for index in range(0, len(self.data)):
            logger.info("Start creation Group {}".format(index))

            group = self.data[index]
            list_good_leaf_node = self.p_data[index]
            max_value = np.amax(np.array(list(group.values())), 0)
            min_value = np.amin(np.array(list(group.values())), 0)
            for key in group.keys():
                # key = row product
                self.final_data[key] = list()
                value_row = list()
                for column_index in range(0, len(max_value)):
                    value_row.append("[{}-{}]".format(min_value[column_index], max_value[column_index]))
                for node in list_good_leaf_node:
                    if key in node.group.keys():
                        value_row.append(node.pattern_representation)
                value_row.append("Group: {}".format(index))
                self.final_data[key] = value_row
                logger.info(key)
                logger.info(value_row)
            logger.info("Finish creation Group {}".format(index))

    def recycle_bad_leaves(self, good_leaf_nodes=None, bad_leaf_nodes=None, p_value=None, paa_value=None):
        max_bad_level = 0
        tot_bad_size = 0
        # Find max level and total size of bad_leaf_nodes
        for node in bad_leaf_nodes:
            tot_bad_size += node.size
            if node.level > max_bad_level:
                max_bad_level = node.level

        current_level = max_bad_level
        while tot_bad_size >= p_value and current_level > 0:
            current_PRs = dict()
            current_leaves = dict()
            current_to_merge = list()
            names_to_nodes = dict()
            for node in bad_leaf_nodes:
                if node.level == current_level:
                    if current_PRs.get(node.pattern_representation) == None:
                        current_PRs[node.pattern_representation] = 1
                        current_leaves[node.pattern_representation] = list()
                    else:
                        if node.pattern_representation not in current_to_merge:
                            current_to_merge.append(node.pattern_representation)
                        current_PRs[node.pattern_representation] += 1
            
                    current_leaves[node.pattern_representation].append(node.name)
                    names_to_nodes[node.name] = node
            while len(current_to_merge) > 0:
                current_pattern_representation = current_to_merge.pop(0)
                merge_node_group = dict()
                removed_tuples = 0
                for node in current_leaves[current_pattern_representation]:
                    bad_leaf_nodes.remove(names_to_nodes[node])
                    for key, value in names_to_nodes[node].group.items():
                        merge_node_group[key] = value
                        removed_tuples += 1
                if len(merge_node_group) >= p_value:
                    tot_bad_size -= removed_tuples
                    merge_node = Node(level=current_level, pattern_representation=current_pattern_representation,
                                    label="good-leaf", group=merge_node_group, paa_value=paa_value)
                    good_leaf_nodes.append(merge_node)
                else:
                    merge_node = Node(level=current_level, pattern_representation=current_pattern_representation,
                                    label="bad-leaf", group=merge_node_group, paa_value=paa_value)
                    bad_leaf_nodes.append(merge_node)

            for node in bad_leaf_nodes:
                if node.level == current_level:
                    node.decrease_node_level()
            current_level -= 1
        
        self.p_data = good_leaf_nodes

    def generalize(self):
        for index in range(0, len(self.kp_data)):
            logger.info("Generalizing group {}".format(index))
            group = self.kp_data[index]
            min_list, max_list = ka.get_list_min_and_max_from_table(list(group.values()))
            for key in group:
                row = list()
                for column in range(0, len(group[key])):
                    row.append("[{}-{}]".format(min_list[column], max_list[column]))
                pr = self.pr[key]
                row.append(pr)
                row.append(index)
                self.final_data[key] = row
        return self.final_data

    def save_on_file(self, file_name=None, first_column=None, columns=None):
        separator = "\t"
        columns.insert(0, first_column)
        columns.append("Pattern")
        columns.append("Group")      
        with open(file_name, "w") as file_to_write:
            columns_string = separator.join(map(str, columns)) 
            file_to_write.write(columns_string+"\n")
            for key, value in self.final_data.items():
                value_to_print_on_file = key + separator + separator.join(map(str, value))
                file_to_write.write(value_to_print_on_file+"\n")
