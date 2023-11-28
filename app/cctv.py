import requests


def get_cctv_data():
    api_url = 'https://www.seogu.go.kr/seoguAPI/3660000/getCctvLifeSecrty'
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        data = data.get('response').get('body')
        return filter_cctv_data(data)
    else:
        print("Error: CCTV data could not be loaded")


def filter_cctv_data(data):
    amount = data.get('totalCnt')
    response_items = data.get('items')
    cctv_list = []
    for element in response_items:
        e = {"lat": element.get("la"), "lon": element.get("lo")}
        cctv_list.append(e)
    return {"cctvs": cctv_list}