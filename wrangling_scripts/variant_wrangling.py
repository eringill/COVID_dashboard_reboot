import pandas as pd
pd.options.mode.chained_assignment = None
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import datetime as dt

def wrangle_data(url):
    df = pd.read_csv(csv_url)
    df.columns = ['grouping', 'identifier', 'lineage', 'percentage', 'week']
    df['week'] = pd.to_datetime(df['week'])
    unique_weeks = df.week.unique()
    unique_identifiers = df.identifier.unique()
    unique_weeks_columns = ['grouping', 'identifier', 'percentage', 'week']
    df_unique_weeks = pd.DataFrame(columns = unique_weeks_columns)

    for identifier in unique_identifiers:
        df_sub1 = df[df['identifier'] == identifier]
    #print(df_sub1.head())
        for week in unique_weeks:
            df_sub2 = df_sub1[df_sub1['week'] == week]
            #print(df_sub2.head())
            pct = df_sub2.percentage.sum()
            df_unique_weeks.loc[len(df_unique_weeks)] = [df_sub1.iloc[0]['grouping'], identifier, pct, week]
    df_unique_weeks['YMD'] = df_unique_weeks['week'].dt.date

    variants = df_unique_weeks.identifier.unique()
    df_unique_weeks = df_unique_weeks[df_unique_weeks['YMD'] > pd.to_datetime('2020-03-01')]
    
    return df_unique_weeks, variants

def return_variant_graph():
    graph = []
    for i, var in enumerate(var_list):
        x_val = week_df[week_df['identifier'] == var].YMD.tolist()
        y_val = week_df[week_df['identifier'] == var].percentage.tolist()
        graph.append(
            go.Bar(
                x = x_val,
                y = y_val,
                name = var,
                marker_color = px.colors.qualitative.Dark24[i]
            )
        )

    layout = dict(barmode='relative', title="Variant Proportion of Samples Sequenced in Canada by Date",
                  xaxis=dict(title='Date'),
                  yaxis=dict(title='Variant Proportion')
                  )

    figures = []
    figures.append(dict(data = graph, layout = layout))

    return figures

csv_url = 'https://health-infobase.canada.ca/src/data/covidLive/covid19-epiSummary-variants.csv'

week_df, var_list = wrangle_data(csv_url)
