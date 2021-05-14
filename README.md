COVID_dashboard_reboot
======================

Data Source
-----------
All data for this project are available from the [Government of Canada Infobase](https://health-infobase.canada.ca). Data are updated daily.

Motivation
----------
This is a reboot of my [canada_COVID-19_dashboard project](https://github.com/eringill/canada_COVID-19_dashboard) (which was written in a jupyter notebook and used bokeh for data visualization).
For this version, I wanted to create something that could be hosted on a server so that users can access it anywhere.
I've also made tweaks to how the data are processed and displayed.

The motivation for the original dashboard was to create something that users could interact with freely and explore - where the visualizations can do the talking.

Required Libraries
------------------
(Technically nothing - you can view the dashboard [here]())

If you want to fork the repo and run on your own machine, you'll need:
- python
- pandas
- plotly
- flask

Files
-----
- `README.md` - This file
- `LICENSE.md` - Legal information
- `wrangling_scripts/wrangling.py` - scripts to wrangle data on COVID-19 infections
- `wrangling_scripts/vaccine_wrangling.py` - scripts to wrangle data on COVID-19 vaccination
- `COVIDdashboard.py` - execute to start the app
- `COVID_dashboard_app/static` - all image files
- `COVID_dashboard_app/templates` - all html files
- `COVID_dashboard_app/__init__.py` - flask config and routes import
- `COVID_dashboard_app/routes.py` - all the information for flask to do its job and JavaScript to pass figures to front end


