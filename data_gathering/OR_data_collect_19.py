import openreview
import pickle
import re
import pandas as pd
from data_gathering.helper_data_collect import get_decision_19, get_reviews_19, get_age_acc, get_age_rej_a, \
    get_author_age_rej_b
from get_full_display import full_display
pd.options.mode.chained_assignment = None  # default='warn'

path_pickle = 'C:/Users/souri/PycharmProjects/thesis_code/data_gathering/data_pickeled/'

# guest_client = openreview.Client(baseurl='https://api.openreview.net')
# submissions = guest_client.get_all_notes(invitation="ICLR.cc/2019/Conference/-/Blind_Submission",
# details='directReplies')
# with open('C:/Users/souri/PycharmProjects/thesis_code/data_gathering/OR_data/submission_OR_19.pkl', 'wb') as f:
# pickle.dump(submissions, f)
data = pickle.load(open('C:/Users/souri/PycharmProjects/thesis_code/data_gathering/OR_data/submission_OR_19.pkl',
                        'rb'))  # using pickle file

# collect and merge data related to decision and reviews from OR
""" Decision """
df_decisions_19 = get_decision_19(data)
df_decisions_19 = pd.DataFrame(df_decisions_19)
df_decisions_19 = df_decisions_19[['Title', 'Authors', 'recommendation']]
df_decisions_19['year'] = 2019
df_decisions_19 = df_decisions_19.rename(columns={'recommendation': 'decision'})

""" Reviews """
df_review_19 = pd.DataFrame(get_reviews_19(data))
df_review_19 = df_review_19[['Title', 'Authors', 'review', 'rating', 'confidence']]
df_review_19['rating_score'] = df_review_19['rating'].apply(lambda x: x.split(':')[0]).astype(int)
df_review_19['rating_text'] = df_review_19['rating'].apply(lambda x: x.split(':')[-1])
df_review_19['confidence_score'] = df_review_19['confidence'].apply(lambda x: x.split(':')[0]).astype(int)
df_review_19['confidence_text'] = df_review_19['confidence'].apply(lambda x: x.split(':')[-1])
df_review_19 = df_review_19.drop(['rating', 'confidence', 'Authors'], axis=1)

df_review_19 = df_review_19.groupby(['Title'])[df_review_19.columns.tolist()[1:]].agg(list)
df_review_19 = df_review_19.reset_index()

""" Merging papers with decision and review information"""
df_19_m = df_decisions_19.merge(df_review_19, on='Title')
df_19_m['decision'] = df_19_m['decision'].apply(lambda x: 'Accept' if x.startswith('Accept') else 'Reject')
df_19_m = df_19_m.rename(columns={'Title': 'title'})
print(df_19_m.head())

# get author information form DBLP

""" Accepted Papers """

df_19_acc = df_19_m[df_19_m.decision == 'Accept'].reset_index(drop=True)
df_19_acc_age, informal_list_acc, not_found_list_acc, error_l_acc = get_age_acc(df_19_acc[2:4])
print('\n######## Accepted papers ###########\n')
print(df_19_acc_age)

""" Rejected Papers """

# rejected paper in ICLR but present in DBLP
df_19_rej = df_19_m[df_19_m.decision == 'Reject'].reset_index(drop=True)
data, informal_list_y, not_found_list_y, error_l_y = get_age_rej_a(df_19_rej[1:7])
print('\n######## All Rejected papers in ICLR ###########\n')
print(data)
data['len_age'] = data['academic_age'].apply(lambda x: len(x))
df_age_rej_n = data[data['len_age'] == 1]
df_age_rej_y = data[data['len_age'] != 1]
print('\n######## Found in DBLP ###########\n')
print(df_age_rej_y)

# rejected paper in ICLR and not present in DBLP
age_rej_n_19, nf_auth_19 = get_author_age_rej_b(df_age_rej_n)
print('\n######## Not found in DBLP ###########\n')
print(age_rej_n_19)

# merger all
df_19_all = pd.concat([df_19_acc_age,df_age_rej_y, age_rej_n_19], axis=0).reset_index(drop=True)
df_19_all = df_19_all.drop('len_age',axis=1)
print('\n######## All Papers from 2019 ###########\n')
print(df_19_all)

# pickle the data to avoid long run

pickle.dump(df_19_all, open(f'{path_pickle}all_data_19.pkl', 'wb'))