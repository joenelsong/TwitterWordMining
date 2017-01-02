
import sqlite3
import os
import sys
import datetime

def db_add_records(vendor_ids, twitter_id, tweet, user_id, timestamp, sent_pol, sent_sub):
    #retweeted = 1 if retweeted == "True" else 0 # Convert from True/False to 1/0
    print "[", datetime.datetime.now(), "] *** Adding records to database for vendors/terms: ", vendor_ids
    
    try:
        cur.execute(''' INSERT INTO Tweets(tweet_id, tweet, user_id, timestamp, sentiment_polarity, sentiment_subjectivity) VALUES (?,?,?,?,?,?)''', (twitter_id, tweet, user_id, timestamp, sent_pol, sent_sub))
        for i in range( len( vendor_ids) ):
            cur.execute(''' INSERT INTO VendorsTweets(vendor_id, tweet_id) VALUES (?,?)''', (vendor_ids[i], twitter_id))
            
        con.commit()
    except sqlite3.OperationalError:
        print("Database was locked")
    
        
def path():
    pathname = os.path.dirname(sys.argv[0])        
    asbPath = os.path.abspath(pathname)
    return str(asbPath)
    
def db_datetime(timestamp_ms): # import datetime, 
    timestamp = timestamp_ms[:10] # trash milliseconds from timestamp
    d = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
    # returns string of format: yyyy-mm-dd hh:mm:ss ; compatiable with sqlite3 DATETIME
    return d
    
def db_close():
    con.close()
    
def create_db():
    # Create Tables
    try:
        cur.executescript("""CREATE TABLE IF NOT EXISTS Vendors(vendor_id INTEGER(2) PRIMARY KEY, vendor_name VARCHAR(20)); INSERT INTO Vendors Values(1, 'Cisco'); INSERT INTO Vendors Values(2, 'AWS'); INSERT INTO Vendors Values(3, 'Microsoft Sharepoint'); INSERT INTO Vendors Values(4, 'linux'); INSERT INTO Vendors Values(5, 'powershell'); INSERT INTO Vendors Values(6, 'itil'); INSERT INTO Vendors Values(7, 'sql'); INSERT INTO Vendors Values(8, 'azure'); INSERT INTO Vendors Values(9, "ceh");
        CREATE TABLE IF NOT EXISTS Tweets(tweet_id INTEGER(24) PRIMARY KEY, tweet VARCHAR(140), user_id INTEGER(16), timestamp DATETIME, sentiment_polarity FLOAT, sentiment_subjectivity FLOAT); 
        CREATE TABLE IF NOT EXISTS VendorsTweets(vendor_id INTEGER(1), tweet_id INTEGER(10), PRIMARY KEY(vendor_id, tweet_id)  ); """)
        con.commit()
        print("Creating new Database")
        #con.close()
    except:
        print("Connected to Existing Database")
    #con.close()


DB = os.path.join(path(), 'IT_Vendors_Terms.db')
con = sqlite3.connect(DB)
con.text_factory = str
cur = con.cursor() 

if __name__ == "__main__":
    
    create_db()


#DB = os.path.join(path(), 'IT_Vendors.db')

#create_db()
# Test Entries
#db_add_records( 1, "0123456789", "simulated test tweet from Cisco", True, db_datetime("1471832026123") )
#db_add_record( 4, "simulated test tweet from linux sudoooo", db_datetime("1471830765752") )

