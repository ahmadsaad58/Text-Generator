import pandas as pd

if __name__ == "__main__":
	with open('data.txt', 'r+') as f:
		x = pd.DataFrame([line.strip() for line in f])
		x.to_csv('data.csv')