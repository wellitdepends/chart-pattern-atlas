import numpy as np, pickle, datetime
exec(open('select_examples.py').read().split("res={}")[0].split("used=[]")[0])
res=pickle.load(open('res.pkl','rb'))
def fit(p,A,L):
    t=resample(tpath(p),L); c=(A[:,2]+A[:,3]+A[:,4])/3
    a,b=np.polyfit(t,c,1); return a,b

def snap_guides(p,A,L,n,a,b):
    path=tpath(p); wp=sorted(p['wp']); sc=(L-1)/(n-1); rad=max(2,int(round(L*0.06)))
    H,Lo=A[:,2],A[:,3]
    kind={}
    for k,(t,v) in enumerate(wp):
        if 0<k<len(wp)-1:
            if v>wp[k-1][1] and v>wp[k+1][1]: kind[t]='hi'
            elif v<wp[k-1][1] and v<wp[k+1][1]: kind[t]='lo'
    def snap(t,side):
        i=int(round(t*sc)); lo,hi=max(0,i-rad),min(L,i+rad+1)
        if side=='hi': j=lo+int(np.argmax(H[lo:hi])); return (j,H[j])
        j=lo+int(np.argmin(Lo[lo:hi])); return (j,Lo[j])
    out=[]
    has_poly=any(len(g)>2 for g in p['guides'])
    for g in p['guides']:
        if has_poly and len(g)==2 and 'Diamond' not in p['name']: continue
        if len(g)>2:  # polyline through pivots (harmonics)
            out.append([snap(t,kind.get(int(round(t)),'hi' if v>=path[min(int(round(t)),n-1)] else 'lo')) for t,v in g]); continue
        (t0,v0),(t1,v1)=g
        line=lambda t:v0+(v1-v0)*(t-t0)/(t1-t0)
        touches=[(t,kind[t]) for t,v in wp if t in kind and t0-1<=t<=t1+1 and abs(v-line(t))<0.8]
        if len(touches)>=2:
            pts=[snap(t,sd) for t,sd in touches]
            xs=np.array([q[0] for q in pts],float); ys=np.array([q[1] for q in pts])
            if len(set(xs))>=2:
                m,c=np.polyfit(xs,ys,1)
                if abs(v1-v0)<1e-9: m,c=0.0,float(np.median(ys))
                x0,x1=t0*sc,t1*sc; out.append([(x0,m*x0+c),(x1,m*x1+c)]); continue
        out.append([(t*sc,a*v+b) for t,v in g])
    return out
EX={}
for pi,p in enumerate(P):
    sc,sym,k,L,s,m=res[pi]; A=A_(sym,k)[s:s+L]
    n=len(tpath(p)); a,b=fit(p,A,L)
    guides=snap_guides(p,A,L,n,a,b)
    EX[pi]=dict(sym=sym,k=k,A=A,guides=guides,score=sc,method=m)
pickle.dump(EX,open('ex.pkl','wb'))
if __name__=='__main__':
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    fig,axs=plt.subplots(7,6,figsize=(24,22))
    for ax,(pi,e) in zip(axs.flat,EX.items()):
        for i,(t,o,h,l,c) in enumerate(e['A']):
            col='#0C8C7A' if c>=o else '#CF4636'
            ax.plot([i,i],[l,h],color=col,lw=.8); ax.add_patch(plt.Rectangle((i-.35,min(o,c)),.7,max(abs(c-o),1e-9),color=col))
        for g in e['guides']: ax.plot([q[0] for q in g],[q[1] for q in g],'--',color='#2F55C4',lw=1)
        ax.set_title(f"{P[pi]['name']} | {e['sym'].split(':')[1]} {e['k']}D",fontsize=10); ax.set_xticks([]); ax.autoscale()
    plt.tight_layout(); plt.savefig('grid.png',dpi=55)
