#import mysql.connector

#def get_db_connection():
   # return mysql.connector.connect(
      #  host="localhost",
     #   user="root",
    #    password="Shadha@123",
   #     database="cems"
  # )

#import os
#from flask_sqlalchemy import SQLAlchemy

#db = SQLAlchemy()

#def get_database_uri():
    # If running online (Render / hosting)
    #if os.environ.get("DATABASE_URL"):
     #   return os.environ.get("DATABASE_URL")

    # Local MySQL (your existing setup)
    #return "mysql+pymysql://root:Shadha@123@localhost:3306/cems"
#from flask_sqlalchemy import SQLAlchemy

#db = SQLAlchemy()

#def get_database_uri():
 #   return "sqlite:///demo.db"   # for demo
#from flask_sqlalchemy import SQLAlchemy

#db = SQLAlchemy()

#def get_database_uri():
 #   return "sqlite:///online.db"
#import os
#import pymysql

#def get_db_connection():
 #   return pymysql.connect(
  #      host=os.getenv('mysql-e0c909d-shadhafathima333-a069.k.aivencloud.com'),
   #     user=os.getenv('avnadmin'),
    #    password=os.getenv('AVNS_cVBv68tdS2nGKxhqDq1'),
     #   database=os.getenv('defaultdb'),
      #  port=int(os.getenv('12574', 3306)),
       # cursorclass=pymysql.cursors.DictCursor
    #)
import mysql.connector
def get_db_connection():
    return mysql.connector.connect(
    host="switchyard.proxy.rlwy.net",
    port=10105,
    user="root",
    password="hCBvTAOKnlUJrKHhGiwMvxqNFgWqnpZD",
    database="railway"
)

