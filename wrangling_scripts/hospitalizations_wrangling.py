import requests
import pandas as pd
import json
import chart_studio.plotly as py
import plotly.graph_objects as go
import plotly.io as pio
pio.renderers.default='notebook'
import datetime as dt





def access_api(prov_list, url, column):
    column_names = ['date', column, 'prname']
    total_data = pd.DataFrame(columns = column_names) 
    
    for prov in prov_list:
        new_url = url + prov
        r = requests.get(new_url, allow_redirects=True)

        open('data_summary.json', 'wb').write(r.content)

        with open('data_summary.json') as json_file:
            data = json.load(json_file)

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

    open('data_summary.json', 'wb').write(r.content)

    with open('data_summary.json') as json_file:
        data = json.load(json_file)

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
provnames = sorted(pr_data.prname.unique())
myorder = [2, 0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
provnames = [provnames[i] for i in myorder]

pr_data['YMD'] = pr_data['date'].dt.date
pr_data['prname'] = pr_data['prname'].replace(prov_dict)


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
    figures = []
    figures.append(dict(data = graph, layout = layout))

    return figures

