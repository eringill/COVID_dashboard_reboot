import pandas as pd
#pd.options.mode.chained_assignment = None
import plotly.graph_objs as go
import warnings
warnings.filterwarnings('ignore')

csv_url = "https://health-infobase.canada.ca/src/data/covidLive/vaccination-coverage-map.csv"

df = pd.read_csv(csv_url)

def format_dates(df):
    df['YMD'] = pd.to_datetime(df['week_end'])
    df = df[['YMD', 'prename', 'proptotal_atleast1dose', 'proptotal_fully']]
    return df



#List of unique provinces, Canada, ordered alphabetically with Canada first
def unique_provnames():
    provnames = df.prename.unique()
    provnames = list(provnames)
    provnames.pop()
    provnames.sort()
    myorder = [2, 0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    provnames = [provnames[i] for i in myorder]
    return provnames

def make_dataset(pnames, df):
    
    by_prov = pd.DataFrame()

    # Iterate through all the provinces
    for i in pnames:

        # Subset to the province
        sub = df[df['prename'] == i]

        # Add to the overall dataframe
        by_prov = by_prov.append(sub)
    
    return by_prov

def make_vaccine_dataset():
    data = make_dataset(unique_provnames(), format_dates(df))
    plot_data2 = data[data['prename'] == 'Canada']
    plot_data2 = plot_data2[['YMD', 'proptotal_atleast1dose', 'proptotal_fully']]
    plot_data2['proptotal_atleast1dose'] = (plot_data2['proptotal_atleast1dose'].astype(str)).str.replace('<','')
    plot_data2['proptotal_fully'] = (plot_data2['proptotal_fully'].astype(str)).str.replace('<','')
    plot_data2['proptotal_atleast1dose'] = pd.to_numeric(plot_data2['proptotal_atleast1dose']) 
    plot_data2['proptotal_fully'] = pd.to_numeric(plot_data2['proptotal_fully']) 
    plot_data2 = pd.melt(plot_data2, id_vars= ['YMD'], value_vars = ['proptotal_atleast1dose', 'proptotal_fully'])
    plot_data2["variable"].replace({"proptotal_atleast1dose": "at least one dose", "proptotal_fully": "fully vaccinated"}, inplace=True)
    plot_data2['YMD']= pd.to_datetime(plot_data2['YMD'])
    plot_data2['value'] = pd.to_numeric(plot_data2['value'])

    return plot_data2


#Vaccines Figure
def return_vaccine_fig():
    graph = []
    data = make_vaccine_dataset()
    for vaccine_type in data.variable.unique():
        x_val = data[data['variable'] == vaccine_type].YMD.tolist()
        y_val = data[data['variable'] == vaccine_type].value.tolist()
        graph.append(
            go.Scatter(
                x = x_val,
                y = y_val,
                mode = 'lines',
                name = vaccine_type
            )
        )

    layout = dict(title = "Proportion of Eligible Individuals in Canada <br> Who Have Received Vaccines",
                    xaxis = dict(title = 'Date'),
                    yaxis = dict(title = 'Percent'),
                )
    
    figures = []
    figures.append(dict(data = graph, layout = layout))

    return figures
