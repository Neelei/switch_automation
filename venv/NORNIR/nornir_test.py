#!/usr/bin/env python

# Filename:                     nornir-tutorial.py
# Command to run the program:   python nornir-tutorial.py

# Import dependencies
from nornir import InitNornir

import json

# Pretty print a python dictionary
def prettyPrintDictionary(dict):
  print(json.dumps(dict, indent=2))

# Initialize Nornir
nr = InitNornir(config_file="config.yaml")