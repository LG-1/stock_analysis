import copy
import json
import pickle
import requests

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from datetime import datetime, timedelta



def init_datatable_mode():
    """Initialize DataTable mode for pandas DataFrame represenation."""
    from IPython.core.display import display, Javascript

    # configure path to the datatables library using requireJS
    # that way the library will become globally available
    display(Javascript("""
        require.config({
            paths: {
                DT: '//cdn.datatables.net/1.10.19/js/jquery.dataTables.min',
            }
        });
        $('head').append('<link rel="stylesheet" type="text/css" href="//cdn.datatables.net/1.10.19/css/jquery.dataTables.min.css">');
    """))

    def _repr_datatable_(self):
        """Return DataTable representation of pandas DataFrame."""
        # classes for dataframe table (optional)
        classes = ['table', 'table-striped', 'table-bordered']

        # create table DOM
        script = (
            f'$(element).html(`{self.to_html(index=False, classes=classes)}`);\n'
        )

        # execute jQuery to turn table into DataTable
        script += """
            require(["DT"], function(DT) {
                $(document).ready( () => {
                    // Turn existing table into datatable
                    $(element).find("table.dataframe").DataTable();
                })
            });
        """

        return script

    pd.DataFrame._repr_javascript_ = _repr_datatable_


def read_pickle(pth):
    with open(pth, "rb") as fin:
        return pickle.load(fin)
    
def write_pickle(obj, pth):
    with open(pth, 'wb') as fout:
        pickle.dump(obj, fout)


def inf2zero(arr):
    from numpy import inf
    arr[arr == inf] = 0
    arr[arr == -inf] = 0
    return arr

def round_float(x):
    try:
        return round(float(x), 2)
    except Exception as e:
        print(x)
        print(e)
        

def get_Institutional_research(report_date, pagesize=5000, page=1):
    point_date = str(datetime.strptime(report_date, "%Y-%m-%d") - timedelta(days=180)).split()[0]
    total_pages = 1
    df = pd.DataFrame()
    while page <= total_pages:
        print(f"getting page: {page}")
        dataurl = f"http://data.eastmoney.com/DataCenter_V3/jgdy/gsjsdy.ashx?pagesize={pagesize}&page={page}"
        res = json.loads(requests.get(dataurl).text)
        total_pages = int(res.get("pages", 1))
        temp= pd.DataFrame(pd.DataFrame(res['data']))
        if 'NoticeDate' in temp.columns:
            df = pd.concat([df, temp[temp['NoticeDate'] > point_date]])
        page += 1
    
    df['OrgSum'] = df['OrgSum'].astype(int)
    df = df.groupby('SCode').agg({"SCode": np.count_nonzero, "OrgSum": sum}).rename(columns={"SCode": "OrgCount"})
    return df

    

class GetConceptClassified(object):
    def __init__(self):
        self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36"
        self.concept_index_url = "http://q.10jqka.com.cn/gn/detail"
        self.industry_index_url = "http://q.10jqka.com.cn/thshy/"
        
    def get_indexs(self, url, flag_text):
        res = requests.get(url, headers={'User-Agent': self.user_agent})
        concept_index_html = res.content
        groups = []
        keep_code = []
        html_bs = BeautifulSoup(concept_index_html)
        for tag in html_bs.find_all('a'):
            temp = {}
            if flag_text in str(tag):
                temp['GCode'] = tag.attrs['href'].split('/')[-2]
                temp['GName'] = tag.get_text()
                
                if temp['GCode'] not in keep_code:
                    keep_code.append(temp['GCode'])
                    groups.append(temp)
                
        return groups
    
    def get_gn_stocks(self, url):
        
        gn_stocks = []
        stock_html_bs = BeautifulSoup(requests.get(url, headers={'User-Agent': self.user_agent}).content)
        for tt in stock_html_bs.find_all('tr')[1:]:
            temp = {}
            temp['SCode'] = tt.get_text().split('\n')[2]
            temp['SName'] = tt.get_text().split('\n')[3]
            gn_stocks.append(temp)

        return gn_stocks
    
    def get_industry_classified(self):
        industrys = self.get_indexs(self.industry_index_url, 'thshy/detail/code')
        industry_classifiers = []
        for industry in industrys:
            url = f"http://q.10jqka.com.cn/thshy/detail/page/1/ajax/1/size/3000/code/{industry['GCode']}/"
            stocks = self.get_gn_stocks(url)
            for stock in stocks:
                temp = copy.deepcopy(industry)
                temp['SCode'] = stock['SCode']
                temp['SName'] = stock['SName']
                
                industry_classifiers.append(temp)
                
        return industry_classifiers
    
    def get_concept_classified(self):
        concepts = self.get_indexs(self.concept_index_url, 'gn/detail/code')
        
        concept_classifiers = []
        for concept in concepts:
            url = f"http://q.10jqka.com.cn/gn/detail/page/1/ajax/1/size/3000/code/{concept['GCode']}/"
            stocks = self.get_gn_stocks(url)
            
            if len(stocks) < 220:
                # if too much stocks in one concept, will ignore it,
                for stock in stocks:
                    temp = copy.deepcopy(concept)
                    temp['SCode'] = stock['SCode']
                    temp['SName'] = stock['SName']
                    concept_classifiers.append(temp)
                
        return concept_classifiers
    
