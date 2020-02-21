import main as m

def main(file_name=None):
    if file_name == None:
        m.logger.info("Wrong arguments")
    
    if not m.os.path.isfile("datasets\\" + file_name):
        m.logger.info("Wrong path")
        return

    for k_value in range(2,8):
        for p_value in range(k_value+1, k_value+2):
            for paa_value in range(3,6):
                for max_level in range(5,11):
                    m.main(k_value, p_value, paa_value, max_level, file_name)
       
if __name__ == "__main__":

    if len(m.sys.argv) == 2:
        file_name = m.sys.argv[1]
        main(file_name=file_name)
    else:
        print("[*] Usage: python test.py dataset.csv")
