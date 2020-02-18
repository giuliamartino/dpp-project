import numpy as np
from loguru import logger
from node import Node

class Dataset:
    def __init__(self, data: list = list(), p_data: list = list(), kp_data: list = list()):
        self.data = data
        self.p_data = p_data
        self.kp_data = kp_data
        self.final_data = dict()

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

    def save_on_file(self, file_name):
        with open(file_name, "w") as file_to_write:
            value_to_print_on_file = ""
            for key, value in self.final_data.items():
                value_to_print_on_file = key
                value_to_print_on_file = "{},{}".format(value_to_print_on_file, ",".join(value))
                file_to_write.write(value_to_print_on_file+"\n")

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
