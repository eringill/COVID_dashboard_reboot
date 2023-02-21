import pandas as pd
pd.options.mode.chained_assignment = None
import plotly.graph_objs as go
import requests
import pandas as pd
import datetime as dt

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

    layout = dict(title="Cumulative COVID-19 Cases by Region",
                  xaxis=dict(title='Date'),
                  yaxis=dict(title='Cumulative Cases by Region'),
                  updatemenus=[dict(buttons=list([
                      dict(label="Linear",
                           method="relayout",
                           args=[{"yaxis.type": "linear"}]),

                      dict(label="Log",
                           method="relayout",
                           args=[{"yaxis.type": "log"}]),
                  ]),
                  )])
    figures = []
    figures.append(dict(data = graph, layout = layout))

    return figures

#New Cases Figures
def return_new_cases_fig():
    data = make_barchart_dataset(make_dataset(unique_provnames(), format_dates(df)))
    data = data[['prname', 'YMD', 'numtotal_last7', 'ratetotal_last7']]

    graph_three = []
    graph_three.append(
        go.Bar(
            x = data.prname.tolist(),
            y = data.numtotal_last7.tolist(),
        )
    )

    layout_three = dict(title = 'New Cases in Last 7 Days By Region',
                            xaxis = dict(title = 'Region', title_standoff = 25, automargin = True),
                            yaxis = dict(title = 'New Cases in Last 7 Days'),
                        )

    graph_four = []
    graph_four.append(
        go.Bar(
            x = data.prname.tolist(),
            y = data.ratetotal_last7.tolist(),
        )
    )

    layout_four = dict(title = 'New Case Rate (per 100,000 population) <br> in Last 7 Days By Region',
                            xaxis = dict(title = 'Region', title_standoff = 25, automargin = True),
                            yaxis = dict(title = 'New Case Rate in Last 7 Days'),
                            )

    figures = []
    figures.append(dict(data = graph_three, layout = layout_three))
    figures.append(dict(data = graph_four, layout = layout_four))

    return figures

#Active Cases Figures

def access_api(prov_list, url, column):
    column_names = ['date', column, 'prname']
    total_data = pd.DataFrame(columns = column_names) 
    
    for prov in prov_list:
        new_url = url + prov
        r = requests.get(new_url, allow_redirects=True)

        data = r.json()

        hosp = data['data']
        
        df = pd.DataFrame(hosp)

        df['prname'] = prov

        df = df[['date', column, 'prname']]
        
        total_data = total_data.append(df)

    return total_data
        
def access_canada_api(url, column):
    column_names = ['date', column]
    total_data = pd.DataFrame(columns = column_names) 
    r = requests.get(url, allow_redirects=True)

    data = r.json()

    hosp = data['data']
        
    df = pd.DataFrame(hosp)

    df['prname'] = 'Canada'

    df = df[['date', column, 'prname']]
        
    total_data = total_data.append(df)

    return total_data



prov_abbs = ['AB', 'BC', 'MB', 'NB', 'NL', 'NS', 'QC', 'ON', 'SK', 'PE', 'NT', 'NU', 'YT']

url="https://api.covid19tracker.ca/reports/province/"

pr_data = access_api(prov_abbs, url, 'total_hospitalizations')

can_url = 'https://api.covid19tracker.ca/reports'

can_data = access_canada_api(can_url, 'total_hospitalizations')

prov_dict = {
    'AB':'Alberta', 'BC':'British Columbia', 'MB':'Manitoba', 'NB':'New Brunswick', 'NL':'Newfoundland', 'NS':'Nova Scotia', 'QC':'Quebec', 
    'ON':'Ontario', 'SK':'Saskatchewan', 'PE':'Prince Edward Island', 'NT':'Northwest Territories', 'NU':'Nunavut', 'YT':'Yukon'
}

pr_data = pr_data.append(can_data)
pr_data['date'] = pd.to_datetime(pr_data['date'])

pr_data['YMD'] = pr_data['date'].dt.date
pr_data['prname'] = pr_data['prname'].replace(prov_dict)
provnames = sorted(pr_data.prname.unique())
myorder = [2, 0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
provnames = [provnames[i] for i in myorder]


#hospitalizations figure
def return_hosp_fig():
    graph = []
    for region in provnames:
        x_val = pr_data[pr_data['prname'] == region].YMD.tolist()
        y_val = pr_data[pr_data['prname'] == region].total_hospitalizations.tolist()
        graph.append(
            go.Scatter(
                x = x_val,
                y = y_val,
                mode = 'lines',
                name = region
            )
        )

    layout = dict(title="Total Hospitalizations Historically By Region",
                  xaxis=dict(title='Date'),
                  yaxis=dict(title='Number of Individuals Hospitalized'),
                  updatemenus=[dict(buttons=list([
                      dict(label="Linear",
                           method="relayout",
                           args=[{"yaxis.type": "linear"}]),

                      dict(label="Log",
                           method="relayout",
                           args=[{"yaxis.type": "log"}]),
                  ]),
                  )])
    figures = (dict(data = graph, layout = layout))

    return figures

def active_figs():
    return return_hosp_fig()


#deaths figures
def return_deaths_fig():
    data_bar = make_barchart_dataset(make_dataset(unique_provnames(), format_dates(df)))
    data_bar = data_bar[['prname', 'YMD', 'numdeathstoday', 'numdeaths_last7', 'ratedeaths_last7', 'avgdeaths_last7']]

    graph_two = []
    data = make_dataset(unique_provnames(), format_dates(df))
    data = data[['prname', 'YMD', 'numdeaths']]
    for region in unique_provnames():
        x_val = data[data['prname'] == region].YMD.tolist()
        y_val = data[data['prname'] == region].numdeaths.tolist()
        graph_two.append(
            go.Scatter(
                x = x_val,
                y = y_val,
                mode = 'lines',
                name = region
            )
        )

    layout_two = dict(title = "Cumulative Deaths by Region",
                    xaxis = dict(title = 'Date'),
                    yaxis = dict(title = 'Total Number of Deaths'),
                )

    graph_three = []
    graph_three.append(
        go.Bar(
            x = data_bar.prname.tolist(),
            y = data_bar.numdeaths_last7.tolist(),
        )
    )

    layout_three = dict(title = 'Number of Deaths in Last 7 Days By Region',
                        xaxis = dict(title = 'Region', title_standoff = 25, automargin = True),
                        yaxis = dict(title = 'Number of Deaths in Last 7 Days'),
                    )

    graph_four = []
    graph_four.append(
        go.Bar(
            x = data_bar.prname.tolist(),
            y = data_bar.ratedeaths_last7.tolist(),
        )
    )

    layout_four = dict(title = 'Mortality Rate (per 100,000 population) <br> in Last 7 Days By Region',
                        xaxis = dict(title = 'Region', title_standoff = 25, automargin = True),
                        yaxis = dict(title = 'Mortality Rate in Last 7 Days'),
                    )


    figures = []
    figures.append(dict(data = graph_two, layout = layout_two))
    figures.append(dict(data = graph_three, layout = layout_three))
    figures.append(dict(data = graph_four, layout = layout_four))

    return figures

#Rate of Infection Figures
def return_rate_of_infection_fig():
    graph = []
    data = make_dataset(unique_provnames(), format_dates(df))
    data = data[['prname', 'YMD', 'ratecasestotal']]
    for region in unique_provnames():
        x_val = data[data['prname'] == region].YMD.tolist()
        y_val = data[data['prname'] == region].ratecasestotal.tolist()
        graph.append(
            go.Scatter(
                x = x_val,
                y = y_val,
                mode = 'lines',
                name = region
            )
        )

    layout = dict(title = "Rate of Infection (per 100,000 population) By Region",
                    xaxis = dict(title = 'Date'),
                    yaxis = dict(title = 'Rate of Infection (per 100,000 population)'),
                    updatemenus=[dict(buttons=list([
                      dict(label="Linear",
                           method="relayout",
                           args=[{"yaxis.type": "linear"}]),

                      dict(label="Log",
                           method="relayout",
                           args=[{"yaxis.type": "log"}]),
                  ]),
                  )])
    
    figures = []
    figures.append(dict(data = graph, layout = layout))

    return figures

