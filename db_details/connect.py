import ast
import csv

from data_gathering.make_features_for_DB import get_paper_feature, get_review_feature, get_author_feature, \
    get_cit_feature
from tables import sql_citation_table, sql_pub_table, sql_review_table, sql_auth_table
from helpers import create_table, create_connection
import pandas as pd

path_csv = 'C:/Users/souri/PycharmProjects/thesis_code/db_details/'

# create a db_details connection
conn = create_connection('test_database.db')

# create tables
if conn is not None:
    # create Publications table
    create_table(conn, sql_pub_table)
    print("Table created successfully")
    df_pub = get_paper_feature()
    df_pub.to_csv(f'{path_csv}paper.csv', index=False)
    paper_data = pd.read_csv(f'{path_csv}paper.csv')
    print(paper_data.head())
    paper_data.to_sql('Paper', conn, if_exists='append', index=False)

    create_table(conn, sql_review_table)
    print("Table created successfully")
    df_rev = get_review_feature()
    df_rev.to_csv(f'{path_csv}review.csv', index=False)
    review_data = pd.read_csv(f'{path_csv}review.csv')
    print(review_data.head())
    review_data.to_sql('Reviews', conn, if_exists='append', index=False)

    create_table(conn, sql_auth_table)
    print("Table created successfully")
    df_auth = get_author_feature()
    df_auth.to_csv(f'{path_csv}author.csv', index=False)
    auth_data = pd.read_csv(f'{path_csv}author.csv')
    print(auth_data.head())
    auth_data.to_sql('Authors', conn, if_exists='append', index=False)

    create_table(conn, sql_citation_table)
    print("Table created successfully")
    df_cit = get_cit_feature()
    df_cit.to_csv(f'{path_csv}cit.csv', index=False)
    cit_data = pd.read_csv(f'{path_csv}cit.csv')
    print(cit_data.head())
    cit_data.to_sql('Citation', conn, if_exists='append', index=False)

conn.close()
print("sqlite connection is closed")
