class Camera():
    name = '';
    isCheckIn = False;
    id = 0;
    url = ''; 
    def __init__(self, url,id,name,isCheckIn):
        self.name = name;
        self.id = id;
        self.isCheckIn = isCheckIn;
        self.url = url;