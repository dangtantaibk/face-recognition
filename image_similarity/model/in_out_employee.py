
from datetime import datetime
from sqlite3 import Date


class InOutEmployee:
    id ='';
    name = '';
    inDate = datetime.now();
    outDate = datetime.now();
    image = '';
    isCheckIn = True;
    def __init__(self,id,name,inDate,outDate,image,isCheckIn):
        self.id = id;
        self.name = name;
        self.inDate = inDate;
        self.outDate = outDate;
        self.image = image;
        self.isCheckIn = isCheckIn;
    def __str__(self):
            # date = self.datetime.strftime("%Y%m%d-%H:%M:%S");
        return f"(\'{self.id}\',\'{self.name}\',\'{self.inDate}\',\'{self.outDate}\',\'{self.isCheckIn}\')";
        # return f"{start}\"id\":\"{self.id}\",\"name\":\"{self.name}\",\"datetime\":\"{date}\",\"isCheckIn\":\"{self.isCheckIn}\"{end},";