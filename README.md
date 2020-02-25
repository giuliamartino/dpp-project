## Project for Data Protection and Privacy - Time Series Anonymization with (k,P)-anonymity

## Requirements <br /> 
- numpy v1.16.4 <br />
- pandas v0.25.0 <br />
- loguru v0.3.2 <br /> 
- saxpy v1.0.1.dev167 <br />
- matplotlib v3.1.3 <br />

## Datasets <br />
In the [datasets](/datasets "datasets") folder there are three different example datasets. All dataset must be **.csv** and must have the columns name in the first row. <br />
Our example datasets: <br />
- [ExoTest.csv](datasets/ExoTest.csv "ExoTest.csv") <br />
- [Products.csv](datasets/Products.csv "Products.csv") <br />
- [UrbanPopulation.csv](datasets/UrbanPopulation.csv "UrbanPopulation.csv") <br />
## Usage <br />
- Single test <br />
	Run the [main.py](src/main.py "main.py") file:<br />
	`[*] Usage: python kp-anonymity.py k_value p_value paa_value max_level dataset.csv`<br />
	Where k_value must be greater than p_value, max_level must be greater than 2 and lower than 20.<br />
	This program generates the kp-anonymization of the input dataset in a new file in the [outputs](outputs "outputs") folder.<br />

- Multiple test<br />
	Run the [test.py](src/test.py "test.py") file:<br />
	`[*] Usage: python test.py dataset.csv multitest`<br />
	This test runs the [main.py](src/main.py "main.py") many times and creates a .csv file containing all the average values of the NCPs (Normalized Certainty Penalty) of each table, saved in the [final_table](final_table "final_table") folder.<br />

- Plot<br />
	Run the [test.py](src/test.py "test.py") file:<br />
	`[*] Usage: python test.py dataset.csv plot`<br />
	This test can be done only if you have an output in [final_table](final_table "final_table") folder.<br />
	This test plots in a three-dimensional chart the output data from **multiple test** step.<br />
	The program chooses the pair (paa_value, max_level) that produces the best NCP. Then it plots only tuples with that values of the pair (paa_value, max_level).<br />
  
   <img src="IMG/plot_ExoTest.jpg" alt="Plot" width="300"/>

## Explain Parameters <br />
- k_value: value of k-anonymity <br />
- p_value: value of p-anonymity, the pattern <br />
- paa_value: quantity of letters that can be used to describe the pattern <br />
- max_level: number of letters that can be used to describe the pattern <br />

   

