import pandas as pd
from sklearn.model_selection import train_test_split


# Split data according to category
def split(data):
    data_admin = data[data.sect_act_admin == 1.0].reset_index(drop=True).iloc[:, :-4]
    data_centre_com = data[data.sect_act_centre_com == 1.0].reset_index(drop=True).iloc[:, :-4]
    data_occup_cont = data[data.sect_act_occup_cont == 1.0].reset_index(drop=True).iloc[:, :-4]
    data_autre = data[data.sect_act_autre == 1.0].reset_index(drop=True).iloc[:, :-4]
    data_dict = {'admin': data_admin, 
                 'centre_com': data_centre_com, 
                 'occup_cont': data_occup_cont, 
                 'autre': data_autre}
    return data_dict


# First method
def extract_ts(df: pd.DataFrame, freq: str='D'):
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
    
    if freq == 'D':
        df = df.resample(freq).interpolate(method='linear')
    else:
        df = df.resample(freq).mean().resample(freq).interpolate(method='linear')
    
    return df


# Second method
def extract_vect_ts(df, freq='D'):
    df_1, df_2 = df[['date_etablissement_dpe', 'emission_ges', 'surface_utile']], df.drop(columns='emission_ges')

    def weighted_avg(sub_df):
            return (sub_df.surface_utile*sub_df.emission_ges).sum()/sub_df.surface_utile.sum()
        
    ts_1 = df_1.groupby('date_etablissement_dpe').apply(weighted_avg, include_groups=False).sort_index()

    ts_2 = df_2.groupby(by='date_etablissement_dpe').agg({
        'annee_construction': 'mean', 
        'surface_utile': 'mean', 
        'coord_x': 'mean', 
        'coord_y': 'mean', 
    }).sort_index()

    ts = pd.concat([ts_2, ts_1], axis=1).rename(columns={0: 'emission_ges'})['2013':'2024']
    
    if freq == 'D':
        ts = ts.resample(freq).interpolate(method='linear')
    else:
        ts = ts.resample(freq).mean().resample(freq).interpolate(method='linear')
    
    return ts


# Train test split
def ttsplit(ts, test_size: float=0.25):
    ts_train, ts_test = train_test_split(ts, test_size=test_size, shuffle=False)
    return ts_train, ts_test


# Rolling average
def rolling_average(df, window: int=10):
    return df.rolling(window=window, min_periods=1).mean()


# Etend train to test
def extend_train(train, test):
    test_start = test.index[0]
    train_extended= pd.concat([train, pd.Series(test.iloc[0], index=[test_start])])
    return train_extended


# Singular points of a graph
def singularities(x, y, tol):
    singu = []
    for i in range(1, len(y)-1):
        if abs(((y[i+1] - y[i])/(x[i+1] - x[i])) - ((y[i] - y[i-1])/(x[i] - x[i-1])))>tol:
            singu.append([x[i], y[i]])
    return singu
