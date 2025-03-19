import pandas as pd

# Read preprocessed data
data = pd.read_csv('final_data.csv', index_col='Unnamed: 0')

# Split data according to category
data_admin = data[data.sect_act_admin == 1.0].reset_index(drop=True)
data_centre_com = data[data.sect_act_centre_com == 1.0].reset_index(drop=True)
data_occup_cont = data[data.sect_act_occup_cont == 1.0].reset_index(drop=True)
data_autre = data[data.sect_act_autre == 1.0].reset_index(drop=True)

# Function for aggregrating
def extract_ts(df: pd.DataFrame, step: str='D'):
    """Return corresponding dataframe averaging the emissions with the surface as weight

    Args:
        df (pd.DataFrame): original data
        step (str, optional): ('D': daily, 'M': monthly, 'Y': yearly). Defaults to 'D'.
    """
    
    df = df.copy()
    
    df.date_etablissement_dpe = pd.to_datetime(df.date_etablissement_dpe)
    
    def weighted_avg(sub_df):
        return (sub_df.surface_utile*sub_df.emission_ges).sum()/sub_df.surface_utile.sum()
    
    df = df.groupby('date_etablissement_dpe').apply(weighted_avg, include_groups=False)
    
    df.sort_index(inplace=True)
    
    df = df['2013':'2024']
    
    df = df.resample(step).interpolate(method='linear')
    
    return df

# Aggregating
ts_admin = extract_ts(data_admin)
ts_centre_com = extract_ts(data_centre_com)
ts_occup_cont = extract_ts(data_occup_cont)
ts_autre = extract_ts(data_autre)
