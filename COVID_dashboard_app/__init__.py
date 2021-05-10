from flask import Flask

app = Flask(__name__, template_folder = "templates")

from COVID_dashboard_app import routes