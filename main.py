import json,os,urllib.request as u
E=os.environ["MAKEFUN_ENV_URL"]
V=(0,100,320,330,500,900,0)
N=(-33,-31,-18,-14,14,18,31,33)
D=(-17,-15,15,17,-16,-1,1,16)
R={4:3,0:2,7:1,116:12,112:8,119:4}
O=20000
n=0
def P(f):
 b=[0]*128;s=1;c=0;e=-1;t=(f.split()+["-"]*4)[:4]
 for r,w in enumerate(t[0].split("/")):
  x=0
  for h in w:
   if h.isdigit():x+=int(h)
   else:q="pnbrqk".index(h.lower())+1;b[(7-r)*16+x]=q if h.isupper() else -q;x+=1
 s=1 if t[1]=="w" else -1
 c=sum((k in t[2])<<j for j,k in enumerate("KQkq"))
 if t[3]!="-":e=(int(t[3][1])-1)*16+ord(t[3][0])-97
 return b,s,c,e
def A(b,q,s):
 for o,v in(((-15*s,-17*s),1),(N,2),(D,6)):
  for d in o:
   t=q+d
   if not t&136 and b[t]==v*s:return 1
 for d in D:
  t=q+d
  while not t&136:
   p=b[t]
   if p:
    if p*s>0 and(abs(p)==5 or abs(p)==3+(abs(d) in(1,16))):return 1
    break
   t+=d
 return 0
def K(b,s):return next((i for i in range(128) if not i&136 and b[i]==6*s),-1)
def M(b,s,c,e):
 m=[]
 for i in range(128):
  if i&136:continue
  p=b[i]
  if not p or p*s<0:continue
  a=abs(p);r=i>>4;f=i&7
  if a==1:
   d=16*s;z=r==6 if s>0 else r==1;t=i+d
   if not t&136 and not b[t]:
    m+=([(i,t,q) for q in(5,4,3,2)] if z else [(i,t,0)])
    if((s>0 and r==1)or(s<0 and r==6)) and b[i+2*d]==0:m.append((i,i+2*d,0))
   for t in(i+d-1,i+d+1):
    if t&136:continue
    if b[t]*s<0 or t==e:m+=([(i,t,q) for q in(5,4,3,2)] if z else [(i,t,0)])
  elif a in(2,6):
   for d in(N if a==2 else D):
    t=i+d
    if t&136:continue
    if not b[t] or b[t]*s<0:m.append((i,t,0))
   if a==6:
    for kf,kt,rf,bt in((4,6,7,1),(4,2,0,2),(116,118,119,4),(116,114,112,8)):
     if i==kf and c&bt and b[rf]==4*s and all(not b[x] for x in range(min(kf,rf)+1,max(kf,rf))) and all(not A(b,x,-s)for x in(kf,(kf+kt)//2,kt)):m.append((kf,kt,0))
  else:
   for d in(D[:4] if a==3 else D[4:] if a==4 else D):
    t=i+d
    while not t&136 and not b[t]:m.append((i,t,0));t+=d
    if not t&136 and b[t]*s<0:m.append((i,t,0))
 return m
def T(b,x,s,c,e):
 q=b[:];f,t,z=x;p=q[f];q[f]=0
 if abs(p)==6 and abs(t-f)==2:
  r=t+1 if t>f else t-2;w=t-1 if t>f else t+1;q[w],q[r]=q[r],0
 if z:q[t]=z if p>0 else -z
 else:
  if abs(p)==1 and not q[t] and(f&7)!=(t&7):q[t-16*s]=0
  q[t]=p
 k=c&~R.get(f,0)&~R.get(t,0)
 return q,-s,k,f+16*s if abs(p)==1 and abs(t-f)>16 else -1
def L(b,s):
 y=0
 for i in range(128):
  if i&136:continue
  p=b[i]
  if not p:continue
  a=abs(p);r=i>>4;f=i&7;w=r if p>0 else 7-r;g=min(f,7-f)+min(w,7-w)
  v=V[a]+(0,6*w+8*(2<f<5),7*g,5*g,2*g+12*(w==6),3*g,(10 if w<=1 else -12*w)+6*(1<f<6))[a]
  y+=v if p>0 else -v
 return y*s
def Q(b,s,c,e,a,l,q):
 global n
 n+=1
 if n>O or q<1:return L(b,s)
 t=L(b,s)
 if t>=l:return l
 if t>a:a=t
 for x in M(b,s,c,e):
  if not b[x[1]] and not x[2]:continue
  w,y,z,v=T(b,x,s,c,e)
  if A(w,K(w,s),-s):continue
  u=-Q(w,y,z,v,-l,-a,q-1)
  if u>=l:return l
  if u>a:a=u
 return a
def S(b,s,c,e,d,a,l):
 global n
 if d<=0:return Q(b,s,c,e,a,l,6)
 n+=1
 if n>O:return L(b,s)
 m=M(b,s,c,e)
 m.sort(key=lambda x:abs(b[x[1]])*10-abs(b[x[0]])+900*x[2],reverse=1)
 h=-999999;g=0
 for x in m:
  w,y,z,v=T(b,x,s,c,e)
  if A(w,K(w,s),-s):continue
  g+=1
  u=-S(w,y,z,v,d-1,-l,-a)
  if u>h:h=u
  if u>a:a=u
  if a>=l:break
 if g==0:return -100000 if A(b,K(b,s),-s) else 0
 return h
U=lambda x:chr(97+(x[0]&7))+str((x[0]>>4)+1)+chr(97+(x[1]&7))+str((x[1]>>4)+1)+("qrbn"[5-x[2]] if x[2] else "")
def C(fen,legal):
 global n
 b,s,c,e=P(fen);n=0;m=[]
 for x in M(b,s,c,e):
  if U(x) not in legal:continue
  w,y,z,v=T(b,x,s,c,e)
  if not A(w,K(w,s),-s):m.append(x)
 if not m:return legal[0]
 z=m[0]
 for d in range(1,6):
  if n>O:break
  a=-999999;o=None;u=-999999
  for x in sorted(m,key=lambda x:x!=z):
   if n>O:break
   w,y,j,v=T(b,x,s,c,e)
   t=-S(w,y,j,v,d-1,-999999,-a)
   if t>u:u,o=t,x
   if t>a:a=t
  if n>O or not o:break
  z=o
 return U(z)
def J(p,o):return json.load(u.urlopen(u.Request(E+p,json.dumps(o).encode(),{"content-type":"application/json"})))
while True:
 g=J("/game",{})
 if g["status"]=="done":break
 while g["status"]=="your_move":
  g=J("/move",{"game":g["game"],"move":C(g["fen"],g["legal_moves"])})
