#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import pymysql
from github import Github
from datetime import date
import datetime

## Parse our data
open_count = 0
closed_count = 0 
date = date.today()
formatted_date = date.strftime('%Y-%m-%d')

def parse():
    g = Github("YOUR_ACCESS_TOKEN")
    repo = g.get_repo("aiven/devportal")
    global open_count
    global closed_count

    open_issues = repo.get_issues(state='open')
    for issue in open_issues:  
        open_count += 1

    closed_issues = repo.get_issues(state='closed')
    for issue in closed_issues:  
        closed_count += 1
    
## Write to the database 
def store(): 
    global open_count 
    global closed_count 
    global formatted_date 
    timeout = 10
    connection = pymysql.connect(
        charset="utf8mb4",
        connect_timeout=timeout,
        cursorclass=pymysql.cursors.DictCursor,
        db="YOUR_AIVEN_MYSQL_DB_NAME",
        host="YOUR_AIVEN_MYSQL_HOSTNAME",
        port=YOUR_AIVEN_MYSQL_PORT,
        user="YOUR_AVIEN_MYSQL_USERNAME",
        password="YOUR_AIVEN_MYSQL_PASSWORD",
        read_timeout=timeout,
        write_timeout=timeout,
    )

    query = "INSERT INTO github (`date`, `open`, `closed`) VALUES ('" + formatted_date + "', '" + str(open_count) + "', '" + str(closed_count) + "')" 

    try:

        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS github (`date` DATE PRIMARY KEY, `open` INT, `closed` INT)")
        cursor.execute(query)
        cursor.execute("SELECT * FROM github")
        print(cursor.fetchall())
        connection.commit()

    finally:
        connection.close()

## Execute 
def main():
    parse()
    store()

if __name__ == "__main__":
    main()