from data_provider import *;
provider = DataProvider();

# provider.execute("""INSERT INTO employee_history(id,name, date_time,isCheckIn) VALUES('Khai','Khai','2023-08-16 09:09:00.140643','False')""");
data = provider.fetchall("""select id,name, date_time,isCheckIn from employee_history""");
print("DATA --- DATA updateEmployeeHistoryDictionary ----- ",data);