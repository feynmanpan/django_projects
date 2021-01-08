r = requests.post(url, json=postdata)　  # fastapi用BaseModel，要送json
r.encoding = 'utf-8'
res = r.json()
r.close()
