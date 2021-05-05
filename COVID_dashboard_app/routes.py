from COVID_dashboard_reboot import app

from flask import render_template
import pandas as pd
from wrangling_scripts.wrangling import *

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
    
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
def project_two():
    return render_template('new_cases.html', data_set = )

@app.route('/active_cases_by_region')
def project_two():
    return render_template('active_cases_by_region.html', data_set = )

@app.route('/recoveries')
def project_two():
    return render_template('recoveries.html', data_set = )

@app.route('/deaths')
def project_two():
    return render_template('deaths.html', data_set = )

@app.route('/rate_of_infection')
def project_two():
    return render_template('rate_of_infection.html', data_set = )

@app.route('/testing_rate')
def project_two():
    return render_template('testing_rate.html', data_set = )