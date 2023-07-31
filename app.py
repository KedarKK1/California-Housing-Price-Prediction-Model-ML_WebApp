import pickle
# import pickle5 as pickle
from flask import Flask, request, app, jsonify, url_for, render_template
import numpy as np
import pandas as pd

app = Flask(__name__)

regmodel = pickle.load(open('regmodel.pkl', 'rb'))
scalar = pickle.load(open('scaling.pkl', 'rb'))


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/predict_api', methods=['POST'])
def predict_api():
    data = request.json['data']
    print("data ", data)
    print(np.array(list(data.values())).reshape(1, -1))
    new_data = scalar.transform(np.array(list(data.values())).reshape(1, -1))
    output = regmodel.predict(new_data)
    print("output", output[0])  # since o/p is of 2-d array
    return jsonify(output[0])


@app.route('/predict', methods=['POST'])
def predict():
    data = [float(x) for x in request.form.values()]
    final_input = scalar.transform(np.array(data).reshape(1, -1))
    print("final_input ", final_input)
    output = regmodel.predict(final_input)[0]
    return render_template("home.html", prediction_text="The House Price Prediction is {} ".format(output))


if __name__ == "__main__":
    app.run(debug=True)

# dummy json to api http://127.0.0.1:5000/v-
# {
#     "data": {
#         "MedInc": 8.3252,
#         "HouseAge": 52.0,
#         "AveRooms":	6.238137,
#         "AveBedrms": 1.081081,
#         "Population": 496.0,
#         "AveOccup":	2.547945,
#         "Latitude":	37.88,
#         "Longitude": -122.22
#     }
# }
# response - 85.75548629729107
