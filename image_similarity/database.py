import sqlite3
def create(): 
    con = sqlite3.connect("./database/human_resources.db")
    cur = con.cursor()
    # cur.execute("DROP table employee_history")

    cur.execute('CREATE TABLE employee_history(uuid,id,name,date_time,image,isCheckIn,isSend,isUpload)')
create();
