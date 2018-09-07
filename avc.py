#!/usr/bin/env python

import argparse
import os.path
import yaml
import re

regex = re.compile(r"\{\{.*\}\}")
var_dirs = ["vars", "defaults"]
conf_files = []
conf_vars = []
template_files = []
template_vars = []
task_files = []
task_vars = []
missing_vars = []

parser = argparse.ArgumentParser()
parser.add_argument("-r", "--role", help="Specify role to check against", dest='role_dir') # noqa E501
parser.add_argument("-g", "--group_vars", help="Specify group_vars to check against", nargs="*", dest='group_vars') # noqa E501
parser.add_argument("--version", help="Print version", action="version", version="%(prog)s 0.1.0-alpha") # noqa E501
args = parser.parse_args()

role = args.role_dir
groups = args.group_vars

if groups:
    for group in groups:
        conf_files.append(group)


def get_vars_files(role_dir):
    """ Function to grab all the files we will need """
    for dirpath, dirnames, filenames in os.walk(role):
        for filename in [f for f in filenames if f.endswith(".yaml") or f.endswith(".yml")]: # noqa E501
            for x in var_dirs:
                if x in dirpath:
                    conf_files.append(os.path.join(dirpath, filename))
            if "tasks" in dirpath:
                task_files.append(os.path.join(dirpath, filename))
        for filename in [f for f in filenames if f.endswith(".j2")]:
            if "templates" in dirpath:
                template_files.append(os.path.join(dirpath, filename))

    return conf_files, task_files, template_files


def get_task_vars(task_files):
    """ Grab all variables from task files """
    for f in task_files:
        with open(f) as task:
            for line in task:
                match = re.search(regex, line)
                if match and "item" not in match.group():
                    v = match.group()[3:-3]
                    if v not in task_vars and "lookup" not in v:
                        task_vars.append(v)
    return task_vars


def get_template_vars(template_files):
    """ Grab all variables from template files """
    for f in template_files:
        with open(f) as template:
            for line in template:
                match = re.search(regex, line)
                if match and "item" not in match.group():
                    v = match.group()[3:-3]
                    if v not in template_vars and "lookup" not in v:
                        template_vars.append(v)
    return template_vars


def get_conf_vars(conf_files):
    """ Check group variable files """
    for fn in conf_files:
        with open(fn) as stream:
            yaml_vars = yaml.safe_load(stream)
            if yaml_vars:
                for k, v in yaml_vars.items():
                    conf_vars.append(k)
    return conf_vars


def compare_vars(conf_vars, t_vars):
    """ Checks to see if you have any missing variables """
    c_t = list(set(conf_vars) - set(t_vars))
    for v in c_t:
        if "ansible" not in v:
            missing_vars.append(v)
    t_c = list(set(t_vars) - set(conf_vars))
    for v in t_c:
        if "ansible" not in v:
            missing_vars.append(v)


if __name__ == '__main__':
    c_files, ta_files, te_files = get_vars_files(role)
    conf_vars = get_conf_vars(c_files)
    if not conf_vars:
        print "There are no configuration variables to test against"
        exit(1)
    ta_vars = get_task_vars(ta_files)
    te_vars = get_template_vars(te_files)
    t_vars = ta_vars + te_vars

    if t_vars:
        compare_vars(conf_vars, t_vars)

    if missing_vars:
        print "Variables missing matches:"
        for v in missing_vars:
            if "." not in v:
                print v
    else:
        print "All your variables are accounted for"
