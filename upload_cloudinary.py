import os
import time, hashlib, json, urllib.request, urllib.parse, base64

cloud_name = 'dk99mwva6'
api_key = '652529896575495'
api_secret = 'i-yiMuq6Z7Yw1f3KwW84ngNr5zM'
# Use local extracted_icons folder relative to this script
file_path = os.path.join(os.path.dirname(__file__), 'extracted_icons', 'icon256.png')

timestamp = str(int(time.time()))
params_to_sign = f'timestamp={timestamp}{api_secret}'
signature = hashlib.sha1(params_to_sign.encode('utf-8')).hexdigest()

url = f'https://api.cloudinary.com/v1_1/{cloud_name}/image/upload'

with open(file_path, 'rb') as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

data = {
    'file': f'data:image/png;base64,{encoded_string}',
    'api_key': api_key,
    'timestamp': timestamp,
    'signature': signature
}

data_encoded = urllib.parse.urlencode(data).encode('utf-8')
req = urllib.request.Request(url, data=data_encoded)
try:
    with urllib.request.urlopen(req, timeout=60) as response:
        res = json.loads(response.read())
        print('URL_RESULT:' + res['secure_url'])
except Exception as e:
    if hasattr(e, 'read'):
        try:
            print(e.read().decode('utf-8'))
        except:
            print(e)
    else:
        print(e)
