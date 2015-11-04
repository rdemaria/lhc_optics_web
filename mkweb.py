import os
import time
import copy

import jinja2
import yaml
import json
import matplotlib.pyplot as pl
import matplotlib
import numpy as np

from pyoptics import *


class Scenarios(list):
  def __init__(self,data):
    for name in data['scenario_list']:
      scen=Scenario(name,**data[name])
      self.append(scen)
      setattr(self,name,scen)

class Scenario(object):
  beam_data=['p','E','N<sub>b</sub>','k<sub>b</sub>','&epsilon;']
  beam_data_unit_tmp=['','GeV','10<sup>%d</sup>','','&mu;rad']
  ip_data=['&beta;<sub>x</sub>', '&beta;<sub>y</sub>',
           'x', 'y',
           'p<sub>x</sub>', 'p<sub>y</sub>']
  ip_data_unit=['m','m','mm', 'mm', '&mu;rad', '&mu;rad']
  ip_names=['ip1','ip2','ip5','ip8']
  def __init__(self,name,**data):
    self.name=name
    self.__dict__.update(data)
    self.beam_data_unit=Scenario.beam_data_unit_tmp[:]
    self.beam_data_unit[2]=self.beam_data_unit_tmp[2]%(self.npart_unit)
    for cname,cdata in self.confs.items():
      Configuration._instances[(name,cname)]=cdata
    for cname,cdata in self.confs.items():
      self.confs[cname]=Configuration(name=cname,scenario=name,scn=self,**cdata)
      setattr(self,cname, self.confs[cname])


class Configuration(object):
  selection=['LHC', 'IR1', 'Arc12', 'IR2', 'Arc23', 'IR3', 'Arc34',
                    'IR4', 'Arc45', 'IR5', 'Arc56', 'IR6', 'Arc67',
                    'IR7', 'Arc78', 'IR8', 'Arc81']
  _instances={}
  pdata={'p'  :(0.931494061,1), #GeV,charge
         'Pb' : (193.68715,82)}  #GeV,charge
  def __init__(self,**data):
    scenario=data['scenario']
    if 'template' in data:
      tname=(scenario,data['template'])
      tmp=self._instances[tname].copy()
      self.__dict__.update(copy.deepcopy(tmp))
    self.__dict__.update(data)
    if hasattr(self,'settings'):
      part1,self.nrj1,self.np1,self.nb1,self.emit_n1=self.settings['beam1']
      part2,self.nrj2,self.np2,self.nb2,self.emit_n2=self.settings['beam2']
      if part1=='p':
        self.part1='proton'
      else:
        self.part1='ion'
      if part2=='p':
        self.part2='proton'
      else:
        self.part2='ion'
      self.pmass1,self.charge1=self.pdata[part1]
      self.pmass2,self.charge2=self.pdata[part2]
      self.emit1=self.emit_n1/self.nrj1*self.pmass1
      self.emit2=self.emit_n2/self.nrj2*self.pmass2
      self.np1_web=float(self.np1)/10**self.scn.npart_unit
      self.np2_web=float(self.np2)/10**self.scn.npart_unit
      self.emit_n1_web=self.emit_n1*1e6
      self.emit_n2_web=self.emit_n2*1e6
  def get_conf_dir(self):
    return os.path.join(basedir,self.scenario,self.name)
  def get_twiss_fn(self,beam):
    return os.path.join(self.get_conf_dir(),"twiss_lhcb%s.tfs"%beam)
  def get_twiss(self,beam):
    return optics.open(self.get_twiss_fn(beam))
  def get_data(self):
    for b12 in '12':
      t=optics.open(self.get_twiss_fn(b12))
      for nn,ipn in enumerate([1,2,5,8]):
        print get_ip_data(t,ipn)
        #exp=self.settings['exp'][nn]
        #self.settings['ip%sb%s'%(ipn,b12)]=get_ip_data(t,ipn)+[exp]
        self.settings['ip%sb%s'%(ipn,b12)]=get_ip_data(t,ipn)
    return self


def is_uptodate(targets,depends):
  if force:
    return False
  for fn in depends:
    if not os.path.exists(fn):
      raise IOError, "%s does not exists"%fn
  for fn in targets:
    if not os.path.exists(fn):
      return False
  ttar=min([os.path.getmtime(fn) for fn in targets])
  tdep=max([os.path.getmtime(fn) for fn in depends])
  return tdep<ttar


def execute_madx(path,scnname,run=False):
  fullname=os.path.join(*path)
  basedir,fname=os.path.split(fullname)
  if not os.path.isdir(basedir):
    print "mkdir",basedir
    os.mkdir(basedir)
  name,ext=os.path.splitext(fname)
  outname="%s.out"%name
  fulloutname=os.path.join(basedir,outname)
  madx_cmd='/afs/cern.ch/user/m/mad/bin/rel/last-dev/madx-linux64'
  #madx_cmd='/home/rdemaria/work/madx/madX/build/madx64'
  if not is_uptodate([fulloutname],[fullname]):
    if run=='local':
      cmd='(cd %s; %s <%s >%s)'%(basedir,madx_cmd,fname,outname)
      print cmd
      os.system(cmd)
    elif run=='lsf':
      subname='/afs/cern.ch/work/l/lhcopt/work/bsub_%s_%s'%(scnname,name)
      fh=open(subname,'a+')
      cmd='bsub -o %s -e %s -q 8nh madx %s\n'%(fulloutname,fulloutname,fullname);
      fh.write(cmd)
      fh.close()
      print "Execute %s"%subname



def renderfile(dirnames,name,template,data):
  basedir=''
  for dirname in dirnames:
    basedir=os.path.join(basedir,dirname)
    if not os.path.isdir(basedir):
      print "mkdir",basedir
      os.mkdir(basedir)
  fullname=os.path.join(basedir,name)
  print "write", fullname
  open(fullname,'w').write(template.render(**data))



def tfs_to_csv(tfsname):
  name,ext=os.path.splitext(tfsname)
  figname=name+'.csv'
  try:
    if not is_uptodate([figname],[tfsname]):
      print tfsname
      t=tfsdata.open(tfsname)
      tfsdata.dump_csv(t,open(figname,'w'))
      print figname,"done"
  except IOError:
    print figname,"skipped"
    pass


def plot_beta(tfsname):
  basedir,fname=os.path.split(tfsname)
  name,ext=os.path.splitext(fname)
  figname=os.path.join(basedir,name+'.png')
  selname=os.path.split(name)[1].split('_')[1]
  try:
    if not is_uptodate([figname],[tfsname]):
      pl.clf()
      t=optics.open(tfsname)
      t.s-=t.s[0]
      p=t.plotbeta(newfig=False)
      pl.title('Twiss %s'%selname.upper())
      pl.savefig(figname)
      print figname,"done"
  except IOError:
    print figname,"skipped"
    pass

def plot_aperture(tfsname):
  aptfsname=tfsname.replace('twiss','ap')
  basedir,fname=os.path.split(tfsname)
  name,ext=os.path.splitext(fname)
  apname=name.replace('twiss','ap')
  figname=os.path.join(basedir,apname+'.png')
  selname=os.path.split(name)[1].split('_')[1]
  try:
    if not is_uptodate([figname],[tfsname,aptfsname]):
      pl.clf()
      t=optics.open(tfsname)
      t.s-=t.s[0]
      if t.param['energy']>450:
          ref=12
      else:
          ref=9
      p=t.plotap(newfig=False,nlim=30,ref=ref)
      pl.title('Aperture %s'%selname.upper())
      pl.savefig(figname)
      print figname,"done"
  except IOError:
    print figname,"skipped"
    pass

def plot_orbit(tfsname):
  basedir,fname=os.path.split(tfsname)
  name,ext=os.path.splitext(fname)
  figname=os.path.join(basedir,name.replace('twiss','orbit')+'.png')
  selname=name.split('_')[1]
  try:
    if not is_uptodate([figname],[tfsname]):
      pl.clf()
      t=optics.open(tfsname)
      t.s-=t.s[0]
      p=t.plot('x y',newfig=False)
      pl.title('Orbit %s'%selname.upper())
      pl.savefig(figname)
      print figname,"done"
  except IOError:
    print figname,"skipped"
    pass



templateLoader = jinja2.FileSystemLoader( searchpath="." )
templateEnv = jinja2.Environment( loader=templateLoader )

tmain = templateEnv.get_template("main.template")
tscen = templateEnv.get_template("scenario.template")
tmadx = templateEnv.get_template("job.madx")
taper = templateEnv.get_template("job_aperture.madx")
tmmod = templateEnv.get_template("job_model.madx")
tmmodwin = templateEnv.get_template("job_model_win.madx")
tmseq = templateEnv.get_template("job_mkseq.madx")
tmtwi = templateEnv.get_template("job_mktwiss.madx")
tconf = templateEnv.get_template("configuration.template")
tsele = templateEnv.get_template("selection.template")
ttwip = templateEnv.get_template("twiss_plot.template")
torbp = templateEnv.get_template("orbit_plot.template")

def run_madx(run=False):
  os.system('cp data.json %s'%basedir)
  if run=='lsf':
      os.system('rm /afs/cern.ch/work/l/lhcopt/work/bsub_*')
  for scn in scenarios:
    scndir=os.path.join(basedir,scn.name)
    rdata['scn']=scn
    for cname in scn.conf_list:
      conf= scn.confs[cname]
      rdata['conf']=conf
      respath=[basedir,scn.name,conf.name]
      rdata['resdir']=os.path.join(*respath)
      md="%s_%s"%(scn.name,conf.name)
      for out,template in [('job.madx',taper),('job_model.madx',tmmod),
                           ('job_mkseq.madx',tmseq),
                          # ('lhc_mktwiss.madx',tmtwi)
                          ]:
        renderfile(respath,out,template,rdata)
      confdir=os.path.join(basedir,scn.name,conf.name)
      #execute_madx([confdir,'job.madx'],scn.name,run=run)
      #execute_madx([confdir,'job_model.madx'],scn.name,run=run)
      execute_madx([confdir,'job_mkseq.madx'],scn.name,run=run)
      for part in ['madx_sequence','madx_aperture',
                   'madx_strengths','madx_knobs']:
        pout=[]
        for l in getattr(conf,part):
          ll=l
          for lname,lval in conf.madx_links.items():
            ll=ll.replace(lname,lval)
          #pout.append(ll.replace('/',"\\"))
          pout.append(ll)
        setattr(conf,part+'_win',pout)
      renderfile(respath,'lhc_%s.madx'%md,tmmodwin,rdata)

def run_html():
  renderfile([basedir],'index.html',tmain,rdata)
  for scn in scenarios:
    scndir=os.path.join(basedir,scn.name)
    rdata['scn']=scn
    renderfile([basedir,scn.name],'index.html',tscen,rdata)
    for cname in scn.conf_list:
      conf= scn.confs[cname]
      rdata['conf']=conf
      rdata['resdir']=os.path.join(basedir,scn.name,conf.name)
      print conf.label,conf.settings['ip1b1']
      renderfile([basedir,scn.name,conf.name],'index.html',tconf,rdata)
      for sel in conf.selection:
        rdata['sel']=sel
        for pname in ['twiss','orbit','ap']:
          rdata['pname']=pname
          fname='%s_%s.html'%(pname,sel.lower())
          renderfile([basedir,scn.name,conf.name],fname,ttwip,rdata)


def run_plot():
  for scn in scenarios:
    scndir=os.path.join(basedir,scn.name)
    rdata['scn']=scn
    for cname in scn.conf_list:
      conf= scn.confs[cname]
      rdata['conf']=conf
      rdata['resdir']=os.path.join(basedir,scn.name,conf.name)
      for sel in conf.selection:
        rdata['sel']=sel
        for b12 in '12':
          tfsname="twiss_%sb%s.tfs"%(sel.lower(),b12)
          print scn.name,cname,sel,b12
          tfsfull=os.path.join(basedir,scn.name,conf.name,tfsname)
          print tfsfull
          plot_beta(tfsfull)
          plot_aperture(tfsfull)
          plot_orbit(tfsfull)
          tfs_to_csv(tfsfull)
          if sel.lower()!='lhc':
            apname="ap_%sb%s.tfs"%(sel.lower(),b12)
            apfull=os.path.join(basedir,scn.name,conf.name,apname)
            tfs_to_csv(apfull)



def get_data():
  for scn in scenarios:
    scndir=os.path.join(basedir,scn.name)
    rdata['scn']=scn
    for cname in scn.conf_list:
      conf= scn.confs[cname]
      print 'get_data',scn.name,conf.name
      rdata['conf']=conf
      rdata['resdir']=os.path.join(basedir,scn.name,conf.name)
      ipdata={}
      for b12 in '12':
        fname="twiss_ipb%s_flat.tfs"%b12
        fullname=os.path.join(rdata['resdir'],fname)
        t=optics.open(fullname)
        for ipn in [1,2,5,8]:
          i=np.where(t//('IP%d'%ipn))[0][0]
          ipdata['ip%sb%s'%(ipn,b12)]=[t.betx[i],t.bety[i]]
        fname="twiss_ipb%s.tfs"%b12
        t=optics.open(os.path.join(rdata['resdir'],fname))
        for ipn in [1,2,5,8]:
          i=np.where(t//('IP%d'%ipn))[0][0]
          iporb=[t.x[i]*1e3,t.y[i]*1e3,t.px[i]*1e6,t.py[i]*1e6]
          ipdata['ip%sb%s'%(ipn,b12)].extend(iporb)
          print ipn,iporb
        for nn,ipn in enumerate([1,2,5,8]):
          #print get_ip_data(t,ipn)
          exp=conf.settings['exp'][nn]
          ipd=map(s2d_conv,ipdata['ip%sb%s'%(ipn,b12)])
          #conf.settings['ip%sb%s'%(ipn,b12)]=ipd+[exp]
          conf.settings['ip%sb%s'%(ipn,b12)]=ipd

def get_ip_data(t,n):
  i=np.where(t//('IP%d'%n))[0][0]
  data=(t.betx[i],t.bety[i],t.x[i]*1e3,t.y[i]*1e3,t.px[i]*1e6,t.py[i]*1e6)
  return [s2d_conv(i) for i in data]

def s2d_conv(n):
  if abs(n)>0.999:
    return "%.4g"%n
  elif abs(n)>1e-3:
    return "%.3f"%n
  else:
    return "0"
  #if abs(n)>2e-3:
  #  n=round(n,-int(np.log10(abs(n)))+2)
  #else:
  #  n=0
  #s=('%.3f'%n).replace('.000','')
  #if s=='-0':
  #  s='0'
  #return s

if __name__=='__main__':
  # load web data
  #basedir='/home/rdemaria/work/lhc_optics_web/www'
  #basedir='/afs/cern.ch/user/r/rdemaria/www/www'
  #basedir='/afs/cern.ch/work/r/rdemaria/public/lhc_optics_web/www'
  basedir='/afs/cern.ch/work/l/lhcopt/public/lhc_optics_web/www'
  data=yaml.load(open('datanew.yaml'))
  #data=yaml.load(open('datathin.yaml'))
  json.dump(data,open('data.json','w'),indent=True)
  #data['scenario_list']=['opt2015','opt2015vdm','opt2015hb','opt2015ion']
  data['scenario_list']=['opt2015ion']
  scenarios= Scenarios(data)
  #scenarios.pop(0)
  #scenarios.pop(0)
  #scenarios.pop(0)
  force=False
  rdata={
      'date':time.asctime(),
      'basedir':basedir,
      'scenarios':scenarios}
  #run_madx(run='lsf')
  run_madx(run='local')
  get_data()
  run_html()
  #run_plot()


