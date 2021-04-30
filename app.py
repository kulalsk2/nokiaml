from flask import Flask,render_template,request
import pickle
from flask.helpers import flash
import requests
import time
from datetime import date
model = pickle.load(open('regressor1.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def man():
    return render_template('index.html') #this by itself selects template folder

def latandlong(cityname):
    urlRapid = "https://community-open-weather-map.p.rapidapi.com/find"
    querystringRapid = {"q":cityname,"mode":"null","lon":"0","type":"link, accurate","lat":"0","units":"imperial, metric"}
    headersRapid = {
    'x-rapidapi-key': "38dbf9e34dmshbfaff0223d0ac4fp180cc3jsnb22b375a7fad",
    'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
    }
    res = requests.request("GET", urlRapid, headers=headersRapid, params=querystringRapid)
    resFromRapid = res.json()
    lat = float(resFromRapid['list'][0]['coord']['lat'])
    long = float(resFromRapid['list'][0]['coord']['lon'])
    return lat,long

def getWeatherData(lat,long):
    urlWeatherBit = "https://api.weatherbit.io/v2.0/current?lat="+str(lat)+"&lon="+str(long)+"&key=f6bba80d9ad242b4b82bfb54364059ea"
    res = requests.request("GET", urlWeatherBit)
    resFromWebit = res.json()
    visibility = float(resFromWebit['data'][0]['vis'])
    cloudcoverage = float(resFromWebit['data'][0]['clouds'])
    temperature = float(resFromWebit['data'][0]['temp'])
    dewpoint = float(resFromWebit['data'][0]['dewpt'])
    relativehumidity = float(resFromWebit['data'][0]['rh'])
    windspeed = float(resFromWebit['data'][0]['wind_spd'])
    stationpressure = float(resFromWebit['data'][0]['pres'])
    urlAltitude = "https://api.opentopodata.org/v1/aster30m?locations="+str(lat)+","+str(long)+""  
    resAltimeter = requests.request("GET", urlAltitude).json()
    altimeter=float(resAltimeter['results'][0]['elevation'])
    # todayData = date.today().strftime("%d-%m-%Y")
    # day,month,year = tuple(str(todayData).split('-'))
    # year = int(year)
    # month = int(month)
    # day = int(day)
    X  = [cloudcoverage,visibility,temperature,dewpoint,relativehumidity,windspeed,stationpressure,altimeter]
    return X

def getCorrectUnit(X):
    X[0] = X[0]/100
    X[1] = 0.621371 *X[1] #0.621371 
    X[5] = 2.23694 *X[5]   #2.23694 
    pmb = X[6]
    hm = X[7]
    X[6] = 0.02953 *X[6] #0.02953
    pmbmin0_3 = pmb-0.3
    pmbmin0_3toPower0_190284 = pmbmin0_3**0.190284
    hmBYpmbmin0_3toPower0_190284 = hm/pmbmin0_3toPower0_190284
    rightEq = (1+0.0000842288*hmBYpmbmin0_3toPower0_190284)**5.25530260032
    X[7] = pmbmin0_3*rightEq
    X[7]= 0.02953*X[7]
    return X

@app.route('/predict',methods=['POST'])
def home():
    #cityname = request.form['cityname']
    #lat,long = latandlong(cityname)
    lat = float(request.form['lat'])
    long = float(request.form['long'])
    X = getWeatherData(lat,long)
    X = getCorrectUnit(X)
    print(X)
    timestamp = time.strftime('%H:%M:%S')
    hour =  int(timestamp[:2])
    X.insert(0,hour)
    print(X)
    X = list([X])
    pred = model.predict(X)
    print(pred)
    return render_template('after.html',data=pred)


    

if(__name__=="__main__"):
    app.run(debug=True)