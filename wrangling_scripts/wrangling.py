import pandas as pd
pd.options.mode.chained_assignment = None

csv_url = "https://health-infobase.canada.ca/src/data/covidLive/covid19.csv"

df = pd.read_csv(csv_url)
#parse government data so it is usable

def format_dates(df):
    df['dates'] = pd.to_datetime(df['date'], dayfirst = True)
    df['YMD'] = df['dates'].dt.date
    df = df.drop(['date', 'dates', 'prnameFR', 'pruid'], axis = 1)
    #if provinces don't report active cases, assume they have 0, so the data will plot
    df['numactive'].fillna(0.0, inplace = True)
    return df


#List of unique provinces, Canada, ordered alphabetically with Canada first
def unique_provnames():
    provnames = df.prname.unique()
    provnames = list(provnames)
    provnames.pop()
    provnames.sort()
    myorder = [2, 0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    provnames = [provnames[i] for i in myorder]
    return provnames

#function to make province-wise dataset
def make_dataset(pnames, df):
    
    by_prov = pd.DataFrame()

    # Iterate through all the provinces
    for i in pnames:

        # Subset to the province
        sub = df[df['prname'] == i]

        # Add to the overall dataframe
        by_prov = by_prov.append(sub)
    
    return by_prov

#to make barchart dataset, must retrieve data from most recent date only
def make_barchart_dataset(pnames, df):
    df_sub = df[df['prname'].isin(provnames)]
    recent = max(df_sub['YMD'])
    recent_date = df_sub[df_sub['YMD'] == recent]

    return recent_date

#must pivot datasets for linear plot data so prov names are columns
def format_dataset(df, value):
    df_pivot = pd.pivot_table(df,
    columns = 'prname',
    index = 'YMD',
    values = value)
    
    df_pivot = df_pivot.rename_axis(None)

    return df_pivot

#for all data
data = make_dataset(unique_provnames(), format_dates(df))