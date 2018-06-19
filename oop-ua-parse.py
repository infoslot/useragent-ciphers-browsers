import json, urllib2, sys, MySQLdb
from browsers import browsers
from oopbrowser import oopbrowser


def search_cipher_database(searchstring,current,myConn):
    results = []
    searchstring = "%" + searchstring + "%"
    current.execute("SELECT * FROM uatest WHERE browser_ciphers LIKE %s",(searchstring,) )
    rows = current.fetchall()
    for row in rows:
	results.append(row[1] + ":" +row[2])
    for i in results:
	print i
    print len(results)

def search_cipher_object(searchstring, browserList):
	results = []	
	
	for browser in browserList:
		browser_name = browser.browser_name
		browser_version = browser.browser_version
		browser_ciphers = browser.ciphers
		for cipher in browser_ciphers.split(","):
			if cipher == searchstring:
				results.append(browser_name + ":" + browser_version)
	for result in results:
		print result
	print ("Aantal browsers in het resultaat: ",len(results))

def search_browsertype(searchstring,current,myConn):
    print searchstring
    searchstring = "%" + searchstring + "%"
    current.execute("SELECT * FROM uatest WHERE browser_type LIKE %s",(searchstring,) )
    rows = current.fetchall()
    for row in rows:
	print row[1],row[2]
    
def writeToFile(current,browserList):
    # object = browsers()
    h = open("uatest.csv","w")
    for browser in browserList:
	browser_name = browser.browser_name
	browser_version = browser.browser_version
	browser_ciphers = browser.ciphers
        h.write(browser_name + "," + browser_version + ",")
        for cipher in browser_ciphers:
            h.write(cipher)
    	h.write("\n")


def check_database(current):
    current.execute("SELECT * FROM uatest")
    rows = current.rowcount
    return rows

def setup_database(current):
    sql = 'drop database uatest'
    current.execute(sql)
    sql = 'create database uatest'
    current.execute(sql)
    create_database_structure = ''' 
	use uatest;
	create table uatest(id INT NOT NULL AUTO_INCREMENT,
	browser_type VARCHAR(40) NOT NULL,
	browser_version VARCHAR(40) NOT NULL,
	browser_ciphers VARCHAR(4000) NOT NULL,
	PRIMARY KEY ( id ));'''
    try:
        current.execute(create_database_structure);
    except (MySQLdb.Error, MySQLdb.Warning) as e:
        print(e)
        return None

def loadDatabase(current,myConn,browserList):
    for browser in browserList:
	browser_name = browser.browser_name
	browser_version = browser.browser_version
	browser_ciphers = browser.ciphers
       	current.execute('INSERT INTO uatest(browser_type,browser_version,browser_ciphers) VALUES ("%s","%s","%s")' % (browser_name ,browser_version , browser_ciphers));
       	myConn.commit()

def loadBrowsersObjects():
    r = urllib2.urlopen("https://api.ssllabs.com/api/v3/getClients")
    data = r.read() 
    data = data.decode("utf-8") 
    jsondata = json.loads(data)
    x = len(jsondata)-1
    browserList = []
    while x > 0:
       ciphers = ''       
       name = jsondata[x]['name']
       version = jsondata[x]['version']
       for i in jsondata[x]['suiteNames']:
             ciphers = ciphers+","+i 
       x = x -1;
       browserList.append(oopbrowser(name,version, ciphers))
    return browserList

def main():
	host = '172.17.0.2'
	user = 'uatest'
	passwd = 'uatest'
	db= 'uatest'
    	searchstring = ''
	results = []
	browserList = []

	myConn = MySQLdb.connect(host=host,user=user,passwd=passwd,db=db)
	current = myConn.cursor()
	ciphers = ''
    	setup_database(current)
	browserList = loadBrowsersObjects()
	loadDatabase(current,myConn,browserList)
	if len(sys.argv) > 1:
		searchstring = sys.argv[1]
	rows = check_database(current)
    
	# search_browsertype(searchstring,current,myConn)
	# search_cipher_database(searchstring,current,myConn)
	search_cipher_object(searchstring,browserList)   	
	writeToFile(current,browserList)
	# print(current._last_executed)
   	print ("Totaal aantal browsers in test: ",len(browserList))

			
if __name__ == "__main__":
	main()
