
"""
Connect from Python to Oracle via JDBC
Get JDBC-driver here: https://download.oracle.com/otn/utilities_drivers/jdbc/193/ojdbc8-full.tar.gz
Python 3.7.4
conda install -c conda-forge jaydebeapi==1.1.1 --force-reinstall -y
conda install -c conda-forge JPype1==0.6.3 --force-reinstall -y
"""
import sys
import os

import jpype
import jaydebeapi

print(os.getenv("JAVA_HOME"))

#os.environ['JAVA_HOME'] = os.sep.join("C:\Program Files\Java\jdk1.8.0_301")

JHOME = jpype.getDefaultJVMPath()
jpype.startJVM(JHOME, '-Djava.class.path=C:\_DEV\Java\ojdbc6-12.1.0.2.0.jar')
con = jaydebeapi.connect('oracle.jdbc.driver.OracleDriver',
                         'jdbc:oracle:thin:bw/delvag1@localhost/Berichtswesen')
cur = con.cursor()
cur.execute('select dummy from dual')
r = cur.fetchall()
print(r[0][0])
cur.close()
con.close()

#C:\Program Files\Java\jdk1.8.0_301


####import cx_Oracle
####
####connection = cx_Oracle.connect(
####    user="bw",
####    password="",
####    dsn="localhost/Berichtswesen")
####
####print("Successfully connected to Oracle Database")