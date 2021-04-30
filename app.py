import mainpage
import perday
from flask import Flask,render_template,request
import pickle
import time
model = pickle.load(open('regressor1.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def man():
    return render_template('index.html') #this by itself selects template folder

def getPerDayChart(lat,long,yesterday,today):
    resFromWebit = perday.getWeatherDataForPerDay(lat,long,yesterday,today)
    altimeter = perday.locElevationForPerDay(lat, long)
    solarOutputPerhours = list()
    time = list()
    for i in range(0,24):
        X = perday.refinedDataForPerDay(resFromWebit, i)
        X.append(altimeter)
        print(X)
        X = perday.getCorrectUnitPerDay(X)
        if (X[0]>=0 and X[0]<=5) or (X[0]>=18 and X[0]<=24):
                solarOutputPerhours.append(0)
                time.append(X[0])
                continue
            
        time.append(X[0])
        X = list([X])
        pred = model.predict(X)
        solarOutputPerhours.append(pred[0])
        X = []
    print(solarOutputPerhours)
    solarOutputPerDay = sum(solarOutputPerhours)
    return solarOutputPerhours,time,solarOutputPerDay


@app.route('/perday',methods=['POST'])
def home():
    lat = float(request.form['lat'])
    long = float(request.form['long'])
    yesterday = request.form['yesterday']
    today = request.form['today']
    
    solarOutputPerhours,times,solarOutputPerDay = getPerDayChart(lat,long,yesterday,today)
    X = mainpage.getWeatherData(lat,long)
    X = mainpage.getCorrectUnit(X)
    timestamp = time.strftime('%H:%M:%S')
    hour =  int(timestamp[:2])
    if (hour>=0 and hour<=5) or (hour>=18 and hour<=24):
        return render_template('perday.html',currTimeprediction=0,solarOutputPerhours=solarOutputPerhours,time=times,solarOutputPerDay=solarOutputPerDay)
    X.insert(0,hour)
    X = list([X])
    pred = model.predict(X)
    return  render_template('perday.html',currTimeprediction = pred[0],solarOutputPerhours=solarOutputPerhours,time=times,solarOutputPerDay=solarOutputPerDay)


    

if(__name__=="__main__"):
    app.run(debug=True)