import numpy as np
import pylsa
lsa = pylsa.LSAClient()

## Positive polarity spectrometer

tmp="""\
    squeeze{bsmm}:
      label: Squeeze ({bsm} m)
      shortdesc: LHC squeeze optics ({bsm} m, 10 m, {bsm} m, {bs8m} m) for {nrj} GeV after {st} s from the beginning of the ramp.
      settings:
        beam1: [p, {nrj}, 1.2e11, 2556, 2.5e-06]
        beam2: [p, {nrj}, 1.2e11, 2556, 2.5e-06]
        exp: ['off','on','off','on']
      madx_strengths:
      - call, file="db5/opticsfile.{optn}";
      madx_knobs:
      - NRJ = {nrj};
      - on_sep1={sep1};on_x1={x1};on_a1=0;on_o1=0;on_oh1=0;on_ov1=0;
      - on_sep5={sep5};on_x5={x5};on_a5=0;on_o5=0;on_oh5=0;on_ov5=0;
      - on_sep2={sep2};on_x2={x2};on_a2={a2};on_o2=0;on_oh2=0;on_ov2=0;on_oe2=0;
      - on_sep8={sep8};on_x8={x8};on_a8={a8};on_o8=0;on_oh8=0;on_ov8=0;on_oe8=0;
      - on_alice:=-7000/NRJ;on_lhcb:=-7000/NRJ;
      - dQx.b1=0; dQy.b1=0; dQx.b2=0; dQy.b2=0;
      - dQx.b1_sq=0; dQy.b1_sq=0; dQx.b2_sq=0; dQy.b2_sq=0;
      - dQpx.b1=0; dQpy.b1=0; dQpx.b2=0; dQpy.b2=0;
      - dQpx.b1_sq=0; dQpy.b1_sq=0; dQpx.b2_sq=0; dQpy.b2_sq=0;
      - KOD.A56B1:=KOD.B1*4.65/6.0;
      - KOF.B1={ko}; KOD.B1={ko}; KOF.B2={ko}; KOD.B2={ko};
      template: med_template"""

params="""\
LHCBEAM/MOMENTUM
LHCBEAM/IP1-XING-V-MURAD
LHCBEAM/IP2-XING-V-MURAD
LHCBEAM/IP5-XING-H-MURAD
LHCBEAM/IP8-XING-H-MURAD
LHCBEAM/IP1-SEP-H-MM
LHCBEAM/IP2-SEP-H-MM
LHCBEAM/IP5-SEP-V-MM
LHCBEAM/IP8-SEP-V-MM
LHCBEAM/IP2-ANGLE-H-MURAD
LHCBEAM/IP8-ANGLE-V-MURAD
LHCBEAM1/LANDAU_DAMPING_RUN2
LHCBEAM2/LANDAU DAMPING
LHCBEAM1/QPH
LHCBEAM1/QPV
LHCBEAM2/QPH
LHCBEAM2/QPV""".split('\n')


bp='RAMP-SQUEEZE-6.5TeV-ATS-1m-2017_V3_V1'
pv=lsa.interpOpticsParameters(bp,params)
ot=lsa.getOpticTable(bp)

for nnn,opt in enumerate(ot):
  if opt.time>=365:
    data={}
    if opt.name[8:11]=='11m':
      data['bsmm']=11000
      data['bs8m']=10
    else:
      data['bsmm']=int(opt.name[8:11])*10
      data['bs8m']=int(opt.name[-3:])/100.
    data['bsm'] ="%.1f"%(data['bsmm']/1000.)
    data['nrj'] = "%d"%(pv['LHCBEAM/MOMENTUM'][nnn])
    data['st'] = opt.time
    data['optn'] = nnn-11
    for irn,p1,p2 in zip('1258','VVHH','HHVV'):
      data['x%s'%irn]=pv['LHCBEAM/IP%s-XING-%s-MURAD'%(irn,p1)][nnn]
      data['sep%s'%irn]=pv['LHCBEAM/IP%s-SEP-%s-MM'%(irn,p2)][nnn]
      if irn in '28':
        data['a%s'%irn]=pv['LHCBEAM/IP%s-ANGLE-%s-MURAD'%(irn,p2)][nnn]
    data['o5']=0
    data['o2']=0
    data['ko']=pv['LHCBEAM2/LANDAU DAMPING'][nnn]*-6
    print tmp.format(**data)


:bp='SQUEEZE-6.5TeV-ATS-1m-40cm-2017_V1'
ot = lsa.getOpticTable(bp)
tvalue=[opt.time for opt in ot]

params="""\
LHCBEAM/MOMENTUM
LHCBEAM/IP1-XING-V-MURAD
LHCBEAM/IP2-XING-V-MURAD
LHCBEAM/IP5-XING-H-MURAD
LHCBEAM/IP8-XING-H-MURAD
LHCBEAM/IP1-SEP-H-MM
LHCBEAM/IP2-SEP-H-MM
LHCBEAM/IP5-SEP-V-MM
LHCBEAM/IP8-SEP-V-MM
LHCBEAM/IP2-OFFSET-V-2MM
LHCBEAM/IP2-OFFSET-V-MM
LHCBEAM/IP5-OFFSET-V-MM
LHCBEAM/IP5-OFFSET_V-MM
""".split()

