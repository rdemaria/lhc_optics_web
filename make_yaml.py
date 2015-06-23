sql="""\
opt_11000_10000_11000_10000.madx
opt_9000_10000_9000_9000.madx
opt_7000_10000_7000_8000.madx
opt_4000_10000_4000_7000.madx
opt_3000_10000_3000_6000.madx
opt_2500_10000_2500_5000.madx
opt_2000_10000_2000_4000.madx
opt_1500_10000_1500_3500.madx
opt_1200_10000_1200_3250.madx
opt_1000_10000_1000_3000.madx
opt_900_10000_900_3000.madx
opt_800_10000_800_3000.madx
opt_800_10000_800_3000_coll.madx
opt_700_10000_700_3000.madx
opt_650_10000_650_3000.madx
opt_600_10000_600_3000.madx
opt_600_10000_600_3000_coll.madx
opt_550_10000_550_3000.madx
opt_500_10000_500_3000.madx
opt_450_10000_450_3000.madx
opt_400_10000_400_3000.madx
opt_400_10000_400_3000_coll.madx"""


squeeze=('squeeze{bet5mm}',"""\
    squeeze{bet5mm}:
      label: Squeeze ({bet5m})
      shortdesc: LHC squeeze optics ({bet1m}, {bet2m}, {bet5m}, {bet8m}) for 6.5 TeV.
      madx_strengths:
      - call, file="db5/opt_{bet1}_{bet2}_{bet5}_{bet8}.madx";
      template: med_template""")

coll=('coll{bet5mm}',"""\
    coll{bet5mm}:
      label: Collision ({bet5m})
      shortdesc: LHC collision optics ({bet1m}, {bet2m}, {bet5m}, {bet8m}) for 6.5 TeV.
      madx_strengths:
      - call, file="db5/opt_{bet1}_{bet2}_{bet5}_{bet8}_coll.madx";
      template: med_template""")

out=[]
for ll in sql.split('\n'):
    ll=ll.replace('.madx','_')
    op,bet1,bet2,bet5,bet8,rest=ll.split('_',5)
    data={'bet1':bet1, 'bet2': bet2, 'bet5': bet5, 'bet8': bet8}
    data['bet5mm']=int(bet5)
    for bb in '1258':
      data['bet%sm'%bb]='%gm'%(int(data['bet%s'%bb])/1000.)
    if rest=='coll_':
        lbl,tmp= coll
    else:
        lbl,tmp= squeeze
    print tmp.format(**data)
    out.append(lbl.format(**data))

for l in out:
    print "  - %s" %l

vdml="""\
opt_12600_12500_12600_12500.madx
opt_14500_14500_14500_14500.madx
opt_16700_17000_16700_17000.madx
opt_19200_19000_19200_19000.madx
opt_19200_19000_19200_21000.madx
opt_19200_19000_19200_24000.madx
opt_19200_19000_19200_24000_coll.madx"""

vdm=('vdm{bet8mm}',"""\
    vdm{bet8mm}:
      label: Collision ({bet8m})
      madx_strengths:
      - call, file="db5/opt_{bet1}_{bet2}_{bet5}_{bet8}.madx";
      shortdesc: LHC VDM optics ({bet1m}, {bet2m}, {bet5m}, {bet8m}) for 6.5 TeV.
      template: med_template""")

vdmcoll=('vdm{bet8mm}',"""\
    vdm{bet8mm}:
      label: Collision ({bet8m})
      madx_strengths:
      - call, file="db5/opt_{bet1}_{bet2}_{bet5}_{bet8}.madx";
      shortdesc: LHC VDM in collision optics ({bet1m}, {bet2m}, {bet5m}, {bet8m}) for 6.5 TeV.
      template: med_template""")

out=[]
for ll in vdml.split('\n'):
    ll=ll.replace('.madx','_')
    op,bet1,bet2,bet5,bet8,rest=ll.split('_',5)
    data={'bet1':bet1, 'bet2': bet2, 'bet5': bet5, 'bet8': bet8}
    data['bet8mm']=int(bet8)
    for bb in '1258':
      data['bet%sm'%bb]='%gm'%(int(data['bet%s'%bb])/1000.)
    if 'coll' in rest:
        lbl,tmp= vdmcoll
    else:
        lbl,tmp= vdm
    print tmp.format(**data)
    out.append(lbl.format(**data))

for l in out:
    print "  - %s" %l


hbl="""\
opt_12600_10000_12600_10000_hibeta.madx
opt_14500_10000_14500_10000_hibeta.madx
opt_16700_10000_16700_10000_hibeta.madx
opt_19200_10000_19200_10000_hibeta.madx
opt_22000_10000_22000_10000_hibeta.madx
opt_25000_10000_25000_10000_hibeta.madx
opt_30000_10000_30000_10000_hibeta.madx
opt_33000_10000_33000_10000_hibeta.madx
opt_36000_10000_36000_10000_hibeta.madx
opt_40000_10000_40000_10000_hibeta.madx
opt_43000_10000_43000_10000_hibeta.madx
opt_46000_10000_46000_10000_hibeta.madx
opt_51000_10000_51000_10000_hibeta.madx
opt_54000_10000_54000_10000_hibeta.madx
opt_60000_10000_60000_10000_hibeta.madx
opt_67000_10000_67000_10000_hibeta.madx
opt_75000_10000_75000_10000_hibeta.madx
opt_90000_10000_90000_10000_hibeta.madx
opt_90000_10000_90000_10000_hibeta_coll.madx"""

hb=('hb{bet5mm}',"""\
    hb{bet5mm}:
      label: Hibeta ({bet5m})
      madx_strengths:
      - call, file="db5/opt_{bet1}_{bet2}_{bet5}_{bet8}_hibeta.madx";
      shortdesc: LHC High Beta optics ({bet1m}, {bet2m}, {bet5m}, {bet8m}) for 6.5 TeV.
      template: med_template""")

hbcoll=('hb{bet5mm}_coll',"""\
    hb{bet5mm}_coll:
      label: Hibeta Coll ({bet5m})
      madx_strengths:
      - call, file="db5/opt_{bet1}_{bet2}_{bet5}_{bet8}_hibeta_coll.madx";
      shortdesc: LHC High Beta in collision optics ({bet1m}, {bet2m}, {bet5m}, {bet8m}) for 6.5 TeV.
      template: med_template""")

out=[]
for ll in hbl.split('\n'):
    op,bet1,bet2,bet5,bet8,rest=ll.split('_',5)
    data={'bet1':bet1, 'bet2': bet2, 'bet5': bet5, 'bet8': bet8}
    data['bet5mm']=int(bet5)
    for bb in '1258':
      data['bet%sm'%bb]='%gm'%(int(data['bet%s'%bb])/1000.)
    if 'coll' in rest:
        lbl,tmp= hbcoll
    else:
        lbl,tmp= hb
    print tmp.format(**data)
    out.append(lbl.format(**data))

for l in out:
    print "  - %s" %l
