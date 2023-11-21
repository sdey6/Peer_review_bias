import json
import pickle
import numpy as np
from matplotlib import pyplot as plt

from data_gathering.helper_data_collect import get_citation, api_key
from get_full_display import full_display
import pandas as pd
from bs4 import BeautifulSoup
import requests
from serpapi import GoogleSearch

path_pickle = 'C:/Users/souri/PycharmProjects/thesis_code/data_gathering/data_pickeled/'

""" Get citation for 2017 """

df_17 = pd.read_pickle(f'{path_pickle}all_data_17.pkl')
df_17.title = df_17.title.apply(lambda x: x.lower())
title_list = df_17.title.unique().tolist()
data_cit_17 = get_citation(api_key, title_list[:3])
data_cit_17 = cit_df_5 = pd.DataFrame(data_cit_17)

data_cit_17.title = data_cit_17.title.apply(lambda x: x.lower())
data_cit_17 = data_cit_17[data_cit_17.title.isin(title_list)].reset_index(drop=True)
data_cit_17 = data_cit_17.drop_duplicates('title').reset_index(drop=True)
data_cit_17.cited_by_count = data_cit_17.cited_by_count.fillna(0)
data_cit_17.cited_by_count = data_cit_17.cited_by_count.astype(int)
pickle.dump(data_cit_17, open(f'{path_pickle}all_cit_17.pkl', 'wb'))
cit_17 = pd.read_pickle(f'{path_pickle}all_cit_17.pkl')
print(cit_17.head())

""" Get citation for 2018 """

df = pd.read_pickle(f'{path_pickle}all_data_18.pkl')  # use the pickled data
title_list = df.title.unique().tolist()
data_cit = get_citation(api_key, title_list[:2])  # get the citations
cit_df = pd.DataFrame(data_cit)
cit_df.title = cit_df.title.apply(lambda x: x.lower())
title_list = [i.lower() for i in title_list]
cit_df_18 = cit_df[cit_df.title.isin(title_list)].reset_index(drop=True)
df_cit_new = cit_df_18.drop_duplicates('title').reset_index(drop=True)
df_cit_new.cited_by_count = df_cit_new.cited_by_count.fillna(0)
df_cit_new = df_cit_new[~(df_cit_new.cited_by_count == 'No result')].reset_index(drop=True)
df_cit_new.cited_by_count = df_cit_new.cited_by_count.astype(int)
pickle.dump(df_cit_new, open(f'{path_pickle}all_cit_18.pkl', 'wb'))
cit_18 = pd.read_pickle(f'{path_pickle}all_cit_18.pkl')
print(cit_18.head())

""" Get citation for 2019 """
df = pd.read_pickle(f'{path_pickle}all_data_19.pkl')  # use the pickled data
title_list = df.title.unique().tolist()
data_cit = get_citation(api_key, title_list[:3])
cit_df = pd.DataFrame(data_cit)
cit_df.title = cit_df.title.apply(lambda x: x.lower())
title_list = [i.lower() for i in title_list]
cit_df_19 = cit_df[cit_df.title.isin(title_list)].reset_index(drop=True)
df_cit_new_19 = cit_df_19.drop_duplicates('title').reset_index(drop=True)
df_cit_new_19.cited_by_count = df_cit_new_19.cited_by_count.fillna(0)
df_cit_new_19 = df_cit_new_19[~(df_cit_new_19.cited_by_count == 'No result')].reset_index(drop=True)
df_cit_new_19.cited_by_count = df_cit_new_19.cited_by_count.astype(int)
pickle.dump(df_cit_new_19, open(f'{path_pickle}all_cit_19.pkl', 'wb'))
cit_19 = pd.read_pickle(f'{path_pickle}all_cit_19.pkl')
print(cit_19.shape)

