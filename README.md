<H1>File-Encryptor-Compressor-with-MySql</H1>

Hello Guys, This Program is purely Python Based.

Before starting we have to fullfill all the requirenments. For this follow this steps:-

STEP 1: Installing Dependencies <PIL and MySql.Connector>. Run in terminal > pip install pillow mysql.connector

STEP 2: We should have Mysql DBMS in our system.

STEP 3: Creating a database named "profile" and a relation named "info" in it. run commands in Mysql > CREATE DATABASE profile; > USE profile; > CREATE TABLE info ( USERNAME VARCHAR(25), PASSWORD VARCHAR(25), EMAIL VARCHR(25)); close MySql

STEP 4: Write your MySQL login Password below in "passwd=" attribute in line 45.

Voila! Run main.py.