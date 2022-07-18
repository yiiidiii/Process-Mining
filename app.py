import matplotlib.pyplot as plt
import pandas as pd
import os
import matplotlib.pyplot as pyplot
import matplotlib.cbook as cbook
import numpy as np
import matplotlib.dates as mdates
from flask import Flask, render_template, send_file, Blueprint
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
from wtforms.validators import InputRequired
from matplotlib.ticker import FuncFormatter
import textwrap

import __init__
import petri_net_vis.net_vis
import alpha_miner.statistics as stat

file_dir = os.path.dirname(
    os.path.abspath(__file__)
)

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/uploaded_files'

if os.environ.get("FLASK_ENV") == "production": # on live server
    bp = Blueprint('myapp', __name__, template_folder='templates', static_folder="static", url_prefix='/ports/8006')
else:
    bp = Blueprint('myapp', __name__, template_folder='templates', static_folder="static", url_prefix='')


class UploadFileForm(FlaskForm):
    file = FileField('File', validators=[InputRequired()])  # no error when no file is uploaded, but a reminder
    submit = SubmitField('Upload File')


@bp.route('/', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data  # first grab the file
        fpath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
        file.save(fpath)  # then save the file

        net, pl_legend, trans_legend = petri_net_vis.net_vis.graphviz_net(fpath)
        file.filename = file.filename.replace('.xes', '')

        # statistics
        num_traces = stat.num_of_traces(fpath)
        stat.num_events_total(fpath)
        mean_duration = str(stat.get_durations_of_traces(fpath))
        stat.num_events_total(fpath)
        stat.get_durations_of_traces(fpath)
        plot_occurrences()
        plot_durations()

        net.render("static/test_files/svg_files/petri_net", cleanup=True, format='svg')
        return render_template('user_image.html', user_image="static/test_files/svg_files/petri_net" + ".svg",
                               trans_legend=trans_legend, place_legend=pl_legend,
                               num_traces=num_traces, event_occ='static/statistics/event_occurrences.svg', trace_dur='static/statistics/trace_durations.svg',
                               mean_duration=mean_duration)

    return render_template('index.html', form=form)


@bp.route('/download_svg/')
@app.route('/download_svg/')
def return_files_svg():
    try:
        return send_file("static/test_files/svg_files/petri_net.svg", download_name='net.svg')
    except Exception as e:
        return str(e)


@bp.route('/download_pdf/')
@app.route('/download_pdf/')
def return_files_pdf():
    try:
        return send_file("static/test_files/svg_files/petri_net.pdf", download_name='net.pdf')
    except Exception as e:
        return str(e)


@bp.route('/l1')
@app.route('/l1')
def l1():
    PATH_XES = 'static/test_files/xes_files/L1.xes'
    PATH_NET = 'static/test_files/svg_files/petri_net'

    return visualize_net(PATH_XES, PATH_NET)


@bp.route('/l2')
@app.route('/l2')
def l2():
    PATH_XES = 'static/test_files/xes_files/L2.xes'
    PATH_NET = 'static/test_files/svg_files/petri_net'

    return visualize_net(PATH_XES, PATH_NET)


@bp.route('/l3')
@app.route('/l3')
def l3():
    PATH_XES = 'static/test_files/xes_files/L3.xes'
    PATH_NET = 'static/test_files/svg_files/petri_net'

    return visualize_net(PATH_XES, PATH_NET)


@bp.route('/l4')
@app.route('/l4')
def l4():
    PATH_XES = 'static/test_files/xes_files/L4.xes'
    PATH_NET = 'static/test_files/svg_files/petri_net'

    return visualize_net(PATH_XES, PATH_NET)


@bp.route('/l5')
@app.route('/l5')
def l5():
    PATH_XES = 'static/test_files/xes_files/L5.xes'
    PATH_NET = 'static/test_files/svg_files/petri_net'

    return visualize_net(PATH_XES, PATH_NET)


@bp.route('/l6')
@app.route('/l6')
def l6():
    PATH_XES = 'static/test_files/xes_files/L6.xes'
    PATH_NET = 'static/test_files/svg_files/petri_net'

    return visualize_net(PATH_XES, PATH_NET)


@bp.route('/l7')
@app.route('/l7')
def l7():
    PATH_XES = 'static/test_files/xes_files/L7.xes'
    PATH_NET = 'static/test_files/svg_files/petri_net'

    return visualize_net(PATH_XES, PATH_NET)


@bp.route('/billinstances')
@app.route('/billinstances')
def billinstances():
    PATH_XES = 'static/test_files/xes_files/billinstances.xes'
    PATH_NET = 'static/test_files/svg_files/petri_net'

    return visualize_net(PATH_XES, PATH_NET)


@bp.route('/posterinstances')
@app.route('/posterinstances')
def posterinstances():
    PATH_XES = 'static/test_files/xes_files/posterinstances.xes'
    PATH_NET = 'static/test_files/svg_files/petri_net'

    return visualize_net(PATH_XES, PATH_NET)


@bp.route('/flyerinstances')
@app.route('/flyerinstances')
def flyerinstances():
    PATH_XES = 'static/test_files/xes_files/flyerinstances.xes'
    PATH_NET = 'static/test_files/svg_files/petri_net'

    return visualize_net(PATH_XES, PATH_NET)


@bp.route('/running-example')
@app.route('/running-example')
def running_example():
    PATH_XES = 'static/test_files/xes_files/running-example.xes'
    PATH_NET = 'static/test_files/svg_files/petri_net'

    return visualize_net(PATH_XES, PATH_NET)


def visualize_net(path_xes_file, path_net_file):
    net, place_legend, trans_legend = petri_net_vis.net_vis.graphviz_net(f'{path_xes_file}')
    num_traces = stat.num_of_traces(path_xes_file)
    stat.num_events_total(path_xes_file)
    mean_duration = stat.get_durations_of_traces(path_xes_file)

    stat.num_events_total(path_xes_file)
    stat.get_durations_of_traces(path_xes_file)
    plot_occurrences()
    plot_durations()

    net.render(f'{path_net_file}', cleanup=True, format='svg')
    return render_template('images_test_files.html', svg_file=f'{path_net_file}' + '.svg',
                           place_legend=place_legend, trans_legend=trans_legend,
                           num_traces=num_traces, event_occ='static/statistics/event_occurrences.svg', trace_dur='static/statistics/trace_durations.svg',
                           mean_duration=mean_duration)


def plot_occurrences():
    """
    generates a bar chart for the occurrence of each event and writes it into svg file.
    :return:
    """
    data = pd.read_csv('static/statistics/event_number.csv')

    df = pd.DataFrame(data)

    # Here we sort the second column, i.e. the duration by its value
    df = df.sort_values('occurrence', ascending=True)

    # subplots gives us n (default 1) plot and its axis
    # the figure size is configured as the number of elements in the x-axis
    # The height is set statically to 6 (inches)
    fig, ax = plt.subplots(figsize=(len(df['event_name']), 6))

    # sets the name of the graph
    ax.set_title("Total Occurrences of Events", fontsize=20, pad=15)
    ax.set_ylabel("Occurrences", fontsize=14, labelpad=7)
    ax.set_xlabel("Event Names", fontsize=14, labelpad=7)

    ax.bar(df['event_name'], df['occurrence'], color='#855D6AB0')
    # X axis looks tidier
    fig.autofmt_xdate()
    fig.tight_layout()

    # Offset for the text
    y_offset = ax.get_ylim()[1] * 0.0075
    for i, v in enumerate(df.values):
        ax.text(v[0], v[1] + y_offset, str(v[1]), color="black", ha="center")

    plt.savefig('static/statistics/event_occurrences.svg', format='svg', bbox_inches='tight')


def format_func(x, y):
    """
    formats the given x nanoseconds to HH:MM:SS (hours:minutes:seconds)
    :param x: nanoseconds
    :return: the string representation of HH:MM:SS
    """
    total_seconds = int(x / 1000000000)

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    return "{:d}:{:02d}:{:02d}".format(hours, minutes, seconds)


def plot_durations():
    """
    generates a bar chart for the durations of each trace and saves into svg file
    :return:
    """
    data = pd.read_csv('static/statistics/trace_durations.csv')

    df2 = pd.DataFrame(data)

    # Reading the data as time delta because time delta is what we need
    df2["trace_name"] = df2["trace_name"].astype(str)
    df2["duration"] = pd.to_timedelta(df2["duration"])

    # Here we sort the second column, i.e. the duration by its value
    df2 = df2.sort_values('duration', ascending=True)

    # If length of x-axis too high, then only the first 7 and last 7 entries are taken
    # the first 7 are the smallest values regarding duration, and the last are the highest
    if len(df2["duration"]) >= 15:
        df2 = df2.iloc[list(range(7)) + list(range(len(df2) - 7, len(df2)))]

    # If you want to print the duration please uncomment the next line UwU
    # print(df2['duration'])
    # formatter gives us the nanoseconds as HH:MM:SS
    formatter = FuncFormatter(format_func)

    # subplots gives us n (default 1) plot and its axis
    # We configure the figure size as the number of elements in the x-axis
    # The height is set statically to 6 (inches)
    fig, ax = plt.subplots(figsize=(len(df2['trace_name']), 6))

    # Sets our glorious formatter to the y axis, so it looks as beautiful as the sun
    ax.yaxis.set_major_formatter(formatter)

    # sets the name of the graph
    ax.set_title("Trace Durations", fontsize=20, pad=15)
    ax.set_ylabel("Duration in HH:MM:SS", fontsize=14, labelpad=7)
    ax.set_xlabel("Trace Names", fontsize=14, labelpad=7)

    ax.bar(df2['trace_name'], df2['duration'], color='#855D6AB0')
    # X axis looks tidier
    fig.autofmt_xdate()
    fig.tight_layout()

    # Sets the starting value of the y-axis to 0 or the least value minus 1h (configurable)
    ax.set_ylim(bottom=max(pd.Timedelta("0").delta, int(df2['duration'].iloc[[0]].values[0]) - pd.Timedelta("1h").delta))

    # Offset for the text.
    y_offset = ax.get_ylim()[1] * 0.0075
    for i, v in enumerate(df2.values):
        ax.text(v[0], v[1].delta + y_offset, format_func(v[1].delta, 0), color="black", ha="center")

    plt.savefig('static/statistics/trace_durations.svg', format='svg', bbox_inches='tight')


app.register_blueprint(bp)


if __name__ == "__main__":
    app.run(debug=True)
