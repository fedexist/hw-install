import pyhs2
import time
import sys

with pyhs2.connect(host='localhost',
               port=10500, #hive 2 port
               authMechanism="PLAIN",
               user='admin',
               password='grebeteam', #LOOK AWAY
               database='data_stream') as conn:
    with conn.cursor() as cur:
        #Show databases
        cur.getDatabases()

        #Execute query
		
        #cur.execute("delete from active_table where id=1")
        #cur.execute("update active_table SET origin='GOA' WHERE id = 1")
        #cur.execute("insert into active_table values(1,'MXP','JFK',100.0,100.0,"+ str(time.time()) +",'robovolante')")
		
        cur.execute("select * from active_table limit 1000")
		
        #Return column info from query
        cur.getSchema()

		
        #Fetch table results
       ''' for record in cur.fetch():
            timestamp = record[5]
            id = record[0]
            if time.time() - 60000 >  timestamp:
                if id > max_id:
                    max_id = id
                if id < min_id:
                    min_id = id	
        if max_id > min_id:'''
        cur.execute("DELETE from active_table WHERE time < "+ str(time.time() - 60000))