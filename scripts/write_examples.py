import pickle, csv, datetime, numpy as np
exec(open('fit_guides.py').read().split("if __name__")[0])
P_names=[p['name'] for p in P]
rows=list(csv.reader(open('../data/trend-patterns.csv')))
hdr=rows[0][:6]; rows=[r[:6] for r in rows[1:]]
hdr+=['example_symbol','example_interval','example_dates','example_candles','example_guides','example_match']
def fmt(v,dec): return f"{round(float(v),dec):.{dec}f}".rstrip('0').rstrip('.')
out=[]
for r in rows:
    pi=P_names.index(r[0]); e=EX[pi]; A=e['A']; L=len(A)
    px=float(np.median(A[:,4])); dec=5 if px<2 else 4 if px<20 else 2
    dates=",".join(datetime.datetime.utcfromtimestamp(t).strftime('%Y-%m-%d') for t in A[:,0])
    candles=" | ".join(",".join(fmt(v,dec) for v in row[1:5]) for row in A)
    gl=[]
    for g in e['guides']:
        pts=[]
        for (t0,v0),(t1,v1) in zip(g,g[1:]):
            for t,v in ((t0,v0),(t1,v1)):
                ti=min(max(int(round(t)),0),L-1)
                vv=v0+(v1-v0)*((ti-t0)/(t1-t0)) if t1!=t0 else v
                if not pts or pts[-1][0]!=ti: pts.append((ti,vv))
                elif pts[-1][0]==ti: pts[-1]=(ti,vv)
        pts=sorted(dict(pts).items())
        if len(pts)>=2: gl.append(";".join(f"{t}:{fmt(v,dec)}" for t,v in pts))
    interval={1:"Daily",2:"2-day",3:"3-day",5:"5-day"}[e['k']]
    match="" if e['method']=='rule' else str(int(round(e['score']*100)))
    out.append(r+[e['sym'],interval,dates,candles," | ".join(gl),match])
with open('../data/trend-patterns.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(hdr); w.writerows(out)
print(len(out))
