import random, math, csv, json
R=lambda x: round(x,2)

def zig(upper, lower, touches):
    """touches: list of (t, 'U'|'L') -> waypoints on the given lines"""
    return [(t, upper(t) if k=='U' else lower(t)) for t,k in touches]
def line(t0,p0,t1,p1): return lambda t: p0+(p1-p0)*(t-t0)/(t1-t0)

P=[]  # (name, signal, type, waypoints, guides, gaps, desc, mirror_of)
def add(name,sig,typ,wp,guides,desc,gaps=(),curve=None):
    P.append(dict(name=name,signal=sig,type=typ,wp=wp,guides=guides,gaps=list(gaps),desc=desc,curve=curve))

# ---------- Head and shoulders ----------
hs=[(0,82),(10,96),(15,90),(22,106),(28,90),(34,97),(40,88),(47,81)]
add("Head and Shoulders","bearish","Reversal",hs,[[(8,90),(42,90)]],
 "Three peaks after an uptrend, with the middle peak (the head) higher than the two shoulders on either side. A break below the neckline joining the two troughs signals a bearish reversal. The usual price target is the height from head to neckline, projected down from the break.")
# ---------- Double / triple ----------
dt=[(0,82),(12,100),(19,91),(27,100),(34,89),(41,82)]
add("Double Top","bearish","Reversal",dt,[[(10,100),(29,100)],[(12,91),(37,91)]],
 "Two peaks at about the same price after an uptrend, separated by a trough. Buyers fail twice at the same resistance. The pattern confirms when price closes below the trough between the peaks. Also known as an M pattern.")
tt=[(0,82),(10,100),(15,92),(21,100),(26,92),(32,100),(38,90),(45,83)]
add("Triple Top","bearish","Reversal",tt,[[(8,100),(34,100)],[(13,92),(40,92)]],
 "Three peaks at about the same price after an uptrend. Resistance holds three times, and a close below the support line through the troughs confirms a bearish reversal.")
# ---------- Rounding ----------
def rb_curve(t):
    if t<=6: return 104-3*t
    if t<=46: return 80+6*((t-26)/20)**2*3.1/3.1*3.2  # 80 at bottom, ~99 at rims
    return None
rb=[(0,106),(6,100)]+[(t,round(80+19.5*((t-26)/20)**2,2)) for t in range(8,46,2)]+[(46,99.5),(50,101),(56,108)]
add("Rounding Bottom","bullish","Reversal",rb,[[(6,100),(50,100)]],
 "A long, gradual U-shaped turn from a downtrend to an uptrend, as selling slowly fades and buying slowly builds. A move above the level where the decline began confirms it. Also known as a Saucer Bottom.")
# ---------- Cup and handle ----------
cup=[(0,86),(6,100)]+[(t,round(100-15*math.sin(math.pi*(t-6)/30),2)) for t in range(8,36,2)]+[(36,100),(39,97.5),(41,98.5),(43,96.5),(46,101),(54,110)]
add("Cup and Handle","bullish","Continuation",cup,[[(6,100),(47,100)]],
 "A rounded, U-shaped cup followed by a short, shallow pullback called the handle, both below a resistance level. A breakout above the rim continues the prior uptrend. Popularised by William O'Neil.")
# ---------- Wedges ----------
U=line(0,95,36,103); L=line(0,85,36,101)
rw=zig(U,L,[(0,'L'),(5,'U'),(10,'L'),(15,'U'),(20,'L'),(25,'U'),(29,'L'),(33,'U')])+[(36,99),(44,88)]
add("Rising Wedge","bearish","Reversal",rw,[[(0,95),(36,103)],[(0,85),(36,101)]],
 "Price rises between two upward-sloping lines that converge, with the lower line rising faster. Each new high gains less ground, and a break below the lower line usually leads to a drop. Can appear as a reversal at the top of an uptrend or as a bearish continuation within a downtrend.")
# ---------- Triangles ----------
U=lambda t:100; L=line(0,86,36,99)
at=[(0,80)]+zig(U,L,[(4,'U'),(9,'L'),(14,'U'),(19,'L'),(24,'U'),(28,'L'),(32,'U'),(34,'L')])+[(38,103),(46,110)]
add("Ascending Triangle","bullish","Continuation",at,[[(2,100),(38,100)],[(2,87),(36,99.5)]],
 "A flat resistance line on top and a rising support line underneath. Buyers make higher lows while sellers hold one price, and a breakout above resistance usually continues the uptrend.")
U=line(0,106,40,98); L=line(0,84,40,96)
st=[(0,95)]+zig(U,L,[(3,'U'),(8,'L'),(13,'U'),(18,'L'),(23,'U'),(28,'L'),(32,'U'),(36,'L'),(39,'U')])
add("Symmetrical Triangle","neutral","Bilateral",st,[[(2,105.6),(42,97.6)],[(2,84.6),(42,96.6)]],
 "Lower highs and higher lows squeeze price into a narrowing triangle with no side in control. Price can break out either way, so traders wait for the break. It more often continues the trend that came before it. Also known as a Coil.")
# ---------- Flags / pennants ----------
fU=line(9,105,29,100.5); fL=line(9,100,29,95.5)
bf=[(0,84),(4,87),(9,105)]+zig(fU,fL,[(12,'L'),(15,'U'),(19,'L'),(22,'U'),(26,'L'),(29,'U')])+[(31,103),(38,118)]
bf[-3]=(29,fU(29))
add("Bull Flag","bullish","Continuation",bf,[[(9,105),(31,100)],[(11,100),(31,95)]],
 "A sharp rally (the flagpole) followed by a short, orderly pullback inside a small downward-sloping channel (the flag). A breakout above the flag usually continues the rally by about the length of the pole.")
pU=line(9,105,30,100); pL=line(9,96,30,99.5)
bp=[(0,84),(4,87),(9,105)]+zig(pU,pL,[(12,'L'),(15,'U'),(19,'L'),(22,'U'),(25,'L'),(27,'U'),(29,'L')])+[(32,104),(39,117)]
add("Bull Pennant","bullish","Continuation",bp,[[(9,105),(31,99.8)],[(11,96.3),(31,99.7)]],
 "A sharp rally followed by a brief pause in a small symmetrical triangle (the pennant). A breakout above the pennant usually continues the rally.")
# ---------- Rectangle ----------
U=lambda t:100; L=lambda t:92
br=[(0,82),(6,100)]+zig(U,L,[(11,'L'),(16,'U'),(21,'L'),(26,'U'),(31,'L'),(36,'U'),(40,'L')])+[(44,103),(51,110)]
br[2]=br[2]
add("Bullish Rectangle","bullish","Continuation",br,[[(5,100),(45,100)],[(9,92),(42,92)]],
 "In an uptrend, price pauses and trades sideways between flat support and resistance. A breakout above the top of the range continues the uptrend. Also known as a Trading Range or Consolidation.")
# ---------- Channels ----------
U=line(0,93,48,111); L=line(0,85,48,103)
ac=zig(U,L,[(0,'L'),(5,'U'),(10,'L'),(15,'U'),(20,'L'),(25,'U'),(30,'L'),(35,'U'),(40,'L'),(45,'U'),(48,'L')])
add("Ascending Channel","bullish","Continuation",ac,[[(0,93),(48,111)],[(0,85),(48,103)]],
 "Price moves higher between two parallel, upward-sloping lines. Higher highs and higher lows define the uptrend, with the lower line acting as support. Also known as a Rising Channel or Up Channel.")
U=lambda t:100; L=lambda t:92
hc=zig(U,L,[(0,'L'),(7,'U'),(14,'L'),(21,'U'),(28,'L'),(35,'U'),(42,'L'),(49,'U'),(54,'L')])
hc=[(0,96)]+hc[1:]
add("Horizontal Channel","neutral","Bilateral",hc,[[(0,100),(54,100)],[(0,92),(54,92)]],
 "Price moves sideways between flat support and resistance with no trend. Traders often buy near support and sell near resistance until a breakout picks a direction. Also known as a Sideways Channel or Range.")
# ---------- Broadening ----------
U=line(0,98,44,107); L=line(0,94,44,84)
bfm=[(0,96)]+zig(U,L,[(3,'U'),(8,'L'),(14,'U'),(20,'L'),(27,'U'),(34,'L'),(41,'U')])+[(46,97)]
add("Broadening Formation","neutral","Bilateral",bfm,[[(0,98),(44,107)],[(0,94),(44,84)]],
 "Swings grow wider over time, making higher highs and lower lows between two diverging lines. It reflects rising volatility and disagreement, and price can break out either way. Also known as a Megaphone Pattern.")
U=line(0,94,40,110); L=line(0,90,40,98)
abw=zig(U,L,[(0,'L'),(4,'U'),(10,'L'),(16,'U'),(23,'L'),(31,'U'),(38,'L')])[:-1]+[(38,97),(46,88)]
abw=zig(U,L,[(0,'L'),(4,'U'),(10,'L'),(16,'U'),(23,'L'),(31,'U'),(37,'L')])+[(40,95),(47,87)]
add("Ascending Broadening Wedge","bearish","Reversal",abw,[[(0,94),(40,110)],[(0,90),(40,98)]],
 "Price climbs between two upward-sloping lines that spread apart, so the swings get wider as it rises. The widening swings show an unstable advance, and a break below the lower line usually leads to a decline.")
# ---------- Diamond ----------
dm=[(0,82),(6,97),(10,94.3),(15,99.7),(20,90.7),(26,103),(31,91.9),(36,99.5),(40,93.8),(44,96.8),(47,95),(55,84)]
add("Diamond Top","bearish","Reversal",dm,[[(6,97),(26,103),(44,96.8)],[(10,94.3),(20,90.7),(40,93.8)]],
 "After an uptrend, swings first widen and then narrow, tracing a diamond shape. A break below the lower right edge signals a bearish reversal. It is rare, and it can look like a head and shoulders with a V-shaped neckline.")
# ---------- V ----------
vt=[(0,80),(4,83),(8,86),(12,91),(16,96),(20,101),(24,96),(28,91),(32,86),(36,83),(40,80)]
add("V-Top","bearish","Reversal",vt,[],
 "A sharp rally followed immediately by an equally sharp decline, with no pause or pattern at the top. Often driven by news or exhaustion, it is hard to trade because it gives little warning. Also known as a Spike Top or Inverted V.")
# ---------- Island reversal ----------
it=[(0,84),(14,96),(15,100.5),(17,102),(19,101),(21,102.5),(22,97),(24,95),(32,86)]
add("Island Reversal Top","bearish","Reversal",it,[[(13,98.3),(24,98.3)]],
 "After an uptrend, price gaps up, trades for a few sessions, then gaps down, leaving the cluster isolated like an island between two gaps. It signals a sharp bearish reversal.",gaps=[15,22])
# ---------- Bump and run ----------
bar=[(0,85),(8,87.7),(13,89.3),(17,93),(21,98),(25,103),(27,104),(30,101),(33,97.8),(36,97.2),(40,94),(47,87)]
add("Bump and Run Reversal Top","bearish","Reversal",bar,[[(0,84.6),(42,98)]],
 "A gentle uptrend (the lead-in) is followed by a steep, speculative rally (the bump), which then falls back through the original trendline (the run). A break of the lead-in trendline signals a bearish reversal. Developed by Thomas Bulkowski.")
# ---------- Measured move ----------
mm=[(0,85),(4,88),(14,100),(18,96),(22,94),(26,98),(36,109)]
add("Measured Move Up","bullish","Continuation",mm,[],
 "A rally, a pullback, then a second rally of roughly the same size as the first. The first leg is used to project the target for the second. Also known as an ABC move or Swing Measurement.")
# ---------- Dead cat ----------
dcb=[(0,100),(6,99),(9,95),(12,83),(15,85),(19,90),(22,89),(25,85),(32,76)]
add("Dead Cat Bounce","bearish","Continuation",dcb,[],
 "After a steep drop, price bounces briefly before resuming its decline to new lows. The bounce is a relief rally, not a reversal. The name comes from the saying that even a dead cat bounces if it falls far enough.")
# ---------- Harmonics ----------
abcd=[(0,106),(3,104),(10,92),(17,100),(27,87),(34,95)]
add("Bullish ABCD","bullish","Reversal",abcd,[[(0,106),(10,92),(17,100),(27,87)]],
 "Price falls from A to B, retraces part of the move to C, then falls from C to D by about the same distance as A to B. The completion at D marks a likely bullish reversal. The simplest harmonic pattern, also known as AB=CD.")
gart=[(0,85),(10,105),(16,92.6),(22,100),(32,89.3),(40,98)]
add("Bullish Gartley","bullish","Reversal",gart,[[(0,85),(10,105),(16,92.6),(22,100),(32,89.3)],[(0,85),(16,92.6)],[(16,92.6),(32,89.3)]],
 "A five-point harmonic pattern, X-A-B-C-D, where B retraces 61.8% of XA and D completes at the 78.6% retracement of XA. The D point is a potential buying zone. Named after H.M. Gartley, also known as the 222 pattern.")

# mirrors
def mirror(p,name,desc,sig):
    prices=[w[1] for w in p['wp']]; C=(min(prices)+max(prices))/2
    m=dict(p); m['name']=name; m['desc']=desc; m['signal']=sig
    m['wp']=[(t,R(2*C-v)) for t,v in p['wp']]
    m['guides']=[[(t,R(2*C-v)) for t,v in g] for g in p['guides']]
    return m
by={p['name']:p for p in P}
MIR=[
("Head and Shoulders","Inverse Head and Shoulders","bullish","Three troughs after a downtrend, with the middle trough (the head) lower than the two shoulders on either side. A break above the neckline joining the two peaks signals a bullish reversal. Also known as a Head and Shoulders Bottom."),
("Double Top","Double Bottom","bullish","Two troughs at about the same price after a downtrend, separated by a peak. Sellers fail twice at the same support. The pattern confirms when price closes above the peak between the troughs. Also known as a W pattern."),
("Triple Top","Triple Bottom","bullish","Three troughs at about the same price after a downtrend. Support holds three times, and a close above the resistance line through the peaks confirms a bullish reversal."),
("Rounding Bottom","Rounding Top","bearish","A long, gradual dome-shaped turn from an uptrend to a downtrend, as buying slowly fades and selling slowly builds. A move below the level where the advance began confirms it. Also known as an Inverted Saucer."),
("Cup and Handle","Inverse Cup and Handle","bearish","An upside-down cup followed by a short bounce (the handle), both above a support level. A breakdown below the support continues the prior downtrend. Also known as an Inverted Cup and Handle."),
("Rising Wedge","Falling Wedge","bullish","Price falls between two downward-sloping lines that converge, with the upper line falling faster. Each new low loses less ground, and a break above the upper line usually leads to a rally. Can appear as a reversal at the bottom of a downtrend or as a bullish continuation within an uptrend."),
("Ascending Triangle","Descending Triangle","bearish","A flat support line underneath and a falling resistance line on top. Sellers make lower highs while buyers defend one price, and a breakdown below support usually continues the downtrend."),
("Bull Flag","Bear Flag","bearish","A sharp decline (the flagpole) followed by a short, orderly bounce inside a small upward-sloping channel (the flag). A break below the flag usually continues the decline by about the length of the pole."),
("Bull Pennant","Bear Pennant","bearish","A sharp decline followed by a brief pause in a small symmetrical triangle (the pennant). A break below the pennant usually continues the decline."),
("Bullish Rectangle","Bearish Rectangle","bearish","In a downtrend, price pauses and trades sideways between flat support and resistance. A breakdown below the bottom of the range continues the downtrend. Also known as a Trading Range or Consolidation."),
("Ascending Channel","Descending Channel","bearish","Price moves lower between two parallel, downward-sloping lines. Lower highs and lower lows define the downtrend, with the upper line acting as resistance. Also known as a Falling Channel or Down Channel."),
("Ascending Broadening Wedge","Descending Broadening Wedge","bullish","Price falls between two downward-sloping lines that spread apart, so the swings get wider as it drops. Selling is losing control, and a break above the upper line usually leads to a rally."),
("Diamond Top","Diamond Bottom","bullish","After a downtrend, swings first widen and then narrow, tracing a diamond shape. A break above the upper right edge signals a bullish reversal. It is rare, and it can look like an inverse head and shoulders."),
("V-Top","V-Bottom","bullish","A sharp decline followed immediately by an equally sharp rally, with no basing period at the bottom. Often driven by news or capitulation. Also known as a Spike Bottom or V-Reversal."),
("Island Reversal Top","Island Reversal Bottom","bullish","After a downtrend, price gaps down, trades for a few sessions, then gaps up, leaving the cluster isolated like an island between two gaps. It signals a sharp bullish reversal.",),
("Bump and Run Reversal Top","Bump and Run Reversal Bottom","bullish","A gentle downtrend is followed by a steep, panicky drop (the bump), which then recovers back through the original trendline (the run). A break above the lead-in trendline signals a bullish reversal. Developed by Thomas Bulkowski."),
("Measured Move Up","Measured Move Down","bearish","A decline, a bounce, then a second decline of roughly the same size as the first. The first leg is used to project the target for the second. Also known as an ABC move down."),
("Bullish ABCD","Bearish ABCD","bearish","Price rises from A to B, pulls back part of the move to C, then rises from C to D by about the same distance as A to B. The completion at D marks a likely bearish reversal. Also known as AB=CD."),
("Bullish Gartley","Bearish Gartley","bearish","The mirror image of the bullish Gartley: X-A-B-C-D where B retraces 61.8% of XA and D completes at the 78.6% retracement of XA, near a potential selling zone. Also known as the 222 pattern."),
]
for base,name,sig,desc in MIR: P.append(mirror(by[base],name,desc,sig))

# ---------- build candles ----------
def build(p,seed):
    rnd=random.Random(seed)
    wp=sorted(p['wp']); n=wp[-1][0]+1
    path=[0]*n
    for (t0,p0),(t1,p1) in zip(wp,wp[1:]):
        for t in range(t0,t1+1): path[t]=p0+(p1-p0)*(t-t0)/(t1-t0) if t1>t0 else p1
    kind={}
    for k,(t,v) in enumerate(wp):
        if 0<k<len(wp)-1:
            a,b=wp[k-1][1],wp[k+1][1]
            if v>a and v>b: kind[t]='peak'
            elif v<a and v<b: kind[t]='trough'
    rng=max(path)-min(path); amp=rng*0.018; wick=rng*0.022
    out=[]; prev=None
    for t in range(n):
        target=path[t]
        c=target+rnd.gauss(0,amp)
        o=path[t-1]+rnd.gauss(0,amp*0.5) if prev is None else prev['c']
        if t in p['gaps']: o=target+rnd.gauss(0,amp*0.5)
        if prev is None: o=target-(path[1]-path[0])+rnd.gauss(0,amp*0.5)
        k=kind.get(t)
        if k=='peak':
            c=target-abs(rnd.gauss(0,amp))-amp*0.8; h=target; l=min(o,c)-abs(rnd.gauss(0,wick))
        elif k=='trough':
            c=target+abs(rnd.gauss(0,amp))+amp*0.8; l=target; h=max(o,c)+abs(rnd.gauss(0,wick))
        else:
            h=max(o,c)+abs(rnd.gauss(0,wick)); l=min(o,c)-abs(rnd.gauss(0,wick))
        h=max(h,o,c); l=min(l,o,c)
        cd=dict(o=o,h=h,l=l,c=c)
        # keep gaps clean
        if t in p['gaps'] and prev:
            if o>prev['h']: cd['l']=max(min(o,c)-0.2, prev['h']+0.4) if min(o,c)>prev['h']+0.4 else cd['l']
            if cd['l']<=prev['h'] and o>prev['c']:
                cd['o']=max(o,prev['h']+1.0); cd['c']=max(c,prev['h']+0.8); cd['l']=prev['h']+0.5; cd['h']=max(cd['h'],cd['o'],cd['c'])
            if o<prev['l'] or o<prev['c']:
                cd['o']=min(cd['o'],prev['l']-1.0); cd['c']=min(cd['c'],prev['l']-0.8); cd['h']=prev['l']-0.5; cd['l']=min(cd['l'],cd['o'],cd['c'])
        out.append(cd); prev=cd
    return out

rows=[]
for i,p in enumerate(P):
    cs=build(p,1000+i)
    for c in cs: assert c['h']>=max(c['o'],c['c'])-1e-9 and c['l']<=min(c['o'],c['c'])+1e-9, p['name']
    for g in p['gaps']:
        a,b=cs[g-1],cs[g]
        assert b['l']>a['h'] or b['h']<a['l'], (p['name'],g,a,b)
    candles=" | ".join(",".join(f"{R(c[k]):g}" for k in "ohlc") for c in cs)
    n=len(cs)-1
    def clip(g):
        out=[]
        for (t0,v0),(t1,v1) in zip(g,g[1:]):
            a,b=max(t0,0),min(t1,n)
            if b<=a: continue
            f=lambda t:v0+(v1-v0)*(t-t0)/(t1-t0)
            seg=[(a,f(a)),(b,f(b))]
            if out and out[-1][0]==seg[0][0]: seg=seg[1:]
            out+=seg
        return out
    gl=[clip(g) for g in p['guides']]; gl=[g for g in gl if len(g)>=2]
    guides=" | ".join(";".join(f"{R(t):g}:{R(v):g}" for t,v in g) for g in gl)
    rows.append([p['name'],p['signal'],p['type'],candles,guides,p['desc']])
order={"Reversal":0,"Continuation":1,"Bilateral":2}
with open('../data/trend-patterns.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['pattern','signal','type','candles','guides','description']); w.writerows(rows)
print(len(rows),"patterns"); print(sorted(set(len(r[3].split('|')) for r in rows)))
