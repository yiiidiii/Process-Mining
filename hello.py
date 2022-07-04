from flask import Flask, render_template, send_file
import alpha_miner
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
import petri_net_vis.main
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/upload_files'


class UploadFileForm(FlaskForm):
    file = FileField('File', validators=[InputRequired()])  # no error when no file is uploaded, but a reminder
    submit = SubmitField('Upload File')


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data  # first grab the file
        fpath = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'],
                             secure_filename(file.filename))
        file.save(fpath)  # then save the file

        net = petri_net_vis.main.graphviz_net(fpath)
        net.render(os.path.join("static/upload_nets", secure_filename(file.filename)), cleanup=True, format='png')
        return render_template('user_image.html', user_image=os.path.join("static/upload_nets", secure_filename(file.filename)) + '.png')
    return render_template('index.html', form=form)


@app.route('/l1')
def l1():
    PATH_XES = 'static/test_files/xes_files/L1.xes'
    PATH_NET = 'static/test_files/png_files/L1.pdf'

    return visualize_net(PATH_XES, PATH_NET)


@app.route('/l2')
def l2():
    PATH_XES = 'static/test_files/xes_files/L2.xes'
    PATH_NET = 'static/test_files/png_files/L2.pdf'

    return visualize_net(PATH_XES, PATH_NET)


@app.route('/l3')
def l3():
    PATH_XES = 'static/test_files/xes_files/L3.xes'
    PATH_NET = 'static/test_files/png_files/L3.pdf'

    return visualize_net(PATH_XES, PATH_NET)


@app.route('/l4')
def l4():
    PATH_XES = 'static/test_files/xes_files/L4.xes'
    PATH_NET = 'static/test_files/png_files/L4.pdf'

    return visualize_net(PATH_XES, PATH_NET)


@app.route('/l5')
def l5():
    PATH_XES = 'static/test_files/xes_files/L5.xes'
    PATH_NET = 'static/test_files/png_files/L5.pdf'

    return visualize_net(PATH_XES, PATH_NET)


@app.route('/l6')
def l6():
    PATH_XES = 'static/test_files/xes_files/L6.xes'
    PATH_NET = 'static/test_files/png_files/L6.pdf'

    return visualize_net(PATH_XES, PATH_NET)


@app.route('/l7')
def l7():
    PATH_XES = 'static/test_files/xes_files/L7.xes'
    PATH_NET = 'static/test_files/png_files/L7.pdf'

    return visualize_net(PATH_XES, PATH_NET)


@app.route('/billinstances')
def billinstances():
    PATH_XES = 'static/test_files/xes_files/billinstances.xes'
    PATH_NET = 'static/test_files/png_files/billinstances.pdf'

    return visualize_net(PATH_XES, PATH_NET)


@app.route('/posterinstances')
def posterinstances():
    PATH_XES = 'static/test_files/xes_files/posterinstances.xes'
    PATH_NET = 'static/test_files/png_files/posterinstances.pdf'

    return visualize_net(PATH_XES, PATH_NET)


@app.route('/flyerinstances')
def flyerinstances():
    PATH_XES = 'static/test_files/xes_files/flyerinstances.xes'
    PATH_NET = 'static/test_file/png_files/flyerinstances.pdf'

    return visualize_net(PATH_XES, PATH_NET)

# TODO: add statistics 100%
# TODO: css file 0%
# TODO: Unittests 40%
# TODO: correct alpha miner 100%


def visualize_net(path_xes_file, path_net_file):
    net = petri_net_vis.main.graphviz_net(f'{path_xes_file}')
    net.render(f'{path_net_file}', cleanup=True, format='png')
    return render_template('images_test_files.html', user_image=f'{path_net_file}' + '.png')


if __name__ == "__main__":
    app.run(debug=True)
    # l1()
