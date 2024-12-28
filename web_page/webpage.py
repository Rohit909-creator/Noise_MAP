from flask import Flask, render_template, request, redirect, url_for
from MAP_SIM import Map
app = Flask(__name__)

mapp = Map()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/show_map', methods=['POST'])
def show_map():
    # Retrieve input data from the form
    mapp.start_location = request.form.get('start_location')
    mapp.end_location = request.form.get('end_location')
    mapp.get_routes()
    mapp.render_route()

    return redirect(url_for('noise_map'))

@app.route('/noise_map')
def noise_map():
    return render_template('noise_map.html')

if __name__ == '__main__':
    app.run(debug=True)
