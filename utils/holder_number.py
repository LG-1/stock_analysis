

import os
import sys
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd

from .mongo_utils import STOCK_ANALYSIS

ROOT_PTH = os.path.abspath(os.path.join(os.getcwd(), ".."))


class HolderNumber(object):
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        if sys.platform in ['darwin']:
            # macos
            chromedriver_pth = '/Users/liguang/tools/ch_driver/chromedriver'
        elif sys.platform in ['linux']:
            # linux
            chromedriver_pth = '/mnt/f/08_Stock_Analysis/stock_analysis/external_executions/chromedriver'
        else:
            chromedriver_pth = 'F:\\08_Stock_Analysis\\stock_analysis\\external_executions\\chromedriver.exe'

        self.driver = webdriver.Chrome(
            executable_path=chromedriver_pth, options=chrome_options)
        self.holder_number_url_prefix = 'http://f10.eastmoney.com/f10_v2/ShareholderResearch.aspx?code='

    def get_holder_number_table_from_mongo(self, scode):
        res = list(STOCK_ANALYSIS.holder_number.find({"scode": scode}, {"_id": False}))
        if res:
            return pd.DataFrame(res)
        return pd.DataFrame()

    def get_holder_number_table(self, scode, retry_num=5):
        """
        date: 日期
        shareholders: 股东人数(户)
        change_ratio: 较上期变化(%)
        per_shares: 人均流通股(股)
        concentration: 筹码集中度
        price: 股价(元)
        per_holding_amount: 人均持股金额(元)
        total_ratio_ten: 前十大股东持股合计(%)
        total_ratio_ten_public: 前十大流通股东持股合计(%)

        """

        table = pd.DataFrame()
        validate_date = False
        while retry_num:
            try:
                self.driver.get(self.holder_number_url_prefix + scode)
                p_element = self.driver.find_element_by_id(id_='Table0')

                res = {}
                for line in p_element.text.split("\n"):
                    line_split = [self.normalize_numeric(
                        i) for i in line.split(' ')]
                    if validate_date:
                        res[line_split[0]] = line_split[1:]
                    else:
                        validate_date = self.validate_date_str(line_split[-1])
                        if validate_date:
                            res['日期'] = [
                                sp for sp in line_split if self.validate_date_str(sp)]

                table = pd.DataFrame(res)
                if table.shape[1] == 9:
                    table.columns = ['date', 'shareholders',
                                     'change_ratio', 'per_shares', 'concentration', 'price', 'per_holding_amount', 'total_ratio_ten', 'total_ratio_ten_public']
                    table['scode'] = scode
                    table['update_timestamp'] = time.time()
                    return table
                return table

            except Exception as e:
                retry_num -= 1
                print(
                    f"get holder number table failed once for {scode}, reason: {e}")

        print(
            f"get holder number table failed for {scode}, with {retry_num} retrys.")
        return table

    @staticmethod
    def normalize_numeric(numeric_str):
        if numeric_str[-1] == '万':
            numeric_str = str(float(numeric_str[:-1])*10000)
        return numeric_str

    @staticmethod
    def validate_date_str(date_str):
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except Exception as e:
            return False


if __name__ == "__main__":
    scode = 'sz000008'
    hn = HolderNumber()
    table = hn.get_holder_number_table(scode)
    print(table)
