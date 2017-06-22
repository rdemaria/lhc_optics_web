import yaml
import copy

data=yaml.load(open('datanew.yaml'))

scname='opt2015'
scn=copy.deepcopy(data[scname])
data[scname+'thin']=scn

for confname in scn['conf_list']:
    conf=scn['confs'][confname]
    st=[ll.replace('.madx','_thin.madx') for ll in conf['madx_strengths']]
    conf['madx_strengths']=st

ln='call,file="db5/toolkit/slice.madx";'
scn['confs']['med_template']['madx_sequence'].append(ln)
scn['confs']['med_template']['madx_aperture']=[]
data['scenario_list'].append(scname+'thin')

data['opt2015thin']['confs']['inj']
data['opt2015thin']['confs']['med_template']
data['opt2015']['confs']['med_template']


yaml.dump(data,open('datathin.yaml','w'))

lst=scn['conf_list']

basedir='/afs/cern.ch/work/l/lhcopt/public/lhc_optics_web/www/opt2015'

for  confname in scn['conf_list']:
    t=optics.open("%s/%s/twiss_lhcb1.tfs"%(basedir,confname))
    th=optics.open("%sthin/%s/twiss_lhcb1.tfs"%(basedir,confname))
    print confname
    idx=t//'BPM'; idxh=th//'BPM'
    for vn in 'betx bety'.split():
      res=abs(1-th[vn][idxh]/t[vn][idx]).max()
      if res>2.3e-3:
          print res,t[vn],th[vn]
    for vn in 'x y'.split():
      res=abs(th[vn][idxh]-t[vn][idx]).max()
      if res>2.1e-6:
          print res,t[vn],th[vn]




