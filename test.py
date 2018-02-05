import requests
import json
import time


def send_request():
    # API 1
    # PUT https://api.atmchain.io/v2/user

    try:
        response = requests.put(
            url="https://api.atmchain.io/v2/user",
            headers={
                "Content-Type": "application/json; charset=utf-8",
            },
            data=json.dumps({
                "userinfo": {
                    "firstName": "1111",
                    "lastName": "2222"
                },
                "sourceid": "user01",
                "source": "1xia1snanjsuanslowansxsuaiwnsnnaxsanjdsiiansiasxjjsnahsxjansnahjsxkxnajahsa"
            })
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(
            content=response.content.decode()))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


def send_request1():
    # API 1
    # GET https://api.atmchain.io/v2/user

    try:
        response = requests.get(
            url="https://api.atmchain.io/v2/user",
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            },
            data={
                "sourceid": "test1_user3e",
                "source": "s3m",
            },
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(
            content=response.content.decode()))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


def send_request3(transfer_data):
    # API 1
    # PUT https://api.atmchain.io/v2/transaction

    try:
        response = requests.put(
            url="https://api.atmchain.io/v2/transaction",
            headers={
                "Content-Type": "application/json; charset=utf-8",
            },
            data=json.dumps(transfer_data)
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        print('Response HTTP Response Body: {content}'.format(
            content=response.content))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


transfer_data = {
                "source": "s3m",
                "from": "0x2cDB4F9B25d6Eb544C6971d4542ef096bFa28Ea5",
                "detail": {
                    "txAmount": 0,
                    "txDetail": "test detail",
                    "merchantNo": 18022800,
                    "txTimestamp": 0,
                    "merchantTxId": 0,
                    "merchantTxNo": "xiaoshangxing"
                },
                "sourceid": "test1_user3e",
                "value": 0,
                "to": "0x12a3C0Ed5Cf70F7Ad4F7641313cd8bD0f9d207C7",
                "timestamp": 0,
                "sign": "xxxx"
            }

for i in range(1):
    _value = 100.0 + i * 0.19
    _merchantNo = 18022800 + i
    _merchantTxId = 9700100 + i

    _time = int(time.time())
    transfer_data["detail"]["merchantNo"] = _merchantNo
    transfer_data["detail"]["txTimestamp"] = _time
    transfer_data["detail"]["merchantTxId"] = _merchantTxId
    transfer_data["value"] = _value
    send_request3()
