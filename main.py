import numpy as np
from sklearn.preprocessing import PolynomialFeatures
import pickle
from flask import Flask, render_template, request

app = Flask(__name__)

# Load prebuilt model
with open("HUM_forecast.pkl", 'rb') as file:  
    HUM_forecast_model = pickle.load(file)
HUM_forecast_model

with open("TC_forecast.pkl", 'rb') as file:  
    TC_forecast_model = pickle.load(file)
TC_forecast_model

# Handle GET request

def validValue(initVal):
    if initVal=="" or initVal==None:
        return False, "No Value"  
    try:
        val = int(initVal)
        return True, val
    except Exception as e:
        return False, "Not an Integer"

def predictFunc(val,model, deg):
    try:
        poly = PolynomialFeatures(degree=deg)
        valForModel = poly.fit_transform(np.array([val]).reshape(-1, 1))
        prediction = model.predict(valForModel)[0][0]
        return True, prediction
    except Exception as e:
        return True , str(e)


@app.route('/')
def checkClimate():
    return render_template('index.html')


@app.route('/temperature')
def loadTemperature():
    return render_template('temperature.html')

@app.route('/humidity')
def loadHumidity():
    return render_template('humidity.html')

# Handle POST request
@app.route('/temperature', methods=['POST'])
def checkTemperature():
    isValid, tempText = validValue(request.form['tempText'])
    if isValid:
        successMsg, prediction = predictFunc(tempText,TC_forecast_model, 4)
        return render_template('temperature.html', response=str(prediction),success=successMsg)
    else:
        return render_template('temperature.html', response=tempText)


@app.route('/humidity', methods=['POST'])
def checkHumidity():
    isValid, humText = validValue(request.form['humText'])
    if isValid:
        successMsg, prediction = predictFunc(humText,HUM_forecast_model, 3)
        return render_template('humidity.html', response=str(prediction),success=successMsg)
    else:
        return render_template('humidity.html', response=humText)

if __name__ == '__main__':
    app.run(debug=True)