#!/usr/bin/env python

import sys

import simplejson
import yaml

data=simplejson.load(sys.stdin)
print yaml.dump(data,default_flow_style=False)
