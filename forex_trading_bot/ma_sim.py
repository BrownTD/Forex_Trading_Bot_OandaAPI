import pandas as pd
import utils
import instrument

def is_trade(row):
    if row.DIFF >= 0 and row.DIFF_PREV < 0:
        return 1
    if row.DIFF <= 0 and row.DIFF_PREV > 0:
        return -1
    return 0

def get_ma_col(ma):
    return f'MA_{ma}'

def get_price_data(pairname, granularity):
    df = pd.read_pickle(utils.get_his_data_filename(pairname, granularity))
    
    non_cols = ['time', 'volume']
    mod_cols = [x for x in df.columns if x not in non_cols]
    df[mod_cols] = df[mod_cols].apply(pd.to_numeric)
    return df[['time','mid_c']]
    
def process_data(ma_short, ma_long, price_data):
    ma_list = set(ma_short+ ma_long)
    
    for ma in ma_list:
        price_data[get_ma_col(ma)] = price_data.mid_c.rolling(window=ma).mean()
        
    return price_data
    
def run():
    pairname = 'GBP_JPY'
    granularity = 'H1'
    ma_short = [8,16,32,64]
    ma_long = [32,64,96,128,256]
    i_pair = instrument.Instrument.get_instrument_dict()[pairname]
    
    price_data = get_price_data(pairname, granularity)
    price_data = process_data(ma_short, ma_long, price_data)
    
    print=(price_data)
    
if __name__ == '__main__':
    run()