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
        print(os.path.join("static/upload_nets", secure_filename(file.filename) + ".png"))
        return render_template('user_image.html', user_image=os.path.join("static/upload_nets", secure_filename(file.filename) + ".png"))
    return render_template('index.html', form=form)


# def index():
#     return render_template('templates/index.html')


@app.route('/l1')
def l1():
    net = petri_net_vis.main.graphviz_net('static/test_files/L1.xes')
    net.view()
    return 'Your file is shown in the pdf viewer'


if __name__ == "__main__":
    app.run(debug=True)
