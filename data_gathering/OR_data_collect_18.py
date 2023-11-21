import openreview
import pickle
import re
import pandas as pd
from data_gathering.helper_data_collect import get_decision, get_reviews, get_age_acc, get_age_rej_a, \
    get_author_age_rej_b
from get_full_display import full_display
pd.options.mode.chained_assignment = None  # default='warn'

path_pickle = 'C:/Users/souri/PycharmProjects/thesis_code/data_gathering/data_pickeled/'

''''the pickle files in OR data can be used instead of running the APIs'''

# guest_client = openreview.Client(baseurl='https://api.openreview.net')
# submissions = guest_client.get_all_notes(invitation="ICLR.cc/2018/Conference/-/Blind_Submission",
# details='directReplies')
# with open('C:/Users/souri/PycharmProjects/thesis_code/data_gathering/OR_data/submission_OR_18.pkl', 'wb') as f:
# pickle.dump(submissions, f)
data = pickle.load(open('C:/Users/souri/PycharmProjects/thesis_code/data_gathering/OR_data/submission_OR_18.pkl',
                        'rb'))  # using pickle file

# collect and merge data related to decision and reviews from OR

decisions_18 = get_decision(data)
decisions_18 = pd.DataFrame(decisions_18)
decisions_18 = decisions_18[['Title', 'Authors', 'decision', ]]
decisions_18['year'] = 2018

reviews = get_reviews(data)  # get the reviews of the papers
df_rev = pd.DataFrame(reviews)
df_rev = df_rev[['Title', 'Authors', 'review', 'rating', 'confidence']]
df_rev['rating_score'] = df_rev['rating'].apply(lambda x: x.split(':')[0]).astype(int)
df_rev['rating_text'] = df_rev['rating'].apply(lambda x: x.split(':')[-1])
df_rev['confidence_score'] = df_rev['confidence'].apply(lambda x: x.split(':')[0]).astype(int)
df_rev['confidence_text'] = df_rev['confidence'].apply(lambda x: x.split(':')[-1])
df_rev = df_rev.drop(['rating', 'confidence', 'Authors'], axis=1)
df_rev = df_rev.groupby(['Title'])[df_rev.columns.tolist()[1:]].agg(list)
df_rev = df_rev.reset_index()
df_18_m = decisions_18.merge(df_rev, on='Title')
df_18_m = df_18_m.rename(columns={'Title': 'title'})
df_18_m = df_18_m[df_18_m.decision != 'Invite to Workshop Track'].reset_index(drop=True)
df_18_m['decision'] = df_18_m['decision'].apply(lambda x: 'Accept' if x.startswith('Accept') else 'Reject')
print('\n ######## Papers with review information ########\n')
print(df_18_m.head())

# Starting of gathering author data from DBLP

# accepted paper

df_18_acc = df_18_m[df_18_m.decision == 'Accept'].reset_index(drop=True)
df_18_acc_age, informal_list_acc, not_found_list_acc, error_l_acc = get_age_acc(df_18_acc[2:4])
print('\n######## Accepted papers ###########\n')
print(df_18_acc_age)

# rejected paper in ICLR but present in DBLP

df_18_rej = df_18_m[df_18_m.decision == 'Reject'].reset_index(drop=True)
data, informal_list_y, not_found_list_y, error_l_y = get_age_rej_a(df_18_rej[1:7])
print('\n######## All Rejected papers in ICLR ###########\n')
print(data)
data['len_age'] = data['academic_age'].apply(lambda x: len(x))
df_age_rej_n = data[data['len_age'] == 1]
df_age_rej_y = data[data['len_age'] != 1]

print('\n######## Found in DBLP ###########\n')
print(df_age_rej_y)

# rejected paper in ICLR and not present in DBLP

age_rej_n_18, nf_auth_18 = get_author_age_rej_b(df_age_rej_n)
print('\n######## Not found in DBLP ###########\n')
print(age_rej_n_18)
df_18_all = pd.concat([df_18_acc_age,df_age_rej_y, age_rej_n_18], axis=0).reset_index(drop=True)
df_18_all = df_18_all.drop('len_age',axis=1)
print('\n######## All Papers from 2018 ###########\n')
print(df_18_all)

# pickle the data to avoid long run

pickle.dump(df_18_all, open(f'{path_pickle}all_data_18.pkl', 'wb'))



