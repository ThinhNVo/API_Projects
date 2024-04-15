# weather_collector.py

### First function

This program auto-collects weather data from Noa with values ranging from temperature, dew point, humidity, wind speed, precipitation, snow amount, and even short forecast description. It then formats the data like max, avg, and min of the values. It also calculates the precipitation of a state from mm to inch.

```python
file.write(today + " forecast: \n")
    file.write(f'Max Temperature: {max_temp} \n')
    file.write(f'Avg Temperature: {avg_temp} \n')
    file.write(f'Min Temperature: {min_temp} \n')
    file.write(f'Max Dew Point: {max_dewP } \n')
    file.write(f'Avg Dew Point: {avg_dewP} \n')
    file.write(f'Min Dew Point: {min_dewP } \n')    
    file.write(f'Max Humidity: {max_humid} \n')
    file.write(f'Avg Humidity: {avg_humid} \n')
    file.write(f'Min Humidity: {min_humid} \n')
    file.write(f'Max wind speed: {max_windS} \n')
    file.write(f'Avg wind speed: {avg_windS} \n')
    file.write(f'Min wind speed: {min_windS} \n')
    file.write(f'precipitation: {actualPrecipitation} \n')
    file.write(f'snow amount: {snowAmount} \n')
    file.write(f'Forecast: {forcast} \n')
```

#### you can comment out the values that you don't want in your report.


```python
file.write(today + " forecast: \n")
    file.write(f'Max Temperature: {max_temp} \n')
    #file.write(f'Avg Temperature: {avg_temp} \n')
    #file.write(f'Min Temperature: {min_temp} \n')
    file.write(f'Max Dew Point: {max_dewP } \n')
    #file.write(f'Avg Dew Point: {avg_dewP} \n')
    #file.write(f'Min Dew Point: {min_dewP } \n')    
    file.write(f'Max Humidity: {max_humid} \n')
    #file.write(f'Avg Humidity: {avg_humid} \n')
    #file.write(f'Min Humidity: {min_humid} \n')
    file.write(f'Max wind speed: {max_windS} \n')
    #file.write(f'Avg wind speed: {avg_windS} \n')
    #file.write(f'Min wind speed: {min_windS} \n')
    file.write(f'precipitation: {actualPrecipitation} \n')
    file.write(f'snow amount: {snowAmount} \n')
    file.write(f'Forecast: {forcast} \n')
```


### Second Function

This program also uploads data to Postgres Database. You can uncomment them and replace username, password, hostname, database_name to your database information.

```python
report_list.extend(weather_functions.database_upload( 'username', 'password', 'hostname', 'database_name', max_temp, avg_temp, min_temp, max_dewP, 
                            avg_dewP, min_dewP, max_humid, avg_humid, 
                            min_humid, max_windS, avg_windS, min_windS, 
                            actualPrecipitation, snowAmount, forcast))
``` 

# install modules

```
pip install requests
pip install uszipcode 
pip install python_Levenshtein
pip install psycopg2 # for database upload
```


# imports modules

## weather_collector's import

```python
import json
import requests
import os
import sys
from datetime import datetime, timedelta
from collections import Counter
from uszipcode import SearchEngine
import weather_functions
```

## weather_function's import

```python
import requests
import os
import sys
import re
import psycopg2 
from datetime import datetime, timedelta
from collections import Counter
from psycopg2 import Error
from uszipcode import SearchEngine
```



# Start the program

``` 
python weather_collector.py
```

