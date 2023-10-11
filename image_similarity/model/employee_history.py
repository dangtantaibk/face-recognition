from datetime import datetime
import os
import uuid

class EmployeeHistory: 
    id = 0;
    name = '';
    datetime = datetime.now();
    isCheckIn = False;
    image = ''
    def __init__(self,id,name,date = None,image = None,isCheckIn = None):
        self.id = id;
        self.name = name;

        self.datetime = datetime.now();
        self.isCheckIn = isCheckIn;
        if image != None:
            self.image == image 
        else:
            dateStr = self.datetime.strftime('%Y_%m_%d')
            timeStr = self.datetime.strftime('%H_%M_%S_%f')
            path = "./data/images/{0}".format(dateStr);
# Check whether the specified path exists or not
            isExist = os.path.exists(path)
            if not isExist:
                os.makedirs(path)
            url = "{0}/{1}_{2}.jpg".format(path,name,timeStr)
            # print('url',url);
            self.image = url;
        if date != None:
            self.datetime = date;
                   
    def __str__(self):
        # date = self.datetime.strftime("%Y%m%d-%H:%M:%S");
        return f"""INSERT INTO employee_history(id,name, date_time,image,isCheckIn) VALUES(\'{self.id}\',\'{self.name}\',\'{self.datetime}\',\'{self.image}\',\'{self.isCheckIn}\')""";
        # return f"{start}\"id\":\"{self.id}\",\"name\":\"{self.name}\",\"datetime\":\"{date}\",\"isCheckIn\":\"{self.isCheckIn}\"{end},";
    def value(self):
        id = uuid.uuid4().__str__();
        return (id,self.id, self.name ,self.datetime,self.image,self.isCheckIn)
class EmployeeHistoryCheckInDictionary: 
    thisdict = {
        
    }
class EmployeeHistoryCheckOutDictionary: 
    thisdict = {
        
    }
    
    
        