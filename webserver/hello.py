from flask import Flask, render_template
import petri_net_vis.main

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/l1')
def l1():
    net = petri_net_vis.main.create_net()
    net.draw('my_net.png', place_attr=petri_net_vis.main.draw_place, trans_attr=petri_net_vis.main.draw_transition)


if __name__ == "__main__":
    app.run(debug = True)