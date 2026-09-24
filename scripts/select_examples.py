import numpy as np, pickle, json, datetime, math
exec(open('scan_matches.py').read().split("T=[tpath(p)")[0])  # defs + P + D
T=[tpath(p) for p in P]
cands=pickle.load(open('cands.pkl','rb'))
AG={}
def A_(sym,k):
    if (sym,k) not in AG: AG[(sym,k)]=agg(D[sym],k)
    return AG[(sym,k)]
used=[]; uses={}
def span(sym,k,L,s):
    A=A_(sym,k); return A[s,0],A[min(s+L,len(A))-1,0]
def overlaps(sym,a,b):
    for (s2,a2,b2) in used:
        if s2==sym and min(b,b2)-max(a,a2)>0.3*min(b-a,b2-a2): return True
    return False
def gapped(A,i,up):
    return A[i,3]>A[i-1,2] if up else A[i,2]<A[i-1,3]
res={}
# islands first: rule-based on daily bars
def find_island(top):
    best=None
    for sym,bars in D.items():
        A=A_(sym,1)
        for i in range(20,len(A)-20):
            if not gapped(A,i,top): continue
            for j in range(i+2,min(i+10,len(A)-15)):
                if gapped(A,j,not top):
                    # island must stay above/below both gap edges
                    seg=A[i:j]
                    if top and seg[:,3].min()<=max(A[i-1,2],A[j,2]): continue
                    if (not top) and seg[:,2].max()>=min(A[i-1,3],A[j,3]): continue
                    pre=(A[i-1,4]-A[i-16,4])/A[i-16,4]; post=(A[j+10,4]-A[j,4])/A[j,4]
                    sc=(pre-post) if top else (post-pre)
                    if best is None or sc>best[0]: best=(sc,sym,1,(j+12)-(i-16),i-16)
                    break
    return best
order=sorted(range(len(P)),key=lambda i:-max(c[0] for c in cands[i]))
for pi in order:
    p=P[pi]
    if p['name'].startswith('Island Reversal'):
        b=find_island('Top' in p['name']); sc,sym,k,L,s=b; res[pi]=(0.0,sym,k,L,s,'rule')
        a,bb=span(sym,k,L,s); used.append((sym,a,bb)); uses[sym]=uses.get(sym,0)+1; continue
    cs=sorted(cands[pi],key=lambda c:-(c[0]-0.012*uses.get(c[1],0)))
    for c in cs:
        sc,sym,k,L,s=c
        a,b=span(sym,k,L,s)
        if overlaps(sym,a,b): continue
        res[pi]=(sc,sym,k,L,s,'corr'); used.append((sym,a,b)); uses[sym]=uses.get(sym,0)+1; break
pickle.dump(res,open('res.pkl','wb'))
for pi in range(len(P)):
    sc,sym,k,L,s,m=res[pi]; a,b=span(sym,k,L,s)
    f=lambda t:datetime.datetime.utcfromtimestamp(t).strftime('%Y-%m-%d')
    print(f"{P[pi]['name'][:30]:30} {sc:.3f} {sym:18} {k}D L={L:3} {f(a)}→{f(b)} {m}")
