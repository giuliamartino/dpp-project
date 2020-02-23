import main as m
from os import listdir
from os.path import isfile, join

def multiple_tests(file_name=None):
    if file_name == None:
        m.logger.info("Wrong arguments")
    
    if not m.os.path.isfile("datasets\\" + file_name):
        m.logger.info("Wrong path")
        return

    final_table=list()
    final_table.append(["k_value","p_value","paa_value","max_level","ncp"])

    m.logger.disable("__main__")
    m.logger.disable("main")
    m.logger.disable("p_anonymity")
    m.logger.disable("k_anonymity")
    m.logger.disable("node")
    m.logger.disable("dataset")

    for p_value in range(2,8):
        for k_value in range(p_value+1,p_value+7):
            for paa_value in range(3,6):
                for max_level in range(5,11):
                    ncp = m.main(k_value, p_value, paa_value, max_level, file_name)
                    m.logger.info("End: " + str(k_value) + "," + str(p_value) + "," \
                                    + str(paa_value) + "," + str(max_level))
                    final_table.append([k_value,p_value,paa_value,max_level,ncp])
    
    # ncp = m.main(4, 3, 4, 7, file_name)
    # final_table.append([4,3,4,7,ncp])
    # ncp = m.main(5, 3, 3, 5, file_name)
    # final_table.append([5,3,3,5,ncp])
    
    save_ncp_table(file_name=file_name, ncp_table=final_table)

def save_ncp_table(file_name=None, ncp_table=None):
    separator = ","    
    with open("final_table\\" + file_name.replace(".csv", "") + "_out.csv", 'w') as f:
        for row in ncp_table:
            string = separator.join(map(str, row)) 
            f.write(string + "\n")

if __name__ == "__main__":

    if len(m.sys.argv) == 2:
        file_name = m.sys.argv[1]
        multiple_tests(file_name=file_name)
    else:
        print("[*] Usage: python test.py dataset.csv")
