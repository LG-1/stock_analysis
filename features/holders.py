import pandas as pd


def holder_num_score(holders_df: pd.DataFrame, paras: list = [0.5, 0.3, 0.2]) -> float:
    """
    holders_df: input a df contain date and shareholders values.
    output a score of holder num change status.
    """
    holder_nums = []
    total_score = 0.0

    if not holders_df.empty and 'date' in holders_df.columns and 'shareholders' in holders_df.columns:
        holders_df['shareholders'] = holders_df['shareholders'].astype(float)
        holder_nums = holders_df.sort_values('date', ascending=False)['shareholders'].values

    for i in range(len(holder_nums) - 1):
        if i < len(paras):
            total_score += (-100 * (holder_nums[i] - holder_nums[i + 1])/holder_nums[i + 1]) * paras[i]

    res = round(total_score, 2)
    print(res)
    
    return res


if __name__ == "__main__":
    test_data = {'date': {0: '2020-09-30',
                        1: '2020-06-30',
                        2: '2020-03-31',
                        3: '2020-01-31',
                        4: '2019-12-31',
                        5: '2019-09-30',
                        6: '2019-06-30',
                        7: '2019-03-31',
                        8: '2019-02-28',
                        9: '2018-12-31'},
                        'shareholders': {0: '351400.0',
                        1: '431000.0',
                        2: '397400.0',
                        3: '340900',
                        4: '322900.0',
                        5: '300000.0',
                        6: '321900.0',
                        7: '354500.0',
                        8: '369099',
                        9: '429400.0'},
                        'scode': {0: 'sz000001',
                        1: 'sz000001',
                        2: 'sz000001',
                        3: 'sz000001',
                        4: 'sz000001',
                        5: 'sz000001',
                        6: 'sz000001',
                        7: 'sz000001',
                        8: 'sz000001',
                        9: 'sz000001'}}
    test_df = pd.DataFrame(test_data)
    holder_num_score(test_df, [0.4, 0.3, 0.2, 0.1])