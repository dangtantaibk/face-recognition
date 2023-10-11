from ast import Try
from copyreg import constructor
from syslog import LOG_CONS
from telnetlib import EL
from tkinter import E, N
from data_provider import *;
from model.employee_history import *
from model.in_out_employee import *;
from datetime import datetime
from datetime import timedelta
from helpers.common import *
import cv2
import threading
from services.api import *
class EmployeeHistoryController:
    provider = DataProvider();
    def __init__(self):
        self.provider = DataProvider();
    def delete(self):
        self.provider.execute("""delete from employee_history""");

    def insert(self,name,frame,isCheckIn,emit):
        try:
            if name == 'unknown':
                return;
            log = EmployeeHistory(name,name,None,None,isCheckIn);
            logCurrent = None;
            if isCheckIn == True:    
                logCurrent = EmployeeHistoryCheckInDictionary.thisdict.get(name);
                if logCurrent != None:
                    past = compareDatetime(datetime.now(), logCurrent.datetime);
                    if past == False:
                        return;
                    self.saveData(log,frame);      
                    EmployeeHistoryCheckInDictionary.thisdict[name] = log;
                    return;
                EmployeeHistoryCheckInDictionary.thisdict[name] = log;
            else:
                logCurrent = EmployeeHistoryCheckOutDictionary.thisdict.get(name);
                if logCurrent != None:
                    past = compareDatetime(datetime.now(), logCurrent.datetime);
                    if past == False:
                        return;
                EmployeeHistoryCheckOutDictionary.thisdict[name] = log;
                
            try:
                inDate = None;
                outDate = None
                if isCheckIn == True:
                    inDate = log.datetime;
                else:
                    outDate = log.datetime;
                inOut = InOutEmployee(name,name,inDate,outDate,log.image,log.isCheckIn);
                if emit:
                    emit((inOut,'update',isCheckIn,1));
            except Exception as err:
                print('err ',err);
     
            self.saveData(log,frame);      
            # print('log __str__',log.__str__())
        except Exception as err:
            print("ERROR ______  ERROR ",err)
    def saveData(self,log : EmployeeHistory,frame):
        self.saveImage(log.image, frame)
        self.provider.execute("""INSERT INTO employee_history(uuid,id,name, date_time,image,isCheckIn) VALUES(?,?,?,?,?,?)""",log.value());
    def saveImage(self,name,frame):
        # width, height = frame.size();
        # new_size = (width//2, height//2)
        # resized_frame = frame.resize(new_size)
        # resized_frame.save(name, optimize=True, quality=30)
        # resize_frame = cv2.resize(frame, (700,500), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(name, frame,[int(cv2.IMWRITE_JPEG_QUALITY), 90]) 
    # if os.path.exists(fileName):
        #     f = open(fileName, "r")
        #     print('file',f.read())
        # self.getInOutEmployee();
    # def getEmployeeHistory(self):
    #     # print("fetchall")
    #     data = self.provider.fetchall("""select id,name, date_time,isCheckIn from employee_history""");
    #     # print("DATA --- DATA ----- ",data);
    #     list = [];
    #     for item in data:
    #         # id,name,date,isCheckIn = item;
    #         datetime_object = datetime.strptime(item[2], '%Y-%m-%d %H:%M:%S.%f')
    #         print('datetime_object',datetime_object);
    #         employeeHistory = EmployeeHistory(item[0],item[1],datetime_object,item[3]);
    #         list.append(employeeHistory)
    #     print("LIST --- LIST ----- ",list);
    def updateEmployeeHistoryDictionary(self):
        try:
            EmployeeHistoryCheckInDictionary.thisdict.clear();
            data = self.provider.fetchall("""select id,name,date_time,image,isCheckIn,uuid from employee_history where STRFTIME('%d/%m/%Y',date_time)=STRFTIME('%d/%m/%Y',DATE()) ORDER BY date_time ASC""");
            print("DATA --- DATA updateEmployeeHistoryDictionary ----- ",data);
            for item in data:
                id = item[0];
                name = item[1];
                datetime_object = datetime.strptime(item[2], '%Y-%m-%d %H:%M:%S.%f')
                image = item[3];
                isCheckIn = item[4] ==1;
                employeeHistory = EmployeeHistory(id,name,datetime_object,image,isCheckIn);
                if isCheckIn == True:
                    employeeCurrent = EmployeeHistoryCheckInDictionary.thisdict.get(id)
                    if employeeCurrent != None:
                        return;
                    EmployeeHistoryCheckInDictionary.thisdict[id] = employeeHistory;
                else:
                    EmployeeHistoryCheckOutDictionary.thisdict[id] = employeeHistory;
        except Exception as err:
            print("ERROR updateEmployeeHistoryDictionary ",err)
            pass
        print('EmployeeHistoryDictionary.thisdict',EmployeeHistoryCheckInDictionary.thisdict)
    def asyncServer(self):        
        def timeout():
            data = self.provider.fetchall("""select id,name,date_time,image,isCheckIn,isSend,uuid from employee_history where isSend is null and isUpload = 1""");
            print("DATA --- DATA asyncServer----- ",data);
            if data == None:
                return [];
            if len(data) == 0:
                return;
            arr = []
            for item in data:
                id = item[0];
                name = item[1];
                date = item[2]
                image = item[3];
                isCheckIn = item[4] ;
                obj = {
                    "code" : id,
                    "image" : image,
                    "dateTime" : date,
                    "isCheckIn" : isCheckIn
                }
                arr.append(obj);
            api = Api();
            data ={
                'logs' :arr
            }
            result = api.post('log/create', data);
            print('result',result);
            if  result.get('code') == 0:
                self.provider.execute("""update employee_history set isSend=1 where isSend is null and isUpload = 1""");
        timeout();
        t =  threading.Timer(300,timeout)
        t.start();
    
    def asyncImage(self):  
        def uploadImage():
            data = self.provider.fetchall("""select uuid,image from employee_history where isUpload is null and isSend is null""");
            print(' asyncImage data', data);
            if data == None:
                return;
            if len(data) == 0:
                return;
            for item in data:
                uuid = item[0];
                image = item[1];
                api = Api();
                result = api.upload('upload/image', image);
                print('result',result);
                print('result.get code',result.get('code'));
                if result.get('code') == 0:
                    link = result.get('data').get('image');
                    # print('link',link);
                    try:
                        self.provider.execute("""update employee_history set image=?,isUpload=? where uuid=?""", (link,True,uuid));
                    except Exception as err:
                        print('err', err);
        uploadImage();
        t =  threading.Timer(120, uploadImage)
        t.start();
        
    def getInOutEmployee(self):
        
        thisdict = {

        }
        # for item in range(1,500):
        #     id = "NV_{0}".format(item);
        #     thisdict[id] = InOutEmployee(id,id,datetime.now(),None,"",True)
        try:
            data = self.provider.fetchall("""select id,name, date_time,image,isCheckIn,isUpload,isSend from employee_history where STRFTIME('%d/%m/%Y',date_time)=STRFTIME('%d/%m/%Y',DATE()) ORDER BY date_time ASC""");
            print("DATA --- DATA ----- ",data);
            for item in data:
                # id ,name ,date ,isCheckIn = item;
                id = item[0];
                name = item[1];
                datetime_object = datetime.strptime(item[2], '%Y-%m-%d %H:%M:%S.%f')
                image = item[3];
                date = datetime_object;            
                isCheckIn = item[4] == 1;
                print('item[4]',item[4]);

                employeeHistory = EmployeeHistory(id ,name ,datetime_object ,image ,isCheckIn);
                if isCheckIn:
                    employeeCurrent = EmployeeHistoryCheckInDictionary.thisdict.get(id)
                    if employeeCurrent == None:
                        EmployeeHistoryCheckInDictionary.thisdict[id] = employeeHistory;
                else:
                    EmployeeHistoryCheckOutDictionary.thisdict[id] = employeeHistory
          
                inOutCurrent = thisdict.get(id);
                print('inOutCurrent',inOutCurrent);
                print('isCheckIn',isCheckIn);
                if inOutCurrent != None:
                    if isCheckIn == True:
                        if inOutCurrent.inDate == None: 
                            inOutCurrent.inDate = date;
                    else:
                        inOutCurrent.outDate = date;
                else:
                    inDate = None;
                    outDate = None;
                    if isCheckIn == True:
                        inDate = date;
                    else:
                        outDate = date; 
                    inOutCurrent = InOutEmployee(id,name,inDate,outDate,image,True);
                thisdict[id] = inOutCurrent;
                print('end');
        except Exception as err:
            print("ERROR ",err)
        print("thisdict --- thisdict ----- ",thisdict);
        return thisdict;

    
