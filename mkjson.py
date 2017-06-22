import yaml
import simplejson

data=yaml.load(open('data.yaml'))
simplejson.dump(data,open('data.json','w'),sort_keys=True,indent=True)


