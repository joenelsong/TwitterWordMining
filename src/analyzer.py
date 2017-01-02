'''
Author: Joey Nelson
Dev Env: Python 2.7.12
'''
import sys
import pandas as pd
import sqlite3
from textblob import TextBlob
#import elasticsearch opted for a simple database design concerned with just a few attributes

# Querries

q_All = """
SELECT vendor_name, count(*) as tweet_ct, avg(sentiment_polarity), avg(sentiment_subjectivity)
FROM Tweets as t
JOIN VendorsTweets USING(tweet_id)
JOIN Vendors USING(vendor_id)
GROUP BY vendor_id
ORDER BY tweet_ct desc
"""
# Unused Querries because I opted to perform organization in python and only needed 1 querry for this simple report 
q_VendorTweetCounts = """
SELECT vendor_name, count(*) as tweet_ct 
FROM Tweets as t
JOIN VendorsTweets USING(tweet_id)
JOIN Vendors USING(vendor_id)
GROUP BY vendor_id
ORDER BY tweet_ct desc"""

q_MostTweetedVendor = """
SELECT y.vendor_name as 'Vendor Name', max(y.tweet_ct) as 'Number of Tweets'
FROM (
SELECT vendor_name, count(*) as tweet_ct FROM Tweets as t
JOIN VendorsTweets USING(tweet_id)
JOIN Vendors USING(vendor_id)
GROUP BY vendor_id)y"""

def main(db_path):
    con = sqlite3.connect(db_path)
    print'Querrying Database:',db_path
    qdf = pd.read_sql_query(q_All, con)
    print qdf
    
    print "<<<Tweet Count Comparison>>>"
    print qdf.head(1).values[0][0], "is the most tweeted about vendor/term (",qdf.head(1).values[0][1],"tweets )"
    print qdf.tail(1).values[0][0], "is the least tweeted about vendor/term (",qdf.tail(1).values[0][1],"tweets )\n"

    # Sort By Sentiment Polarity -- -1 = negative, 0 = neutral, 1 = positive
    print "<<<Sentiment Analysis>>>"
    print "-1 = negative, 0 = neutral, 1 = positive"
    qdf.sort_values( 'avg(sentiment_polarity)' , ascending=False, inplace=True)
    print qdf.head(1).values[0][0], "has the most positive sentiment among vendors/terms ( score:",round(qdf.head(1).values[0][2],4),")"
    print qdf.tail(1).values[0][0], "has the most negative sentiment among vendors/terms ( score:",round(qdf.tail(1).values[0][2],4),")"


if __name__ == "__main__":
    if ( len(sys.argv) > 0):
        db_path = sys.argv[1]
        main(db_path)
    else:
        print "ERROR: Missing Argument Correct usage is:\n>python analyzer.py IT_Vendors_Terms.db" 