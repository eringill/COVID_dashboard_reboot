from canadacoviddashboard import app
import json
import plotly
from flask import render_template
import pandas as pd
from wrangling_scripts.wrangling import *
from wrangling_scripts.vaccine_wrangling import return_vaccine_fig
from wrangling_scripts.variant_wrangling import return_variant_graph

@app.route('/')
@app.route('/index')
def index():

    figures = return_vaccine_fig()


    # plot ids for the html id tag
    ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html',
                           ids=ids,
                           figuresJSON=figuresJSON)
   
@app.route('/total_cases')
def total_cases():

    figures = return_total_cases_fig()

    # plot ids for the html id tag
    ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('total_cases.html',
                           ids=ids,
                           figuresJSON=figuresJSON)

@app.route('/new_cases')
def new_cases():
    figures = return_new_cases_fig()

    # plot ids for the html id tag
    ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('new_cases.html',
                           ids=ids,
                           figuresJSON=figuresJSON)

@app.route('/active_cases')
def active_cases():
    figures = active_figs()

    # plot ids for the html id tag
    ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('active_cases.html',
                           ids=ids,
                           figuresJSON=figuresJSON)


@app.route('/deaths')
def deaths():
    figures = return_deaths_fig()

    # plot ids for the html id tag
    ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('deaths.html',
                           ids=ids,
                           figuresJSON=figuresJSON)

@app.route('/rate_of_infection')
def rate_of_infection():
    figures = return_rate_of_infection_fig()

    # plot ids for the html id tag
    ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('rate_of_infection.html',
                           ids=ids,
                           figuresJSON=figuresJSON)


@app.route('/variants')
def variants():
    figures = return_variant_graph()

    # plot ids for the html id tag
    ids = ['figure-{}'.format(i) for i, _ in enumerate(figures)]

    # Convert the plotly figures to JSON for javascript in html template
    figuresJSON = json.dumps(figures, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('variants.html',
                           ids=ids,
                           figuresJSON=figuresJSON)