# infusionsoft-python

InfusionSoft API wrapper for Infusionsoft written in Python.

## Installing
```
git+git://github.com/GearPlug/infusionsoft-python.git
```

## Usage
```
from infusionsoft.client import Client
client = Client('CLIENT_ID', 'CLIENT_SECRET', 'OPTIONAL - access_token')
```
Get authorization url
```
url = client..oauth_access("REDIRECT_URL")
```

Exchange the code for an access token
```
token = client.exchange_code('REDIRECT_URL', 'CODE')
```

Refresh token
```
token = client.refresh_token('REFRESH TOKEN')
```

Set token
```
token = client.set_token('TOKEN')
```

## Requirements
- requests
- base64 -- b64encode

## Tests
```
python test.py
```

## TODO Endpoints
- All Appointments Section
- All File Section
- All Tag Section
