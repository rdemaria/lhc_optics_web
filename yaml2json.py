#!/usr/bin/env python

import sys

import simplejson
import yaml

data=yaml.load(sys.stdin)
print simplejson.dumps(data,indent=True)
