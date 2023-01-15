import mysql.connector
import os
import inspect
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

import config

"""
Run test_config.py to update the UID for all test data in the database.
"""

# Establish connection to MySQL DB
conn = mysql.connector.connect(
    user = config.user,
    password = config.password, 
    host = config.host,
    database = config.database
)
    
cur = conn.cursor() 

# Update COMP SCI 577 cUID for testing
cur.execute("SELECT cUID FROM courses WHERE cCode = 'Comp Sci 577'")
cs577_cUID = str(cur.fetchone()[0])

# Update Marc Renault pUID
cur.execute("SELECT pUID FROM professors WHERE pName = 'Marc Renault'")
marc_renault_pUID = str(cur.fetchone()[0])

cur.close()
conn.close()
    