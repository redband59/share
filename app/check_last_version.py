#!/bin/python
import mysql.connector
from mysql.connector import Error
import tarfile
import urllib.request
import re
import os, fnmatch
from datetime import datetime

def download(): #Download of the latest Wordpress version
    url = 'https://wordpress.org/latest.tar.gz'
    urllib.request.urlretrieve(url, '/tmp/latest.tar.gz')

def untar_version_file(): #Untar the tar.gz
    tf = tarfile.open("/tmp/latest.tar.gz")
    tf.extractall()
    tf.close()

def checkversion_ref(): #Scan the version.php for last version
    download()
    global ref
    searchfile = open("./wordpress/wp-includes/version.php", "r")
    for line in searchfile:
        if "wp_version =" in line:
            version = re.search('[0-9]+\.[0-9]+\.?[0-9]*', line)
    searchfile.close()
    ref = version.group(0)
    return ref

def checkversion_list(path_wp):
        global version_inst
        global pattern
        pattern = re.compile('[0-9]+\.[0-9]+\.?[0-9]*')
        version_inst = []
        i = 0
        for instances in path_wp:
            version_inst.append(path_wp[i])
            path_wp[i] = path_wp[i] #+ "/version.php"
            searchfile = open(str(path_wp[i]))
            for line in searchfile:
                if "wp_version =" in line:
                    version_temp = pattern.search(line)
                    version_inst.append(version_temp.group(0))
            i = i + 1
        return version_inst

def compare_ref_w_list(version_inst,ref):
        instance_list = version_inst[0::2]
        inst_count = len(version_inst)
        res_list = []
        index_res = []
        ref_splitted = []
        version_splitted = []

        for version in version_inst[1::2]:
            if version == ref:
                res_list.append("OK")
                res_list.append("#008000")
            else:
                res_list.append("NOK")
                ref_splitted = ref.split('.')
                version_splitted = version.split('.')
                if len(version_splitted) == 3:
                    if version_splitted[0] == ref_splitted[0] and version_splitted[1] == ref_splitted[1]:
                        res_list.append("#FFFF00")
                    elif version_splitted[0] == ref_splitted[0]:
                        res_list.append("#FFA500")
                    else:
                        res_list.append("#FF0000")
                else:
                    if version_splitted[0] == ref_splitted[0] and version_splitted[1] == ref_splitted[1]:
                        res_list.append("#FFFF00")
                    elif version_splitted[0] == ref_splitted[0]:
                        res_list.append("#FFA500")
                    else:
                        res_list.append("#FF0000")
        #print(res_list)

        iterator = 0
        itinstance = 0
        for test in instance_list:
            index_res = version_inst.index(instance_list[itinstance], 0, len(version_inst))
            version_inst.insert((index_res + 2), res_list[iterator])
            version_inst.insert((index_res + 3), res_list[iterator + 1])
            iterator += 2
            itinstance += 1
        print(version_inst)
        return version_inst

def search_index_list(version_inst,a,b,inst):
        instance_list = version_inst[a::b]
        index_res = version_inst.index(inst, 0, len(version_inst))
        return index_res

def find(): #Scan /data/www after all version.php file
        path_root = '/data/www/'
        parent = "wp-includes"
        pattern = "version.php"
        global files
        files = []
        for r, d, f in os.walk(path_root):
            if pattern in f:
                dir = r.split('/')
                if parent in dir:
                    files.append(os.path.join(r, pattern))
        return files

def find_instances_name(version_inst): #Get full name of the instance
        temp_list = []
        instance_name_list = version_inst[0::4]
        i = 0
        for test in instance_name_list:
            root = test.split('/')[i + 1] + "/" + test.split('/')[i + 2]
#            test2 = test.split('/')
#            print(test2)
            try:
                brand = test.split('/')[i + 3]
                index = search_index_list(version_inst,0,3,test)
                version_inst.insert((index + 4), brand)
#                print(version_inst)
            except IndexError:
                brand = None
                index = search_index_list(version_inst,0,3,test)
                version_inst.insert((index + 4), brand)
#            print(brand)

            try:
                instance = test.split('/')[i + 4]
                index = search_index_list(version_inst,0,4,test)
                version_inst.insert((index + 5), instance)
#                print(version_inst)
            except IndexError:
                instance = None
                index = search_index_list(version_inst,0,4,test)
                version_inst.insert((index + 5), instance)
#            print(instance)

            try:
                sub_inst = test.split('/')[i + 5]
                index = search_index_list(version_inst,0,5,test)
                version_inst.insert((index + 6), sub_inst)
#                print(version_inst)
            except IndexError:
                sub_inst = None
                index = search_index_list(version_inst,0,5,test)
                version_inst.insert((index + 6), sub_inst)
#            print(sub_inst)



def initialize_db():
        try :
            connection = mysql.connector.connect(host='', database='wp_version', user='python', password='')
            cursor = connection.cursor()
            try :
                cursor.execute("SELECT 1 FROM wpversion LIMIT 1;")
                print("Table Exists, less work !")
                connection.close()


            except mysql.connector.errors.ProgrammingError as error :
                mySql_Create_Table_Query = """CREATE TABLE IF NOT EXISTS wpversion (path VARCHAR(100) NOT NULL PRIMARY KEY, version VARCHAR(20), status VARCHAR(5), color VARCHAR(20), root VARCHAR(30), brand VARCHAR(30), instance VARCHAR(30), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"""
                result = cursor.execute(mySql_Create_Table_Query)
                print("wpversion table created successfully")
                connection.close()

        except mysql.connector.Error as error:
            print("Failed to create table in MySQL: {}".format(error))

def add_value_2_db(version_inst):
        inst_list = version_inst[0::7]
        print(inst_list)
        i = 0
        try :
            connection = mysql.connector.connect(host='gc-wpdb-prod-aur-2.cluster-c7kjzldcj7hr.eu-central-1.rds.amazonaws.com', database='wp_version', user='python', password='0EwH&*%PU0&hfN#b2qr&cS*r')
            cursor = connection.cursor()
            for inst in inst_list :
                path=version_inst[i]
                version=version_inst[i + 1]
                status=version_inst[i + 2]
                color=version_inst[i + 3]
                root=version_inst[i + 4]
                brand=version_inst[i + 5]
                instance_name=version_inst[i + 6]

                recordTuple = (path, version, status, color, root, brand, instance_name, version, status)
                print(recordTuple)
                #print(recordTuple)
                query = """INSERT INTO wpversion (path, version, status, color, root, brand, instance) VALUES (%s, %s, %s, %s, %s, %s, %s)
                                        ON DUPLICATE KEY UPDATE version=%s, status=%s"""
                cursor.execute(query, recordTuple)
                connection.commit()
                i += 7
            print("Record inserted successfully into wpversion table")

        except mysql.connector.Error as error:
            print("Failed to insert into MySQL table {}".format(error))
        finally :
            if (connection.is_connected()):
                    cursor.close()
                    connection.close()
                    print("MySQL connection closed")

def read_DB():
    data = []
    try :
        connection = mysql.connector.connect(host='', database='wp_version', user='python', password='')
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM wpversion")
            data = cursor.fetchall()
            return data
    except mysql.connector.Error as error:
        print("Failed to connect to database")
