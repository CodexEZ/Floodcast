from django.test import TestCase
import os
import pandas as pd

path = os.path.join(os.getcwd()+ "\static\station.csv")
df = pd.read_csv(path)
print(df)
