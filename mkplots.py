#!/afs/cern.ch/work/r/rdemaria/public/anaconda/bin/python
import os,sys

import matplotlib.pyplot as pl
import matplotlib
import numpy as np

from pyoptics import *

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
          ref=10.6
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


if __name__=='__main__':
  basedir='result'
  selection=['LHC', 'IR1', 'Arc12', 'IR2', 'Arc23', 'IR3', 'Arc34',
                    'IR4', 'Arc45', 'IR5', 'Arc56', 'IR6', 'Arc67',
                    'IR7', 'Arc78', 'IR8', 'Arc81']
  force=True
  for sel in selection:
     for b12 in '12':
        tfsname="result/twiss_%sb%s.tfs"%(sel.lower(),b12)
        plot_beta(tfsname)
        plot_aperture(tfsname)
        plot_orbit(tfsname)
        tfs_to_csv(tfsname)
        if sel.lower()!='lhc':
          apname="result/ap_%sb%s.tfs"%(sel.lower(),b12)
          tfs_to_csv(apname)
