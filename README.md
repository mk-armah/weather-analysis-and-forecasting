
Analyze weather data from Open Weather API




# How to make an API call
API call
https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={lat}&lon={lon}&dt={time}&appid={APIkey}

### API Parameters

lat, lon	required	Geographical coordinates (latitude, longitude)

dt	required	Date from the previous five days (Unix time, UTC time zone), e.g. dt=1586468027

appid	required	Your unique API key (you can always find it on your account page under the "API key" tab)

exclude	optional	By using this parameter you can exclude some parts of the weather data from the API response. It should be a comma-delimited list (without spaces).

Available values:

>  current, 
> minutely, 
> hourly, 
> daily, 
> alerts

units	optional	Units of measurement. standard, metric and imperial units are available. If you do not use the units parameter, standard units will be applied by default. 

For temperature in Celsius and wind speed in meter/sec, use units=metric --->         <i>This option was chosen for this project</i>

lang	optional	You can use the lang parameter to get the output in your language.<br/>
cite : OpenWeather, https://openweathermap.org/api/one-call-api#history
