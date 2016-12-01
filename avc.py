#!/usr/bin/env python

import sys
import argparse
import os.path
import glob
import yaml

var_dirs = [ "vars", "defaults" ]
var_files = []
ansible_vars = []
template_vars = []
task_vars = []

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--role", help="Specify role to check against", dest='role_dir')
parser.add_argument("-g", "--group_vars", help="Specify group_vars to check against", nargs="*", dest='group_vars')
parser.add_argument("--version", help="Print version", action="version", version="%(prog)s 0.1.0-alpha")
args = parser.parse_args()

role = args.role_dir
groups = args.group_vars

for group in groups:
    var_files.append(group)

def roles_vars_files(role_dir):
    """ Find all role variable files to check against"""
    for dirpath, dirname, filenames in os.walk(role):
        for filename in [f for f in filenames if f.endswith(".yaml") or f.endswith(".yml")]:
            for x in var_dirs:
                if x in dirpath:
                    var_files.append(os.path.join(dirpath, filename))
    return var_files

def get_vars(var_files):
    """ Check group variable files """
    for fn in var_files:
        with open(fn) as stream:
            yaml_vars = yaml.load(stream)
            for k,v in yaml_vars.items():
                ansible_vars.append(k)
    return ansible_vars

if __name__ == '__main__':
    file_list = roles_vars_files(role)
    a_vars = get_vars(var_files)
    print file_list
    print a_vars

