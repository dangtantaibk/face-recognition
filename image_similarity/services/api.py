import requests
from datetime import datetime
class Api: 
    url = 'https://sellercenter.kido.vn/api/';
    def __init__(self):
        print('__init__');
    
    def post(self,url,data):
        path = self.url + url;
        print('data',data);
        response = requests.post(path, json= data);
        if response.status_code != 200:
            return None;
        return response.json();
    
    def get(self,url,params):
        path = self.url + url;
        response = requests.get(path, params = params);
        return response.json();

    def upload(self,url, folder):
        path = self.url + url;
        # print('path',path);
        # print('folder',folder);
        up = {'file':(folder, open(folder, 'rb'), "image/jpeg")}
        # payload={}

        response = requests.post(path, files= up);
        if response.status_code != 200:
            return None;
        # print('response.status_code',response.status_code)
        return response.json();

if __name__ == "__main__":
    arr = []
    # Get the current datetime
    current_datetime = datetime.now()

    # Format the current datetime as per your desired format
    formatted_datetime_string = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    obj = {
        "code" : "tai",
        "image" : "image",
        "dateTime" : formatted_datetime_string,
        "isCheckIn" : 0
    }
    arr.append(obj);
    api = Api();
    data ={
        'logs' :arr
    }
    result = api.post('log/create', data);
    print(result);