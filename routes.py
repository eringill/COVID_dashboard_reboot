from COVID_dashboard_reboot import app

from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
    
@app.route('/total_cases')
def project_one():
    return render_template('total_cases.html')

@app.route('/new_cases')
def project_two():
    return render_template('new_cases.html')

@app.route('/active_cases_by_region')
def project_two():
    return render_template('active_cases_by_region.html')

@app.route('/recoveries')
def project_two():
    return render_template('recoveries.html')

@app.route('/deaths')
def project_two():
    return render_template('deaths.html')

@app.route('/rate_of_infection')
def project_two():
    return render_template('rate_of_infection.html')

@app.route('/testing_rate')
def project_two():
    return render_template('testing_rate.html')