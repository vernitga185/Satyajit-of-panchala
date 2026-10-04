import requests

API_KEY = 'rnd_T3DQKBHCV4cHLF3w8X1MvTCd5bCH'
HEADERS = {'Authorization': f'Bearer {API_KEY}', 'Accept': 'application/json'}

# 1. List Services
res = requests.get('https://api.render.com/v1/services', headers=HEADERS)
services = res.json()

for srv_wrapper in services:
    srv = srv_wrapper.get('service', {})
    name = srv.get('name', '')
    if 'satyajit' in name.lower() or 'panchala' in name.lower():
        print(f"Found service: {name} ({srv.get('id')})")
        
        # 2. Get latest deploy
        srv_id = srv.get('id')
        dep_res = requests.get(f'https://api.render.com/v1/services/{srv_id}/deploys?limit=1', headers=HEADERS)
        deploys = dep_res.json()
        if deploys:
            dep = deploys[0].get('deploy', {})
            dep_id = dep.get('id')
            status = dep.get('status')
            print(f"Latest deploy: {dep_id} (Status: {status})")
            
            # 3. Get server logs or deploy logs
            # Actually Render doesn't expose deploy logs directly via a simple /logs endpoint in v1, wait, do they?
            pass
        else:
            print("No deploys found.")
