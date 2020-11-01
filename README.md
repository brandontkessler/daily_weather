# Basic Weather app

A basic weather app that provides some command line info based on provided zip code. 

# Usage

Create a config.json file in the project directory with the following info:

```json
    {
        "MAPQUEST_KEY": "<Mapquest key>",
        "OPENWEATHER_KEY": "<Openweather Key>",
        "ZIPCODE": "<Zip Code>"
    }
```

# Caveats

Openweather can accept a zipcode instead of latitude, longitude coordinates so app can be adjusted but decided to use both anyway just for fun.