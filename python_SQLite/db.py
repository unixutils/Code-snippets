#!/usr/bin/python
#import dbops
from dbops import *

application_name="user1"
database_name="passWD"
host_name="server1.domain.com"
db_file="maruthy.db"

create_connection(db_file)
create_table(db_file)

print("adding new entry")
add_host(db_file, host_name, application_name, database_name)
listhosts(db_file, "ALL")

print("deleting entry")
delete_host(db_file, host_name, application_name, database_name)
listhosts(db_file, "ALL")
