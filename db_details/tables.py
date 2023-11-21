sql_pub_table = """ CREATE TABLE IF NOT EXISTS Paper (
                                        paper_id INTEGER PRIMARY KEY,                             
                                        title varchar,
                                        Authors varchar,
                                        decision varchar,
                                        year varchar); """

sql_review_table = """ CREATE TABLE IF NOT EXISTS Reviews (
                                        review_id INTEGER PRIMARY KEY,
                                        paper_id INTEGER,                             
                                        title varchar,
                                        rating_score varchar,
                                        confidence_score varchar, 
                                        review varchar,     
                                        UNIQUE (review_id, paper_id),
                                        FOREIGN KEY (paper_id)
                                        REFERENCES Paper (paper_id)); """

sql_auth_table = """ CREATE TABLE IF NOT EXISTS Authors (    
                                        author_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        paper_id INTEGER ,
                                        Authors varchar,
                                        academic_age int,
                                        current_age int,
                                        total_num_pub int,                                            
                                        UNIQUE (paper_id, Authors),
                                        FOREIGN KEY (paper_id)
                                        REFERENCES Paper (paper_id)); """

sql_citation_table = """ CREATE TABLE IF NOT EXISTS Citation (    
                                        citation_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        paper_id INTEGER ,
                                        title VARCHAR,
                                        cited_by_count varchar ,
                                        FOREIGN KEY (paper_id)
                                        REFERENCES Paper (paper_id)); """