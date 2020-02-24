import os
import main as m
import matplotlib.pyplot as plt

def multiple_tests(file_name=None):
    if file_name == None:
        m.logger.info("Wrong arguments")
    
    if not m.os.path.isfile("datasets\\" + file_name):
        m.logger.info("Wrong path")
        return

    final_table=list()
    final_table.append(["k_value","p_value","paa_value","max_level","ncp"])

    m.logger.disable("main")
    m.logger.disable("p_anonymity")
    m.logger.disable("k_anonymity")
    m.logger.disable("node")
    m.logger.disable("dataset")

    for k_value in range(3,12):
        for p_value in range(k_value-1,1,-1):
            for paa_value in range(3,6):
                for max_level in range(5,11):
                    ncp = m.main(k_value, p_value, paa_value, max_level, file_name)
                    m.logger.info("End: " + str(k_value) + "," + str(p_value) + "," \
                                    + str(paa_value) + "," + str(max_level))
                    final_table.append([k_value,p_value,paa_value,max_level,ncp])
    
    # ncp = m.main(8, 7, 3, 5, file_name)
    # final_table.append([4,3,4,7,ncp])
    # ncp = m.main(8, 7, 3, 6, file_name)
    # final_table.append([5,3,3,5,ncp])
    
    save_ncp_table(file_name=file_name, ncp_table=final_table)

def save_ncp_table(file_name=None, ncp_table=None):
    separator = ","    
    with open("final_table\\" + file_name.replace(".csv", "") + "_out.csv", 'w') as f:
        for row in ncp_table:
            string = separator.join(map(str, row)) 
            f.write(string + "\n")

def plot_tests(file_name=None):
    ncp_table = read_ncp_table(file_name)
    max_level, paa_value = get_best_values(ncp_table)

    # TODO make plots

def read_ncp_table(file_name=None):
    if os.path.isfile("final_table\\" + file_name.replace(".csv", "") + "_out.csv"):
        return m.pd.read_csv("final_table\\" + file_name.replace(".csv", "") + "_out.csv")
    else:
        return

def get_best_values(ncp_table=None):
    ordered_table = ncp_table.sort_values('ncp')
    n_rows = round(len(ordered_table.index) * 0.15)
    counting_rows = ordered_table.head(n_rows)
    occurrences = dict()
    max_couple = (0, 0)
    max_occurrence = 0
    # pylint: disable=W0612
    for index, row in counting_rows.iterrows():
        paa_value = row['paa_value']
        max_level = row['max_level']
        key = (paa_value, max_level)
        if key not in occurrences:
            occurrences[key] = 0
        occurrences[key] += 1
        if occurrences[key] > max_occurrence:
            max_occurrence = occurrences[key]
            max_couple = key
            
    return max_couple[0], max_couple[1]

if __name__ == "__main__":

    if len(m.sys.argv) == 2:
        file_name = m.sys.argv[1]
        plot_tests(file_name=file_name)
    else:
        print("[*] Usage: python test.py dataset.csv")

