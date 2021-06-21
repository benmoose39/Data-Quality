import pandas as pd

filename = input('Enter filename: ')
df = pd.DataFrame(pd.read_excel(filename))

df.to_csv(f"{filename.split('.')[0]}.csv", index=False)

input('[SUCCESS] Press ENTER to exit...')
