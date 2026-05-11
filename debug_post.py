import urllib.request
import urllib.parse

data = urllib.parse.urlencode({
    'nama': 'Test',
    'email': 't@t.com',
    'NRP': '',
    'password': '',
    'jabatan': '',
    'pangkat': '',
    'no_wa': ''
}).encode()

req = urllib.request.Request('http://127.0.0.1:8000/admin/anggota/edit/CA406BB884', data=data, headers={'Cookie': 'user_email=admin'})
try:
    resp = urllib.request.urlopen(req)
    print("Success:", resp.status)
except Exception as e:
    print("Error HTTP Code:", e.code)
    try:
        print("Error Body:", e.read().decode())
    except:
        pass
