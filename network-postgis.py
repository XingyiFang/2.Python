__author__ = 'Han'
import psycopg2,json, sys
import time
import threading

class ThreadClass(threading.Thread):
    def __init__(self, start, end):
        threading.Thread.__init__(self)
        self.thread_start = start
        self.thread_end = end
        self.thread_stop = False

    def run(self):
        start_time = time.time()
        try:
            conn = psycopg2.connect("dbname='network01' user='postgres' port='5432' host='localhost' password='qinhan1021'")
        except:
            print "I am unable to connect to the database"
        mydict = {}

        #area_model, from 54 - 143
        for i in xrange(self.thread_start, self.thread_end):
            for j in xrange(i, 175):
                cur = conn.cursor()
                cur.execute("SELECT id2 AS edge FROM pgr_dijkstra('SELECT id, source, target, st_length(geom) as cost FROM area_model', " + str(i) + ", " + str(j) + ", false, false) as di;")
                rows = cur.fetchall()
                for row in rows:
                    if row[0] in mydict:
                        mydict[row[0]] += 1
                    else:
                        mydict[row[0]] = 1
                cur.close()
                conn.commit()
            print i
            print("--- %s seconds ---" % (time.time() - start_time))

        for key in mydict.iterkeys():
            cur = conn.cursor()
            cur.execute("UPDATE area_model SET frequency = frequency + " + str(mydict[key]) + " WHERE id = "+ str(key) + ";")
            cur.close()
            conn.commit()

        conn.close()
        json.dump(mydict, open("E:/3. Projects/7. network/python/results.txt", 'a'))

        print("--- %s final seconds ---" % (time.time() - start_time))

    def stop(self):
        self.thread_stop = True


def test():
    #thread1 = ThreadClass(int(sys.argv[1]), int(sys.argv[2]))
    #thread2 = ThreadClass(int(sys.argv[3]), int(sys.argv[4]))
	#you can set the variables here, and then run with the commond line as following: the #1,2,3,4 are the input. 
    #python.exe "e:\3. Projects\7. network\python\network-version2.py" #1 #2 #3 #4
    thread1 = ThreadClass(1,95)
    thread2 = ThreadClass(95, 175)
    thread1.start()
    thread2.start()
    #time.sleep(10)
    #thread1.stop()
    #thread2.stop()
    return

if __name__ == '__main__':
    test()