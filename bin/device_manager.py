#!/usr/bin/python
#
# SmartHome
# Copyright (c) 2016 Alexey Baikov <sysboss[@]mail.ru>
#
# udev device manager

import os
import json
import sys, getopt
import textwrap
import pymongo
from pprint import pprint

with open('./config/database.json') as dbconf_file:
    dbconf = json.load(dbconf_file)

# MongoDB config
mongodb_uri = 'mongodb://' + dbconf['dbhost'] + '/' + dbconf['dbname']

def mongo_connect():
    try:
        conn = pymongo.MongoClient( mongodb_uri )
        return conn
    except pymongo.errors.ConnectionFailure, e:
       print "Could not connect to MongoDB: %s" % e
       sys.exit(2)

def add_device(conn, device_data):
    db = conn.get_default_database()

    try:
        db.usb_devices.insert(device_data)
        print "New device added!"
    except pymongo.errors.DuplicateKeyError:
        print "This device is already exist!"
        sys.exit(3)

def remove_device(conn, device_data):
    db = conn.get_default_database()
    result = ''

    try:
        result = db.usb_devices.delete_one( device_data )
    except pymongo.errors:
        print "Failed to remove device"
        sys.exit(2)

    if result.deleted_count < 1:
        print "Device not found"
        sys.exit(3)
    else:
        print "Device removed!"

def list_devices(conn, filter):
    db = conn.get_default_database()
    return db.usb_devices.find(filter)

def usage():
    program = os.path.basename(__file__)
    print "Usage: " + program + " [options]"
    print textwrap.dedent("""\

        --help, -h
                Displays help information

        --action, -a
                Action to do (add or remove)

        --device, -d
                Device name

        --vendor, -v
                Device vendor

        --serial, -s
                Device serial number

        --model, -m
                Device model
    """)
    sys.exit(1)

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"ha:d:v:s:m:l",["action=","device=","vendor=","serial=","model=","list"])
    except getopt.GetoptError:
        usage()
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
        elif opt in ("-a", "--action"):
            action = arg
        elif opt in ("-d", "--device"):
            device = arg
        elif opt in ("-v", "--vendor"):
            vendor = arg
        elif opt in ("-s", "--serial"):
            serial = arg
        elif opt in ("-m", "--model"):
            model = arg
        elif opt in ("-l", "--list"):
            conn = mongo_connect()

            for device in list_devices(conn, {}):
                print device
            sys.exit()

    # check arguments
    if len(sys.argv) < 5:
        print "All arguments are required\n"
        usage()

    print 'Device ', action, device, vendor, serial, model

    device_data = [{
        'device': device,
        'vendor': vendor,
        'model' : model,
        'serial': serial
    }]

    # Connection to MongoDB
    conn = mongo_connect()

    if action == "add":
        add_device(conn, device_data)
    elif action == "remove":
        remove_device(conn, { "device" : device })

if __name__ == "__main__":
   main(sys.argv[1:])
