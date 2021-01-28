from datetime import datetime, timedelta

import tushare as ts
# ts.set_token('ad00beec7ad536862e87da4da49a6a95a1385973009fc949d16f1d94')
pro = ts.pro_api()


def get_stock_exchange_data(scode, days=720):
    """
    包含股票交易数据及融资融券日线数据.
    """
    mock_today = (datetime.now()+timedelta(days=1)).strftime('%Y%m%d')
    start_date = (datetime.strptime(mock_today, '%Y%m%d') - timedelta(days=days)).strftime('%Y%m%d')
    end_date = (datetime.strptime(mock_today, '%Y%m%d')).strftime('%Y%m%d')
    
    daily_df = pro.daily(ts_code=scode, start_date=start_date)
    margin_df = pro.margin_detail(start_date=start_date, ts_code=scode)
    stock_details = daily_df.merge(margin_df, on=['trade_date', 'ts_code'], how='left').fillna(0)
    stock_details['rz-rq-ce'] = stock_details['rzye'] - stock_details['rqye']
    stock_details = stock_details.rename(columns={'ts_code': 'scode'})
    
    return stock_details


def get_all_codes():
    all_stock_df = pro.stock_basic()
    all_codes = [number_dot_upper2lower_number(ts_code)
                 for ts_code in all_stock_df['ts_code'].values]
    return all_codes

def number_dot_upper2lower_number(ts_code):
    """
    convert 000001.SZ to sz000001
    
    """
    splits = ts_code.split('.')
    new_code = splits[1].lower()+splits[0]
    return new_code

def lower_number2number_dot_upper(ts_code):
    """
    convert sz000001 to 000001.SZ
    
    """
    new_code = ts_code[2:]+'.'+ts_code[:2].upper()
    return new_code


if __name__ == "__main__":
    daily_df = get_stock_exchange_data('600438.SH')
    print(daily_df.shape)