import pandas as pd
pd.options.mode.chained_assignment = None
import plotly.graph_objs as go

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
def make_barchart_dataset(df):
    recent = max(df['YMD'])
    recent_date = df[df['YMD'] == recent]

    return recent_date

#for all data
#make_dataset(unique_provnames(), format_dates(df))

#Total Cases Figure
def return_total_cases_fig():
    graph = []
    data = make_dataset(unique_provnames(), format_dates(df))
    data = data[['prname', 'YMD', 'numtotal']]
    for region in unique_provnames():
        x_val = data[data['prname'] == region].YMD.tolist()
        y_val = data[data['prname'] == region].numtotal.tolist()
    graph.append(
        go.Scatter(
            x = x_val,
            y = y_val,
            mode = 'lines',
            name = region
        )
    )

    layout = dict(title = "Cumulative COVID-19 Cases by Region",
                    xaxis = dict(title = 'Date'),
                    yaxis = dict(title = 'Number of Cases'),
                )
    
    figures = []
    figures.append(dict(data = graph, layout = layout))

    return figures

#New Cases Figure
def return_new_cases_fig():
    graph = []
    data = make_barchart_dataset(make_dataset(unique_provnames(), format_dates(df)))
    data = data[['prname', 'YMD', 'numtoday', 'percenttoday', 'numtotal_last7', 'ratetotal_last7']]
    