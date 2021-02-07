# oon-boersenspiel-conservative
## Goal
This little program calculates a rating of the largest stocks, available at the OON-Börsenspiel (https://www.oon-boersespiel.at/de/start.html), using the conservative formula (https://www.robeco.com/media/8/6/7/86725c963376853b694728942c6d8b2f_the-conservative-formula-quantitative-investing-made-easy-2018_tcm1003-18732.pdf).
It does not invest in any stocks, it just provides the calculation, prints the results and stores them in rating.csv.

## Usage
install all the requirements from requirements.txt using the following command:
pip3 install -r requirements.txt

then simply run the main script by calling:
python3 main.py

The results will be stored in rating.csv, it is up to you to decide in which (and how many) stocks you want to invest.
Note that in the OON-Börsenspiel only a small size of possible stocks are available (see symbols.csv).
This might lead to the formula not working as well as expected.

## Functionality
### APIs used to get data
First of all yfinance is used to get daily adjusted close prices from Yahoo Finance. Secondly a simple web scraper fetches total yield data for a given symbol from https://www.gurufocus.com/. All the calculations needed can be done with these two data points.
### Calculations
A Pandas Dataframe is being filled in each step of the execution. For the specific calculations such as the Momentum, numpy is used to get more accurate results.
