import re

from unidecode import unidecode
import requests
from bs4 import BeautifulSoup
import urllib.request
import ast
import time
from serpapi import GoogleSearch

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
}
not_found_list = []
informal_list = []
a = []
b = []
a1 = []
b1 = []
a2 = []
b2 = []
list_t = []
list_c = []
list_j = []
list_i = []
error_l = []


# get the reviews from OR JSON format for 2018
def get_reviews(data):
    reviews = []
    for submission in data:
        reviews = reviews + [
            dict(reply['content'], **{'Title': submission.content['title'], 'Authors': submission.content['authors']
                                      })
            for reply in submission.details["directReplies"] if
            reply["invitation"].endswith("Official_Review")]
    return reviews


# helper function to get the final decision of each paper
def get_decision(data):
    decisions = []
    for submission in data:
        decisions = decisions + [
            dict(reply['content'], **{'Title': submission.content['title'],
                                      'Authors': submission.content['authors']})
            for reply in submission.details["directReplies"]
            if reply["invitation"].endswith("Decision")]
    return decisions


def get_decision_19(data):
    decisions = []
    for submission in data:
        decisions = decisions + [
            dict(reply['content'], **{'Title': submission.content['title'],
                                      'Authors': submission.content['authors']})
            for reply in submission.details["directReplies"]
            if reply["invitation"].endswith("Meta_Review")]
    return decisions


def get_reviews_19(data):
    reviews = []
    for submission in data:
        reviews = reviews + [
            dict(reply['content'], **{'Title': submission.content['title'], 'Authors': submission.content['authors']
                                      })
            for reply in submission.details["directReplies"] if
            reply["invitation"].endswith("Official_Review")]
    return reviews


def get_age(url, year):
    page_auth = requests.get(url, headers=headers)
    soup_auth = BeautifulSoup(page_auth.content, "html.parser")
    year_range = BeautifulSoup(str(soup_auth.find_all(class_='year')),
                               features="lxml").get_text()
    year_range = (ast.literal_eval(year_range))
    year_range.sort(reverse=True)
    end_year = year_range[0]
    start_year = year_range[-1]
    current_age = end_year - start_year + 1
    academic_age = year - start_year + 1
    return current_age, academic_age


def get_age_acc(data):
    """Helper function to get the current and academic age of the authors
    from DBLP for the accepted papers"""
    not_found_list = []
    informal_list = []
    a = []
    b = []
    error_l = []
    for i, j in data.iterrows():
        aa_list = []
        ca_list = []
        try:
            title = j['title']
            # print(title)
            paper_pub_year = j['year']
            html_text = unidecode(title)
            url = 'https://dblp.org/search/publ?q=' + html_text
            url = url.replace(" ", "%20")
            req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
            response = urllib.request.urlopen(req)
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')

            # Check if the title from OR is present in DBLP by the url

            match_title_str = soup.find("p", {"id": "completesearch-info-matches"}).get_text()
            if match_title_str == 'no matches':
                not_found_list.append(title)
                aa_list.append('title not found')
                ca_list.append('title not found')
            else:  # if the match is found proceed with scrapping
                # print(f"\nRecord found in DBLP for the paper: {html_text}\n")
                # print(f"::::::Details scrapped for the paper is as below::::::\n")
                li = soup.find("li", {"class": "entry inproceedings toc"})  # Filtering conference and workshop papers
                if li is None:
                    informal_list.append(title)
                    aa_list.append('only informal')
                    ca_list.append('only informal')
                else:
                    li_class = soup.find("li", {"class": "entry inproceedings toc"})['class']
                    if ' '.join(li_class) == 'entry inproceedings toc':
                        v = li.select("cite.tts-content a")
                        for elem in v:
                            if elem.find('span', {'itemprop': 'isPartOf'}) is None:
                                pid_url = elem.get('href')
                                current_age, academic_age = get_age(pid_url, paper_pub_year)
                                aa_list.append(academic_age)
                                ca_list.append(current_age)
                                time.sleep(2)
        except:
            error_l.append(j['title'])
            aa_list.append('skipped')
            ca_list.append('skipped')
            continue
        finally:
            a.append(aa_list)
            b.append(ca_list)
    data['academic_age'] = a
    data['current_age'] = b
    return data, informal_list, not_found_list, error_l


def get_age_rej_a(data):
    """Helper function to get the current and academic age of the authors for the papers which are
    rejected in ICLR but present in DBLP"""
    not_found_list = []
    informal_list = []
    a = []
    b = []
    a1 = []
    b1 = []
    a2 = []
    b2 = []
    error_l = []
    for i, j in data.iterrows():
        aa_list = []
        ca_list = []
        try:
            title = j['title']
            # print(title)
            paper_pub_year = j['year']
            html_text = unidecode(title)
            url = 'https://dblp.org/search/publ?q=' + html_text
            url = url.replace(" ", "%20")
            req = urllib.request.Request(url, headers={'User-Agent': "Magic Browser"})
            response = urllib.request.urlopen(req)
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')

            # Check if the title from OR is present in DBLP by the url

            match_title_str = soup.find("p", {"id": "completesearch-info-matches"}).get_text()
            if match_title_str == 'no matches':
                not_found_list.append(title)
                aa_list.append('title not found')
                ca_list.append('title not found')
            else:  # if the match is found proceed with scrapping
                li = soup.find("li", {"class": "entry inproceedings toc"})  # Filtering conference and workshop papers
                if li is None:
                    informal_list.append(title)
                    li_inf_class = soup.find("li", {"class": "entry informal toc"})['class']
                    li_inf = soup.find("li", {"class": "entry informal toc"})
                    if ' '.join(li_inf_class) == 'entry informal toc':
                        v = li_inf.select("cite.tts-content a")
                        for elem in v:
                            if elem.find('span', {'itemprop': 'isPartOf'}) is None:
                                pid_url = elem.get('href')
                                current_age, academic_age = get_age(pid_url, paper_pub_year)
                                aa_list.append(academic_age)
                                ca_list.append(current_age)
                else:
                    li_class = soup.find("li", {"class": "entry inproceedings toc"})['class']
                    if ' '.join(li_class) == 'entry inproceedings toc':
                        v = li.select("cite.tts-content a")
                        for elem in v:
                            if elem.find('span', {'itemprop': 'isPartOf'}) is None:
                                pid_url = elem.get('href')
                                current_age, academic_age = get_age(pid_url, paper_pub_year)
                                aa_list.append(academic_age)
                                ca_list.append(current_age)
                                time.sleep(1)
        except:
            error_l.append(j['title'])
            aa_list.append('skipped')
            ca_list.append('skipped')
            continue
        finally:
            a1.append(aa_list)
            b1.append(ca_list)
    data['academic_age'] = a1
    data['current_age'] = b1
    return data, informal_list, not_found_list, error_l


def get_author_age_rej_b(df):
    not_found_list = []
    informal_list = []
    a2 = []
    b2 = []
    """Helper function to get the current and academic age of the authors for the papers which are
        rejected in ICLR and not present in DBLP"""
    for i, j in df.iterrows():
        author_list = j['Authors']
        aa_list = []
        ca_list = []
        # print(j['title'])
        year = j['year']
        try:
            for author_name in author_list:
                time.sleep(2)
                url = 'https://dblp.org/search/author?q=' + author_name
                url = url.replace(" ", "%20")
                rawpage = requests.get(url, headers=headers)
                soup = BeautifulSoup(rawpage.content, "lxml")
                x = soup.findAll('div', attrs={'id': 'completesearch-authors'})
                if len(x) == 0:  # for only one match
                    year_range = BeautifulSoup(str(soup.find_all(class_='year')),
                                               features="lxml").get_text()
                    year_range = (ast.literal_eval(year_range))
                    year_range.sort(reverse=True)
                    end_year = year_range[0]
                    start_year = year_range[-1]
                    current_age = end_year - start_year + 1
                    academic_age = year - start_year + 1
                    aa_list.append(academic_age)
                    ca_list.append(current_age)
                else:  # for multiple/no match
                    for y in x:
                        match_finder = y.find('div', attrs={'class': 'body hide-body'}).find('p').get_text()
                        if match_finder == 'no matches':  # for no match
                            aa_list.append('no_match')
                            ca_list.append('no_match')
                            not_found_list.append(author_name)
                        elif match_finder == 'Exact matches':  # multiple match
                            x_count = y.find('ul', attrs={'class': 'result-list'})
                            if len(x_count) == 1:  # for multiple match but exact one
                                x_link = y.find('ul', attrs={'class': 'result-list'}).find('a').get('href')
                                current_age, academic_age = get_age(x_link, year)
                                aa_list.append(academic_age)
                                ca_list.append(current_age)
                            else:  # for multiple match but combination
                                auth_present_mm = get_auth_present(author_list)
                                pid_url = get_comb_url(auth_present_mm, author_name)
                                if pid_url != 0:
                                    ca_age, aa_age = get_age(pid_url, year)
                                    # print(aa_age, ca_age)
                                    aa_list.append(aa_age)
                                    ca_list.append(ca_age)
                                else:
                                    aa_list.append('no_match')
                                    ca_list.append('no_match')
        except:
            aa_list.append('skipped')
            ca_list.append('skipped')
            continue
        finally:
            a2.append(aa_list)
            b2.append(ca_list)
    df['academic_age'] = a2
    df['current_age'] = b2
    return df, not_found_list


def get_auth_present(auth_list):
    present_list = []
    # print(auth_list)
    for i in auth_list:
        url = 'https://dblp.org/search/author?q=' + i
        url = url.replace(" ", "%20")
        rawpage = requests.get(url, headers=headers)
        soup = BeautifulSoup(rawpage.content, "html.parser")
        x = soup.findAll('div', attrs={'id': 'completesearch-authors'})
        if len(x) == 0:
            present_list.append(i)
        else:
            for y in x:
                match_finder = y.find('div', attrs={'class': 'body hide-body'}).find('p').get_text()
                if match_finder != 'no matches':
                    present_list.append(i)
    return present_list


def get_comb_url(auth_list, auth_name):
    str_comb = get_str_com(auth_list, auth_name)
    url_comb = 'https://dblp.org/search?q=' + str_comb
    url_comb = url_comb.replace(" ", "%20")
    # print('Joint URL: ', url_comb)
    page = requests.get(url_comb, headers=headers)
    soup_comb = BeautifulSoup(page.content, "html.parser")
    # pub_list = soup_comb.findAll("ul", {"class": "publ-list"})
    try:

        x = soup_comb.findAll('cite', attrs={'class': 'data tts-content'})  # Chenghao Liu

        a_l = []
        if len(x) != 0:
            for j in x:
                v = j.select("cite.tts-content a")
                for elem in v:
                    author_name = elem.find('span', {'itemprop': 'name'}).get_text(',', strip=True)
                    if author_name.strip().startswith(auth_name.strip()):
                        # print(author_name)
                        pid_url = elem.get('href')

                        a_l.append(pid_url)

            return a_l[0]
        else:
            return 0

    except:
        return 0


def get_str_com(list_a, name):
    auth_name_ind = list_a.index(name)
    if auth_name_ind != 0:
        fa_comb = list_a[0] + ' ' + name
        return fa_comb
    else:
        fa_comb = list_a[1] + ' ' + name
        return fa_comb


def get_title(title):
    title_l = title.split('|')[0].strip()
    return title_l


def get_decison(dec):
    new_dec = dec.split(':###')[-1]
    return new_dec


def get_rating_text(r_text):
    txt = r_text.split(':')[-1].strip()
    return txt


def get_confidence_score(conf):
    conf_score = re.split(':###|:', conf)[1]
    return conf_score


def get_confidence_text(conf):
    conf_score = re.split(':###|:', conf)[-1].strip()
    return conf_score


def format_auth_list(auth_names):
    new_list = auth_names.split(',')
    new_list = [i.strip() for i in new_list]
    return new_list


data = []
api_key = '36ecb01c3a0c68599c26713ff536f824ea38cef953ec5ab293883f5305b34c1d'


def get_citation(key, t_list):
    for title in t_list:
        print(title)
        params = {
            'engine': "google_scholar",
            'q': title,
            'exactTerms': title,
            'api_key': key,
            'start': 0
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        try:
            for result in results['organic_results']:
                try:
                    file_title = result['title']
                except:
                    file_title = None
                try:
                    cited_by_count = int(result['inline_links']['cited_by']['total'])
                except:
                    cited_by_count = None
                data.append({
                    'title': file_title,
                    'cited_by_count': cited_by_count
                })
        except:
            data.append({
                'title': title,
                'cited_by_count': 'No result'
            })

    return data
