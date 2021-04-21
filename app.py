from flask import Flask, render_template, jsonify,request
import pickle
import numpy as np
import pandas as pd
import xgboost as xgb
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

clf = xgb.XGBClassifier()
clf.load_model(fname='final.model')

# filename = 'kmeans20practice_model.sav'
# loaded_model = pickle.load(open(filename,'rb'))

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

weekdays = {
    "Monday"   : 0,
    "Tuesday"  : 1,
    "Wednesday": 2,
    "Thursday" : 3,
    "Friday"   : 4,
    "Saturday" : 5,
    "Sunday"   : 6
}

sunrise_sunset = {
    "Day" : 0,
    "Night"  : 1
}

weather_cond = {
    "Sunny"       : [0,0,0,0,0],
    "Cloudy"      : [1,0,0,0,0],
    "Fog"         : [0,1,0,0,0],
    "Rain"        : [0,0,1,0,0],
    "Snow or Ice" : [0,0,0,1,0],
    "Thunderstorm": [0,0,0,0,1]
}

df = pd.read_csv('US_Accidents_Dec20_Coordinates_NY.csv')

# selectedWeather, selectedDay, selectedHour, selectedSun,
# selectedTemperature, selectedHumidity, selectedWind, selectedPrecipitation;
class DataStore():
    state         = None
    day_of_week   = None
    hour          = None
    sun           = None
    weather       = None
    temperature   = None
    wind          = None
    precipitation = None
    humidity      = None
    all_lng       = None
    all_lat       = None

data=DataStore()

@app.route("/main",methods=["GET","POST"])


@app.route('/',methods=["GET","POST"])
def index():
    state         = request.form.get("State")
    day_of_week   = request.form.get("Day")
    hour          = request.form.get("Hour")
    sun           = request.form.get("Sun")
    weather       = request.form.get("Weather")
    temperature   = request.form.get("Temperature")
    wind          = request.form.get("Wind")
    precipitation = request.form.get("Precipitation")
    humidity      = request.form.get("Humidity")
    # all_lng     = request.form.get("")
    # all_lat     = request.form.get("")
   
    data.state         = state
    data.day_of_week   = day_of_week
    data.hour          = hour       
    data.sun           = sun        
    data.weather       = weather    
    data.temperature   = temperature
    data.wind          = wind       
    data.precipitation = precipitation
    data.humidity      = humidity   
    # data.all_lng     = all_lng    
    # data.all_lat     = all_lat    
    
    # if data.day_of_week == None:
    #     data.feats=[np.array([lng,lat,clear,cloudy,rain,snow,low_vis,day,night])]
    # else:
    #     data.feats=np.array([float(lng),float(lat),clear=="True",cloudy=="True",rain=="True",snow=="True",low_vis=="True",day=="True",night=="True"])
    # data.temperature = g
    # data.weather = d
    print("***********************************************")
    print(data.day_of_week)
    print(data.state)
    print(data.temperature)
    print(data.humidity)
    print("***********************************************")
    return render_template('NY.html')


@app.route('/data',methods=["GET","POST"])
def data():

    # df = pd.read_csv(r'C:\Users\Kunal\Desktop\GeorgiaTechOMSCS\DVA-CSE6242-Spring-2021\MapWithFlask\templates\coordinates.csv')
    # df = df[df.columns[-2:]]

    # data.all_lat = df.values[:,0].tolist()
    # data.all_lng = df.values[:,1].tolist()
    
    data.state = 'New York'

    if data.day_of_week != None:

        state_coordinates = df[df['State'] == us_state_abbrev[data.state]]
        state_coordinates = state_coordinates.sample(n=2500,random_state=np.random.RandomState())
        data.all_lat = state_coordinates.values[:,0].tolist()
        data.all_lng = state_coordinates.values[:,1].tolist()

        current_day_of_week   = weekdays[data.day_of_week]
        current_hour          = int(data.hour)
        current_sun           = sunrise_sunset[data.sun]        
        current_weather       = weather_cond[data.weather]
        current_temperature   = int(data.temperature)
        current_wind          = int(data.wind)   
        current_precipitation = float(data.precipitation)
        current_humidity      = int(data.humidity)  
        

        test_data = []
        for i in range(len(data.all_lat)):
            # print("day",current_day_of_week)
            # print("hour",current_hour)
            # print("sun",current_sun)
            # print("weather",current_weather)
            # print("temperature",current_temperature)
            # print("wind",current_wind)
            # print("precipitation",current_precipitation)
            # print("humidity",current_humidity)
            # print(data.all_lat[i])
            # print(data.all_lng[i])
            # Adding each row in the order:
            # Lat,Lng,Temp,Humidity,Wind,Precipitaion,Sun,hour,day_of_week,cloudy,fog,rain,snow_ice,thunderstorm
            current_row = [data.all_lat[i],
                           data.all_lng[i],
                           current_temperature,
                           current_humidity,
                           current_wind,
                           current_precipitation,
                           current_sun,
                           current_hour,
                           current_day_of_week]+current_weather

            test_data.append(current_row)

        test_data_input = np.array(test_data)

        predictions = clf.predict(test_data_input).tolist()
        
    else:
        data.all_lat = []
        data.all_lng = []
        predictions = []

    conditions = {
        "day_of_week"   : data.day_of_week,
        "hour"          : data.hour,       
        "sun"           : data.sun,       
        "weather"       : data.weather,    
        "temperature"   : data.temperature,
        "wind"          : data.wind,       
        "precipitation" : data.precipitation,
        "humidity"      : data.humidity,
        "longitude"     : data.all_lng,
        "latitude"      : data.all_lat,
        "predictions"   : predictions                  
    }
    return conditions

@app.route('/get-severity',methods=["GET","POST"])
def predict_severity():
    if data.clear != None:
        print(type(loaded_model.predict([data.feats])))
        return {"severity":loaded_model.predict([data.feats]).tolist()}
    else:
        return {"severity":-1}
