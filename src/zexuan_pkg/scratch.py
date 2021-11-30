import numpy as np
import pandas as pd


df = pd.DataFrame(np.random.randint(0, 100, (4,5)))
df.columns = [f"C{i}" for i in range(1,6)]

print(">>> df\n", df)
print(">>> df.shape\n", df.shape)
print("---")

# print(">>> df.iloc[:, 2]\n", df.iloc[:, 2])
# print("---")

# print(">>> df.mean()\n", df.mean())
# print("---")

# print(">>> df.mean(axis=1)\n", df.mean(axis=1))
# print("---")



import datetime

start_date = datetime.date(1950, 1, 1)
end_date = start_date + datetime.timedelta(days=4-1)

df["date"] = pd.date_range(start_date, end_date)
print(df)