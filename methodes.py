import requests
import json


def get_one_prediction(model_version, pat_id):
    json_request = {'model_version': 1,
                    'patId': 1}
    headers = {'Content-Type': 'application/json'}
    json_request['model_version'] = model_version
    json_request['patId'] = pat_id
    data = {}
    rsp = requests.post('http://147.102.33.191:29000/heartf/predict', data=json.dumps(json_request), headers=headers)
    if rsp.status_code == 200 or rsp.status_code == 201:
        max_elm = get_maximum_from_array(rsp.json()['prediction'])
        data[pat_id] = [rsp.json()['prediction'][max_elm], rsp.json()['day'][max_elm]]
    return data


def get_one_prediction_all_data(model_version, pat_id):
    json_request = {'model_version': 1,
                    'patId': 1}
    headers = {'Content-Type': 'application/json'}
    json_request['model_version'] = model_version
    json_request['patId'] = pat_id
    data = {}
    rsp = requests.post('http://147.102.33.191:29000/heartf/predict', data=json.dumps(json_request), headers=headers)
    if rsp.status_code == 200 or rsp.status_code == 201:
        data[pat_id] = [regulate_data(rsp.json()['prediction']), rsp.json()['day']]
    return data


def get_all_prediction(model_version):
    json_request = {'model_version': 1,
                    'patId': 1}
    headers = {'Content-Type': 'application/json'}
    json_request['model_version'] = model_version
    data = {}
    for i in range(100271, 100570):
        json_request['patId'] = i
        rsp = requests.post('http://147.102.33.191:29000/heartf/predict', data=json.dumps(json_request), headers=headers)
        if rsp.status_code == 200 or rsp.status_code == 201:
            max_elm = get_maximum_from_array(rsp.json()['prediction'])
            data[i] = [rsp.json()['prediction'][max_elm], rsp.json()['day'][max_elm]]
    return data


def get_maximum_from_array(array):
    max_element = 0
    pos = 0
    for i, value in enumerate(array):
        if max_element < value:
            max_element = value
            pos = i

    return pos


def regulate_data(array):
    data = []
    for i in array:
        data.append(int(round(i, 2) * 100))
    return data
