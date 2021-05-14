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
    data = data[['prname', 'YMD', 'numtoday', 'percentoday', 'numtotal_last7', 'ratetotal_last7']]

    graph_one = []
    graph_one.append(
        go.Bar(
            x = data.prname.tolist(),
            y = data.numtoday.tolist(),
        )
    )

    layout_one = dict(title = 'New Cases Today By Region',
                        xaxis = dict(title = 'Region', title_standoff = 25, automargin = True),
                        yaxis = dict(title = 'New Cases Today'),
                    )

    graph_two = []
    graph_two.append(
        go.Bar(
            x = data.prname.tolist(),
            y = data.percentoday.tolist(),
        )
    )
    
    layout_two = dict(title = 'Percent New Cases Today By Region',
                        xaxis = dict(title = 'Region', title_standoff = 25, automargin = True),
                        yaxis = dict(title = 'Percent New Cases Today'),
                    )

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
    figures.append(dict(data = graph_one, layout = layout_one))
    figures.append(dict(data = graph_two, layout = layout_two))
    figures.append(dict(data = graph_three, layout = layout_three))
    figures.append(dict(data = graph_four, layout = layout_four))

    return figures

#Active Cases Figures
def return_active_cases_fig():
    data_pie = make_barchart_dataset(make_dataset(unique_provnames(), format_dates(df)))
    data_pie = data_pie[['prname', 'YMD', 'numactive']]
    data_pie = data_pie[data_pie['prname'] != 'Canada']

    graph_one = []
    graph_one.append(
        go.Pie(
            labels = data_pie.prname.tolist(),
            values = data_pie.numactive.tolist(),
        )
    )

    layout_one = dict(title = 'Active Cases Today By Region <br> as a Percentage of All Active Cases in Canada', textposition = 'inside', uniformtext_minsize=12,
                      uniformtext_mode='hide'
                    )

    graph_two = []
    data = make_dataset(unique_provnames(), format_dates(df))
    data = data[['prname', 'YMD', 'numactive']]
    for region in unique_provnames():
        x_val = data[data['prname'] == region].YMD.tolist()
        y_val = data[data['prname'] == region].numactive.tolist()
        graph_two.append(
            go.Scatter(
                x = x_val,
                y = y_val,
                mode = 'lines',
                name = region
            )
        )

    layout_two = dict(title = 'Cases Active Historically By Region',
                        xaxis = dict(title = 'Date'),
                        yaxis = dict(title = 'Active Cases'),
                    )

    data = make_barchart_dataset(make_dataset(unique_provnames(), format_dates(df)))
    data = data[['prname', 'YMD', 'rateactive']]

    graph_three = []
    graph_three.append(
        go.Bar(
            x=data.prname.tolist(),
            y=data.rateactive.tolist(),
        )
    )

    layout_three = dict(title='Active Case Rate (Per 100,000 Population) <br> Today By Region',
                      xaxis=dict(title='Region', title_standoff=25, automargin=True),
                      yaxis=dict(title='Active Case Rate'),
                      )

    figures = []
    figures.append(dict(data = graph_one, layout = layout_one))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data = graph_two, layout = layout_two))
    
    return figures

#Recoveries Figures
def return_recoveries_fig():
    data_bar = make_barchart_dataset(make_dataset(unique_provnames(), format_dates(df)))
    data_bar = data_bar[['prname', 'YMD', 'numrecoveredtoday']]

    graph_one = []
    graph_one.append(
        go.Bar(
            x = data_bar.prname.tolist(),
            y = data_bar.numrecoveredtoday.tolist(),
        )
    )

    layout_one = dict(title = 'Number of Recoveries Today By Region',
                        xaxis = dict(title = 'Region', title_standoff = 25, automargin = True),
                        yaxis = dict(title = 'Number of Recoveries Today'),
                    )
    
    graph_two = []
    data = make_dataset(unique_provnames(), format_dates(df))
    data = data[['prname', 'YMD', 'numrecover']]
    for region in unique_provnames():
        x_val = data[data['prname'] == region].YMD.tolist()
        y_val = data[data['prname'] == region].numrecover.tolist()
        graph_two.append(
            go.Scatter(
                x = x_val,
                y = y_val,
                mode = 'lines',
                name = region
            )
        )

    layout_two = dict(title = "Cumulative Recoveries by Region",
                    xaxis = dict(title = 'Date'),
                    yaxis = dict(title = 'Total Number of Recoveries'),
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
    figures.append(dict(data = graph_one, layout = layout_one))
    figures.append(dict(data = graph_two, layout = layout_two))
    
    return figures

#deaths figures
def return_deaths_fig():
    data_bar = make_barchart_dataset(make_dataset(unique_provnames(), format_dates(df)))
    data_bar = data_bar[['prname', 'YMD', 'numdeathstoday', 'numdeaths_last7', 'ratedeaths_last7', 'avgdeaths_last7']]

    graph_one = []
    graph_one.append(
        go.Bar(
            x = data_bar.prname.tolist(),
            y = data_bar.numdeathstoday.tolist()
        )
    )

    layout_one = dict(title = 'Number of Deaths Today By Region',
                        xaxis = dict(title = 'Region', title_standoff = 25, automargin = True),
                        yaxis = dict(title = 'Number of Deaths Today')
                    )
    
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
    figures.append(dict(data = graph_one, layout = layout_one))
    figures.append(dict(data = graph_two, layout = layout_two))
    figures.append(dict(data = graph_three, layout = layout_three))
    figures.append(dict(data = graph_four, layout = layout_four))

    return figures

#Rate of Infection Figures
def return_rate_of_infection_fig():
    graph = []
    data = make_dataset(unique_provnames(), format_dates(df))
    data = data[['prname', 'YMD', 'ratetotal']]
    for region in unique_provnames():
        x_val = data[data['prname'] == region].YMD.tolist()
        y_val = data[data['prname'] == region].ratetotal.tolist()
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

#Testing Rate Figures
def return_testing_rate_fig():
    graph = []
    data = make_dataset(unique_provnames(), format_dates(df))
    data = data[['prname', 'YMD', 'ratetests']]
    for region in unique_provnames():
        x_val = data[data['prname'] == region].YMD.tolist()
        y_val = data[data['prname'] == region].ratetests.tolist()
        graph.append(
            go.Scatter(
                x = x_val,
                y = y_val,
                mode = 'lines',
                name = region
            )
        )

    layout = dict(title = "Testing Rate (per 1 million population) By Region",
                    xaxis = dict(title = 'Date'),
                    yaxis = dict(title = 'Testing Rate (per 1 million population)'),
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

