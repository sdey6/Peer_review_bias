import pickle
import pandas as pd
from data_gathering.helper_data_collect import get_title, get_decison, get_rating_text, get_confidence_score, \
    get_confidence_text, format_auth_list, get_age_acc, get_age_rej_a, \
    get_author_age_rej_b
from get_full_display import full_display

pd.options.mode.chained_assignment = None  # default='warn'

path_pickle = 'C:/Users/souri/PycharmProjects/thesis_code/data_gathering/data_pickeled/'

data = pd.read_csv('C:/Users/souri/PycharmProjects/thesis_code/data_gathering/OR_data/iclr2017_papers.csv')
data = data[data.decision != 'Invite to Workshop Track'].reset_index(drop=True)

data['decision'] = data['decision'].apply(lambda x: 'Accept' if x.startswith('Accept') else 'Reject')
data = data[['title', 'authors', 'decision']]
print(data.head())

df_17 = pd.read_excel('C:/Users/souri/PycharmProjects/thesis_code/data_gathering/OR_data/2017_data.xlsx')
col_17 = ['title', 'G', 'decision', 'rate', 'rate1', 'confidence', 'review']
df_17 = df_17[col_17]
df_17 = df_17.rename(columns={'G': 'Date_decison', 'rate1': 'rate_text'})

df_17['title'] = df_17['title'].apply(lambda x: get_title(x))
df_1 = df_17[df_17.decision.isin(['Decision:###Accept (Poster)', 'Decision:###Reject', 'Decision:###Accept (Oral)'])]
df_1.decision = df_1.decision.apply(lambda x: get_decison(x))
df_1.rate_text = df_1.rate_text.astype(str).apply(lambda x: get_rating_text(x))
df_1['confidence_score'] = df_1.confidence.apply(lambda x: get_confidence_score(x))
df_1['confidence_text'] = df_1.confidence.apply(lambda x: get_confidence_text(x))
df_1 = df_1.drop(['Date_decison', 'confidence'], axis=1)
df_1['confidence_score'] = df_1['confidence_score'].apply(lambda x: ast.literal_eval(x))

df_1['year'] = 2017
col_list = ['title', 'decision', 'year', 'rate', 'rate_text', 'review', 'confidence_score', 'confidence_text']
df_1 = df_1[col_list]
df_rev = df_1.groupby(['title', 'year'])[['rate', 'rate_text', 'review',
                                          'confidence_score', 'confidence_text']].agg(list).reset_index()

""" Merging papers with decision and review information"""

df_17_m = data.merge(df_rev, on='title')
df_17_m.title = df_17_m.title.str.replace('#', '')
df_17_m['authors'] = df_17_m['authors'].apply(format_auth_list)
df_17_m = df_17_m.rename(columns={'authors': 'Authors'})
print(df_17_m.head())

# get author information form DBLP

""" Accepted Papers """

df_17_acc = df_17_m[df_17_m.decision == 'Accept'].reset_index(drop=True)
df_17_acc_age, informal_list_acc, not_found_list_acc, error_l_acc = get_age_acc(df_17_acc[2:4])
print('\n######## Accepted papers ###########\n')
print(df_17_acc_age)

""" Rejected Papers """

# rejected paper in ICLR but present in DBLP
df_17_rej = df_17_m[df_17_m.decision == 'Reject'].reset_index(drop=True)
data, informal_list_y, not_found_list_y, error_l_y = get_age_rej_a(df_17_rej[1:7])
print('\n######## All Rejected papers in ICLR ###########\n')
print(data)
data['len_age'] = data['academic_age'].apply(lambda x: len(x))
df_age_rej_n = data[data['len_age'] == 1]
df_age_rej_y = data[data['len_age'] != 1]
print('\n######## Found in DBLP ###########\n')
print(df_age_rej_y)

# rejected paper in ICLR and not present in DBLP
age_rej_n_17, nf_auth_17 = get_author_age_rej_b(df_age_rej_n)
print('\n######## Not found in DBLP ###########\n')
print(age_rej_n_17)

# merger all
df_17_all = pd.concat([df_17_acc_age, df_age_rej_y, age_rej_n_17], axis=0).reset_index(drop=True)
df_17_all = df_17_all.drop('len_age', axis=1)
print('\n######## All Papers from 2017 ###########\n')

col = ['title', 'Authors', 'decision', 'year', 'review', 'rating_score',
       'rating_text', 'confidence_score', 'confidence_text', 'academic_age',
       'current_age']
df_17_all = df_17_all.rename(columns={'rate': 'rating_score', 'rate_text': 'rating_text'})
df_17_all = df_17_all[col]
print(df_17_all)

# pickle the data to avoid long run

pickle.dump(df_17_all, open(f'{path_pickle}all_data_17.pkl', 'wb'))
