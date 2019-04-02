# %matplotlib inline

import pandas as pd
import networkx as nx

# Ignore matplotlib warnings
# import warnings
# warnings.filterwarnings("../ignore")


df = pd.read_csv("us_job_data/edges.csv", encoding="ISO-8859-1")
df.head()

g = nx.from_pandas_edgelist(df, source='skill', target='entity')
nx.draw(g)
