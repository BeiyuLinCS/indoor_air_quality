#!/usr/bin/env python2
"""
This program is written in python2. To run:

python2 example_data_script.py
"""

import datetime
import copy
import psycopg2
import sys

# This program uses psycopg2 to connect to smarthomedata.
# Documentation can be found here.
# http://initd.org/psycopg/docs/
###  python example_data_script.py > ./atmo4.dat


db_conn = psycopg2.connect(database="",
                           host="",
                           port="",
                           user="",
                           password="")


"""
This function converts a 'local' timestamp to the UTC value given the testbed.
"""
def get_utc_stamp(tbname, local_stamp):
    utc_stamp = local_stamp
    SQL = "SELECT timezone('utc', timestamp %s at time zone testbed.timezone) "
    SQL += "FROM testbed WHERE tbname=%s;"
    data = (local_stamp, tbname,)
    with db_conn:
        with db_conn.cursor() as cr:
            cr.execute(SQL, data)
            #print cr.query
            result = cr.fetchone()
            utc_stamp = result[0]
    return utc_stamp

"""
This function returns ALL events from a testbed during the provided stamp ranges.
"""
def get_all_testbed_data(tbname, start_stamp, end_stamp):
    result = list()
    # index vals  0          1            2       3       4        5            6             7         8         9     10      11       12      13        14
    SQL = "SELECT stamp_utc, stamp_local, serial, target, message, sensor_type, package_type, category, event_id, uuid, stamp,  channel, tbname, timezone, by "
    SQL += "FROM all_events WHERE tbname=%s AND stamp BETWEEN %s AND %s;"
    data = (tbname, start_stamp, end_stamp,)
    with db_conn:
        with db_conn.cursor() as cr:
            cr.execute(SQL, data)
            #print cr.query
            for row in cr:
                event = dict()
                # we do a deepcopy of the datetime object as python likes to
                # pass around object by reference if we are not careful.
                event["stamp_utc"] = copy.deepcopy(row[0])
                event["stamp_local"] = copy.deepcopy(row[1])
                event["serial"] = row[2]
                event["target"] = row[3]
                event["message"] = row[4]
                event["sensor_type"] = row[5]
                event["package_type"] = row[6]
                event["category"] = row[7]
                event["event_id"] = row[8]
                event["uuid"] = row[9]
                event["stamp"] = row[10]
                event["channel"] = row[11]
                event["tbname"] = row[12]
                event["timezone"] = row[13]
                event["by"] = row[14]
                #result.append(copy.deepcopy(event))
                print_db_style_events([event])
    return result

"""
This function returns ONLY events from a testbed during the provided stamp ranges
for the given target AND sensor_type.
"""
def get_sensor_testbed_data(tbname, start_stamp, end_stamp, target, sensor_type):
    result = list()
    # index vals  0          1            2       3       4        5            6             7
    SQL = "SELECT stamp_utc, stamp_local, serial, target, message, sensor_type, package_type, category "
    SQL += "FROM all_events WHERE tbname=%s AND stamp BETWEEN %s AND %s AND "
    SQL += "target=%s AND sensor_type=%s;"
    data = (tbname, start_stamp, end_stamp, target, sensor_type,)
    with db_conn:
        with db_conn.cursor() as cr:
            cr.execute(SQL, data)
            #print cr.query
            for row in cr:
                event = dict()
                # we do a deepcopy of the datetime object as python likes to
                # pass around object by reference if we are not careful.
                event["stamp_utc"] = copy.deepcopy(row[0])
                event["stamp_local"] = copy.deepcopy(row[1])
                event["serial"] = row[2]
                event["target"] = row[3]
                event["message"] = row[4]
                event["sensor_type"] = row[5]
                event["package_type"] = row[6]
                event["category"] = row[7]
                result.append(copy.deepcopy(event))
    return result


"""
This function prints ALL events passed to it.
"""
def print_all_events(records):
    for row in records:
        print str(row["stamp_local"]),
        print "\t",
        print row["target"],
        print "\t",
        print row["message"],
        print "\t",
        print row["sensor_type"]
    return

def print_db_style_events(records):
    for row in records:
        print row["event_id"]," | ",row["uuid"]," | ",row["serial"]," | ",row["stamp"]," | ",row["stamp_utc"]," | ",row["stamp_local"]," | ",row["message"]," | ",row["by"]," | ",
        print row["category"]," | ",row["target"]," | ",row["package_type"]," | ",row["sensor_type"]," | ",row["channel"]," | ",row["tbname"]," | ",row["timezone"]
    return

testbedname = "hh102"
local_start_stamp = "2011-12-01"
local_end_stamp = "2011-12-31"
utc_start_stamp = get_utc_stamp(testbedname, local_start_stamp)
utc_end_stamp = get_utc_stamp(testbedname, local_end_stamp)
tb_data = get_all_testbed_data(testbedname, utc_start_stamp, utc_end_stamp)
