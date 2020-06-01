#!/bin/python

import check_last_version
import os.path
from os import path

global version_inst
global path
global ref
pathwp=[]

check_last_version.untar_version_file()
ref = check_last_version.checkversion_ref()
#	print(ref)
pathwp = check_last_version.find()
	#print(pathwp)
version_inst = check_last_version.checkversion_list(pathwp)
check_last_version.compare_ref_w_list(version_inst,ref)
check_last_version.find_instances_name(version_inst)
#print(version_inst)
check_last_version.initialize_db()
check_last_version.add_value_2_db(version_inst)
check_last_version.read_DB()
