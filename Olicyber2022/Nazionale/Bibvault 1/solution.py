import base64, json

def b64(data):
    return base64.urlsafe_b64encode(json.dumps(data, separators=(',',':')).encode()).strip(b'=').decode()

token = f"{b64({'alg':'HS256','typ':'JWT'})}.{b64({'username':'gabibbo','is_admin':'true'})}.firmafalsa"
print(token)