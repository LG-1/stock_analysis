import tushare as ts
ts.set_token('ad00beec7ad536862e87da4da49a6a95a1385973009fc949d16f1d94')
ts = ts.pro_api()

def get_all_codes():
    all_stock_df = ts.stock_basic()
    all_codes = [ts_code.split('.')[1].lower()+ts_code.split('.')[0]
                 for ts_code in all_stock_df['ts_code'].values]
    return all_codes
