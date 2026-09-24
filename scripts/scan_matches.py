import numpy as np, pickle, json, sys, math
from numpy.lib.stride_tricks import sliding_window_view as swv
sys.path.insert(0,'.')
import importlib.util
spec=importlib.util.spec_from_file_location('gen','generate_trend_patterns.py'); gen=importlib.util.module_from_spec(spec); spec.loader.exec_module(gen)
P=gen.P
D=pickle.load(open('data.pkl','rb'))

def tpath(p):
    wp=sorted(p['wp']); n=wp[-1][0]+1; path=np.zeros(n)
    for (t0,p0),(t1,p1) in zip(wp,wp[1:]):
        for t in range(t0,t1+1): path[t]=p0+(p1-p0)*(t-t0)/(t1-t0)
    return path
def resample(x,L):
    return np.interp(np.linspace(0,len(x)-1,L),np.arange(len(x)),x)
def z(a,axis=-1):
    m=a.mean(axis=axis,keepdims=True); s=a.std(axis=axis,keepdims=True)+1e-12; return (a-m)/s

def agg(bars,k):
    out=[]
    for i in range(0,len(bars)-k+1,k):
        g=bars[i:i+k]; out.append((g[0]['t'],g[0]['o'],max(b['h'] for b in g),min(b['l'] for b in g),g[-1]['c']))
    return np.array(out)

T=[tpath(p) for p in P]
cands=[[] for _ in P]
for sym,bars in D.items():
    for k in (1,2,3,5):
        A=agg(bars,k)
        if len(A)<100: continue
        H,Lo,C=A[:,2],A[:,3],A[:,4]
        lens=sorted({int(round(len(t)*f)) for t in T for f in (0.75,1.0,1.3)})
        for L in lens:
            if L<25 or L>80 or L>=len(A): continue
            WC=z(swv(C,L)); WH=z(swv(H,L)); WL=z(swv(Lo,L))
            for pi,t in enumerate(T):
                n=len(t)
                if not (0.7*n<=L<=1.35*n): continue
                tz=z(resample(t,L))
                sc=(WC@tz+WH@tz+WL@tz)/(3*L)
                # keep top few per (sym,k,L)
                idx=np.argpartition(-sc,5)[:5]
                for s in idx: cands[pi].append((float(sc[s]),sym,k,L,int(s)))
pickle.dump(cands,open('cands.pkl','wb'))
print('done',[len(c) for c in cands][:5])
