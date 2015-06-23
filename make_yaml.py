sq="""\
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
      madx_strengths:
      - call, file="db5/opt_{bet1}_{bet2}_{bet5}_{bet8}.madx";
      shortdesc: LHC squeeze optics ({bet1m}, {bet2m}, {bet5m}, {bet8m}) for 6.5 TeV.
      template: med_template""")

coll=('coll{bet5mm}',"""\
    coll{bet5mm}:
      label: Collision ({bet5m})
      madx_strengths:
      - call, file="db5/opt_{bet1}_{bet2}_{bet5}_{bet8}_coll.madx";
      shortdesc: LHC collision optics ({bet1m}, {bet2m}, {bet5m}, {bet8m}) for 6.5 TeV.
      template: med_template""")

out=[]
for ll in sq.split('\n'):
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

