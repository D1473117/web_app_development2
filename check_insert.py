import urllib.request
import urllib.parse
base_url = 'http://127.0.0.1:5000'
data = urllib.parse.urlencode({
    'amount': '10000',
    'type': 'income',
    'category_id': '7',
    'date': '2026-04-23',
    'note': 'Test 10000'
}).encode('utf-8')
req = urllib.request.Request(base_url + '/transactions', data=data, method='POST')
try:
    with urllib.request.urlopen(req) as response:
        print('Status:', response.status)
except Exception as e:
    print('Error:', e)
