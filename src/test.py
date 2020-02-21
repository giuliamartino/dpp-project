import main as m
from os import listdir
from os.path import isfile, join

def multiple_tests(file_name=None):
    if file_name == None:
        m.logger.info("Wrong arguments")
    
    if not m.os.path.isfile("datasets\\" + file_name):
        m.logger.info("Wrong path")
        return


    # for p_value in range(2,8):
    #     for k_value in range(p_value+1,p_value+7):
    #         for paa_value in range(3,6):
    #             for max_level in range(5,11):
    #                 ncp = m.main(k_value, p_value, paa_value, max_level, file_name)
    #                 m.logger.info("End: " + str(k_value) + "," + str(p_value) + "," + str(paa_value) + "," + str(max_level))

    m.main(2, 3, 3, 5, file_name)

if __name__ == "__main__":

    if len(m.sys.argv) == 2:
        file_name = m.sys.argv[1]
        multiple_tests(file_name=file_name)
    else:
        print("[*] Usage: python test.py dataset.csv")
