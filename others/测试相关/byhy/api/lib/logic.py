from pprint import pprint

from others.测试相关.byhy.api.utils.requests_handler import RequestsHandler

baseurl = 'http://127.0.0.1:8047'
req = RequestsHandler()

def login(username, password):
    url = '/api/mgr/signin'
    method = 'post'
    data = {
        'username': username,
        'password': password
    }
    response = req.requests(url=baseurl + url, method=method, data=data)
    print(response)

def add_customer(name, phonenumber, address):
    url = '/api/mgr/customers'
    method = 'POST'
    data = {
        "action": "add_customer",
        "data": {
            "name": name,
            "phonenumber": phonenumber,
            "address": address
        }
    }
    response = req.requests(url=baseurl + url, method=method, json=data)
    print(response)

def list_customer():
    url = '/api/mgr/customers'
    method = 'GET'
    params = {
        "action": "list_customer",
        "pagesize": 100,
        "pagenum": 1
    }
    response = req.requests(url=baseurl + url, method=method, params=params)
    pprint(response)

def put_customer(id, name, phonenumber, address):
    url = '/api/mgr/customers'
    method = 'PUT'
    data = {
        "action": "modify_customer",
        "id": id,
        "newdata": {
            "name": name,
            "phonenumber": phonenumber,
            "address": address
        }
    }
    response = req.requests(url=baseurl + url, method=method, json=data)
    print(response)

def del_customer(id):
    url = '/api/mgr/customers'
    method = 'DELETE'
    data = {
        "action": "del_customer",
        "id": id
    }
    response = req.requests(url=baseurl + url, method=method, json=data)
    print(response)

def add_medicine(name, desc, sn):
    url = '/api/mgr/medicines'
    method = 'POST'
    data = {
        "action": "add_medicine",
        "data": {
            "name": name,
            "desc": desc,
            "sn": sn
        }
    }
    response = req.requests(url=baseurl + url, method=method, json=data)
    print(response)

def list_medicines():
    url = '/api/mgr/medicines'
    method = 'GET'
    params = {
        "action": "list_medicine"
    }
    response = req.requests(url=baseurl + url, method=method, params=params)
    pprint(response)

def put_medicine(id, name, desc, sn):
    url = '/api/mgr/medicines'
    method = 'PUT'
    data = {
        "action": "modify_medicine",
        "id": id,
        "newdata": {
            "name": name,
            "desc": desc,
            "sn": sn
        }
    }
    response = req.requests(url=baseurl + url, method=method, json=data)
    print(response)

def del_medicine(id):
    url = '/api/mgr/medicines'
    method = 'DELETE'
    data = {
        "action": "del_medicine",
        "id": id
    }
    response = req.requests(url=baseurl + url, method=method, json=data)
    print(response)

def add_order(name, customerid, medicinelist):
    url = '/api/mgr/orders'
    method = 'POST'
    data = {
        "action": "add_order",
        "data": {
            "name": name,
            "customerid": customerid,
            "medicinelist": medicinelist
        }
    }
    response = req.requests(url=baseurl + url, method=method, json=data)
    print(response)

def list_orders():
    url = '/api/mgr/orders'
    method = 'GET'
    params = {
        "action": "list_order"
    }
    response = req.requests(url=baseurl + url, method=method, params=params)
    pprint(response)

if __name__ == '__main__':
    login('byhy', '88888888')
    # del_customer(79)
    # list_customer()
    # put_customer(79, '11byhy', '13545667389', '北京')
    # add_customer('byhy', '13545667389', '北京')
    # add_medicine('byhy', 'byhy', '2020-01-01')
    list_medicines()
    # put_medicine(1, '青霉素', '青霉素 国字号', '099877883837')
    # del_medicine(1)
    # add_order('华山医院订单002', 3, [{'id': 16, 'amount': '4', 'name': '环丙沙星'}, {'id': 15, 'amount': '5', 'name': '克林霉素'}])
    # list_orders()
