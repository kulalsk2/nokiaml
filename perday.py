import requests

def getCorrectUnitPerDay(X):
    X[1] = X[1]/100
    X[2] = 0.621371 *X[2] #0.621371 
    X[6] = 2.23694 *X[6]   #2.23694 
    pmb = X[7]
    hm = X[8]
    X[7] = 0.02953 *X[7] #0.02953
    pmbmin0_3 = pmb-0.3
    pmbmin0_3toPower0_190284 = pmbmin0_3**0.190284
    hmBYpmbmin0_3toPower0_190284 = hm/pmbmin0_3toPower0_190284
    rightEq = (1+0.0000842288*hmBYpmbmin0_3toPower0_190284)**5.25530260032
    X[8] = pmbmin0_3*rightEq
    X[8]= 0.02953*X[8]
    return X
    
def getWeatherDataForPerDay(lat,long,yesterday,today):
    
    urlWeatherBit = "https://api.weatherbit.io/v2.0/history/hourly?lat="+str(lat)+"&lon="+str(long)+"&start_date="+str(today)+"&end_date="+str(yesterday)+"&tz=local&key=c19308a05e44450f805946e96f0743d0"
    res = requests.request("GET", urlWeatherBit)
    resFromWebit = res.json()
    return resFromWebit

def locElevationForPerDay(lat, long):
    urlAltitude = "https://api.opentopodata.org/v1/aster30m?locations="+str(lat)+","+str(long)+""  
    resAltimeter = requests.request("GET", urlAltitude).json()
    altimeter=float(resAltimeter['results'][0]['elevation'])
    return altimeter



def refinedDataForPerDay(resFromWebit, i):
    visibility = float(resFromWebit['data'][i]['vis'])
    cloudcoverage = float(resFromWebit['data'][i]['clouds'])
    temperature = float(resFromWebit['data'][i]['temp'])
    dewpoint = float(resFromWebit['data'][i]['dewpt'])
    relativehumidity = float(resFromWebit['data'][i]['rh'])
    windspeed = float(resFromWebit['data'][i]['wind_spd'])
    stationpressure = float(resFromWebit['data'][i]['pres'])
    hour = str(resFromWebit['data'][i]['timestamp_local'])
    hour = int(hour[11:13])
    # todayData = date.today().strftime("%d-%m-%Y")
    # day,month,year = tuple(str(todayData).split('-'))
    # year = int(year)
    # month = int(month)
    # day = int(day)
    
    X  = [hour,cloudcoverage,visibility,temperature,dewpoint,relativehumidity,windspeed,stationpressure]
    return X