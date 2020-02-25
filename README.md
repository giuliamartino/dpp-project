## Project for Data Protection and Privacy - Time Series Anonymization with (k,P)-anonymity
## Usage
- Single test <br />
	Run the **main.py** file:<br />
	`[*] Usage: python kp-anonymity.py k_value p_value paa_value max_level dataset.csv`<br />
	Where k_value must be greater than p_value, max_level must be greater than 2 and lower than 20.<br />
	This file outputs the kp-anonymisation, of the input dataset, in a new file in the **outputs** folder.<br />

- Multiple test<br />
	Run the **test.py** file:<br />
	`[*] Usage: python test.py dataset.csv multitest`<br />
	This test runs the **main.py** many times and creates a .csv file containing all the average values of the ncp of each table, saved in the **final_table** folder <br />

- Plot<br />
	Run the **test.py** file:<br />
	`[*] Usage: python test.py dataset.csv plot`<br />
	This test must be done only if you have the multiple test output in the **final_table**.<br />
	This test plots in a three-dimensional chart the output data from the **multiple test** step.<br />
	The program chooses the max_level and paa_value pair that has the best ncp, than it plots only tuples with that data.<br />
  
   <img src="IMG/plot_ExoTest.jpg" alt="Plot" width="300"/>
   

