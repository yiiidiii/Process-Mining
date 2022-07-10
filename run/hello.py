import matplotlib.pyplot as plt
import pandas as pd
import os
import matplotlib.pyplot as pyplot
import matplotlib.cbook as cbook
import numpy as np
import matplotlib.dates as mdates
from flask import Flask, render_template, send_file
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired

import __init__
import petri_net_vis.net_vis
import lib.alpha_miner.statistics as stat


app = Flask(__name__, template_folder="../templates/", static_folder="../static")
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/uploaded_files'


class UploadFileForm(FlaskForm):
    file = FileField('File', validators=[InputRequired()])  # no error when no file is uploaded, but a reminder
    submit = SubmitField('Upload File')


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():

    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data  # first grab the file
        fpath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
        file.save(fpath)  # then save the file

        net, pl_legend, trans_legend = petri_net_vis.net_vis.graphviz_net(fpath)
        file.filename = file.filename.replace('.xes', '')
        net.render(os.path.join("static/uploaded_nets", secure_filename(file.filename)), cleanup=True, format='svg')
        return render_template('user_image.html', user_image=os.path.join("static/uploaded_nets", secure_filename(file.filename)) + '.svg',
                               trans_legend=trans_legend, place_legend=pl_legend)

    return render_template('index.html', form=form)


@app.route('/l1')
def l1():
    PATH_XES = 'static/test_files/xes_files/L1.xes'
    PATH_NET = 'static/test_files/svg_files/L1'

    return visualize_net(PATH_XES, PATH_NET)


@app.route('/l2')
def l2():
    PATH_XES = 'static/test_files/xes_files/L2.xes'
    PATH_NET = 'static/test_files/svg_files/L2'

    return visualize_net(PATH_XES, PATH_NET)


@app.route('/l3')
def l3():
    PATH_XES = 'static/test_files/xes_files/L3.xes'
    PATH_NET = 'static/test_files/svg_files/L3'

    return visualize_net(PATH_XES, PATH_NET)


@app.route('/l4')
def l4():
    PATH_XES = 'static/test_files/xes_files/L4.xes'
    PATH_NET = 'static/test_files/svg_files/L4'

    return visualize_net(PATH_XES, PATH_NET)


@app.route('/l5')
def l5():
    PATH_XES = 'static/test_files/xes_files/L5.xes'
    PATH_NET = 'static/test_files/svg_files/L5'

    return visualize_net(PATH_XES, PATH_NET)


@app.route('/l6')
def l6():
    PATH_XES = 'static/test_files/xes_files/L6.xes'
    PATH_NET = 'static/test_files/svg_files/L6'

    return visualize_net(PATH_XES, PATH_NET)


@app.route('/l7')
def l7():
    PATH_XES = 'static/test_files/xes_files/L7.xes'
    PATH_NET = 'static/test_files/svg_files/L7'

    return visualize_net(PATH_XES, PATH_NET)


@app.route('/billinstances')
def billinstances():
    PATH_XES = 'static/test_files/xes_files/billinstances.xes'
    PATH_NET = 'static/test_files/svg_files/billinstances'

    return visualize_net(PATH_XES, PATH_NET)


@app.route('/posterinstances')
def posterinstances():
    PATH_XES = 'static/test_files/xes_files/posterinstances.xes'
    PATH_NET = 'static/test_files/svg_files/posterinstances'

    return visualize_net(PATH_XES, PATH_NET)


@app.route('/flyerinstances')
def flyerinstances():
    PATH_XES = 'static/test_files/xes_files/flyerinstances.xes'
    PATH_NET = 'static/test_files/svg_files/flyerinstances'

    return visualize_net(PATH_XES, PATH_NET)


@app.route('/running-example')
def running_example():
    PATH_XES = 'static/test_files/xes_files/running-example.xes'
    PATH_NET = 'static/test_files/svg_files/running-example'

    return visualize_net(PATH_XES, PATH_NET)


def visualize_net(path_xes_file, path_net_file):
    net, place_legend, trans_legend = petri_net_vis.net_vis.graphviz_net(f'{path_xes_file}')
    num_traces = stat.num_of_traces(path_xes_file)
    stat.num_events_total(path_xes_file)
    stat.get_durations_of_traces(path_xes_file)

    stat.num_events_total(path_xes_file)
    stat.get_durations_of_traces(path_xes_file)
    plot_occurrences()
    plot_durations()

    net.render(f'{path_net_file}', cleanup=True, format='svg')
    return render_template('images_test_files.html', user_image=f'{path_net_file}' + '.svg',
                           place_legend=place_legend, trans_legend=trans_legend,
                           num_traces=num_traces, event_occ='static/statistics/event_occurrences.svg', trace_dur='static/statistics/trace_durations.svg')


def plot_occurrences():
    data = pd.read_csv('static/statistics/event_number.csv')

    df = pd.DataFrame(data)
    X = list(df.iloc[:, 0])
    Y = list(df.iloc[:, 1])

    plt.clf()
    plt.bar(X, Y, color='#BE6C72EF')
    plt.title('Total Occurrences of each Event')
    plt.xlabel('event names')
    plt.ylabel('occurrence')

    plt.savefig('static/statistics/event_occurrences.svg', format='svg')


def plot_durations():
    data = pd.read_csv('static/statistics/trace_durations.csv')

    df2 = pd.DataFrame(data)
    X = list(df2.iloc[:, 0])  # trace names
    Y = list(df2.iloc[:, 1])  # durations
    # Y = mdates.datestr2num(Y)

    plt.clf()
    plt.bar(X, Y, color='#BE6C72EF')
    plt.title('Duration of each Trace')
    plt.xlabel('trace name')
    plt.ylabel('duration')

    plt.savefig('static/statistics/trace_durations.svg', format='svg')


if __name__ == "__main__":
    app.run(debug=True)
    # l1()


