import pickle
import pandas as pd
from get_full_display import full_display

pd.options.mode.chained_assignment = None  # default='warn'

path_pickle = 'C:/Users/souri/PycharmProjects/thesis_code/data_gathering/data_pickeled/'

df_17 = pd.read_pickle(f'{path_pickle}all_data_17.pkl')
df_18 = pd.read_pickle(f'{path_pickle}all_data_18.pkl')
df_19 = pd.read_pickle(f'{path_pickle}all_data_19.pkl')
print(df_17.columns)

col_paper = ['title', 'Authors', 'decision', 'year']
col_author = ['Authors', 'academic_age', 'current_age', 'total_num_pub', ]
col_review = ['title', 'rating_score', 'confidence_score', 'review']

""" Paper Feature """


def get_paper_feature():
    df_17_paper = df_17[col_paper]
    df_18_paper = df_18[col_paper]
    df_19_paper = df_19[col_paper]
    df_all_paper = pd.concat([df_17_paper, df_18_paper, df_19_paper], axis=0).reset_index(drop=True)
    return df_all_paper


""" Review Feature """


def get_review_feature():
    df_17_rev = df_17[col_review]
    df_18_rev = df_18[col_review]
    df_19_rev = df_19[col_review]
    df_all_review = pd.concat([df_17_rev, df_18_rev, df_19_rev], axis=0).reset_index(drop=True)
    return df_all_review


""" Author Feature """


def get_author_feature():
    df_17_auth = df_17[col_author]
    df_18_auth = df_18[col_author]
    df_19_auth = df_19[col_author]
    df_all_auth = pd.concat([df_17_auth, df_18_auth, df_19_auth], axis=0).reset_index(drop=True)
    return df_all_auth


""" Citation Feature """


def get_cit_feature():
    cit_17 = pd.read_pickle(f'{path_pickle}all_cit_17.pkl')
    cit_18 = pd.read_pickle(f'{path_pickle}all_cit_18.pkl')
    cit_19 = pd.read_pickle(f'{path_pickle}all_cit_19.pkl')
    all_cit = pd.concat([cit_17, cit_18, cit_19], axis=0).reset_index(drop=True)
    return all_cit



