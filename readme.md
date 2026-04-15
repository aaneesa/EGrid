PR
JECT 15
O
INTELLIGENT EV CHARGING
DEMAND PREDICTI
N
O
& AGENTIC INFRASTRUCTURE
PLANNING
From Usage A
naly
t
ics t
o
A
ut
onomo
us Grid & S
tat
ion Planning
PR
JECT
VERVIEW
O
O
This projec
t
(EV) infrastru
foc
uses on b
u
c
ture planning.
ilding an
AI-driven analy
t
ics syst
em for elec
tric vehicle
In Milest
one 1, classical machine learning
t
echniqu
charging demand
using hist
orical charging stat
ion
es are
used
t
o predic
t EV
usage, t
ime, and l
ocat
ion data.
In Milest
one 2, t
he syst
em evo
lves in
t
o an agen
t
ic
AI assistan
t t
hat reasons abo
charging demand patt
erns, re
trieves infrastru
c
ture planning g
u
idelines, and
generat
es stru
c
tured recommendat
ions.
ut
Th e p r oj ec
t a dd r es s es a r e al -worl d su st a in a bil i
t
y p r obl em a nd d em onst r at
es a p pl i ed
m achin e l e a r ning , a g en
t
ic
AI d es ign, a nd s yst
em d epl
oym en
t .
C
O
NSTRAINTS & REQUIREMENTS
TEAM SIZE
3–4 S
tu
FRAMEW
den
ts
RK
O
LangGraph (Recommended)
API BUDGET
Free Tier
O
nly
H
O
STING
Mandat
ory
APPR
O
VED TECHN
L
GY STACK
O
O
LLMS (MILEST
O
NE 2)
O
pen-so
urce models
Free-t
ier APIs
AGENT FRAMEW
RK
O
LangGraph (Recommended)
Chroma / FAISS (RAG)
ML & ANALYTICS (MILEST
O
NE 1)
t
Sciki
-Learn (Pipelines)
Regression/Classificat
ion
Feature Engineering
UI FRAMEW
RK
O
S
treamli
t (Recommended)
Gradio
H
O
STING PLATF
O
Hu
gging Face Spaces
S
treamli
t Commu
t
ni
y Cl
o
Render (Free Tier)
RM (MANDAT
O
RY)
u
d
WARNING: Localhost
-only demonstrat
ions will no
t
be accept
ed.
MILEST
O
PREDICTI
O
NE 1: ML-B
N
ASED EV CHARGING DEMAND
MID-SEM SUBMISSI
O
N
t
O
bjec
ive: Predic
t EV charging demand at stat
ions using hist
orical usage data.
Foc
us on cleaning real-world data and b
u
ilding rob
ust predic
t
ive models
w i
t
ho
ut L L M s .
Fu
t
nc
ional Requ
iremen
ts:
ccept
charging session and l
ocat
ion data.
Perform data preprocessing and feature engineering.
Predic
t
charging demand (Regression/Classificat
ion).
Display demand
usage
trends via user in
t
erface.
A
TECHNICAL REQUIREMENTS (ML)
Preprocessing: Time-series features, Cleaning.■
ory.■
Features: Locat
ion, Time of Day, Usage hist
ing.■
Models: Random Forest, Gradien
t
Boost
Evaluat
ion: MAE, RMSE, R-Squared.■
INPUTS & O
UTPUTS
Input: Charging session CSV data.■
ion.■
O
utput: Demand Predic
t
nalysis.■
Me
trics: Trend A
MID-SEM DELIVERA
BLES
■
Problem u
descript
ion.
nderstanding & Domain
Syst
t
ture diagram.■
em archi
ec
Input
ion.■
–o
utput specificat
t
ion wi
h UI.■
Working l
ocal applicat
ion report.■
Model evaluat
MILEST
O
PLANNING
NE 2: AGENTIC EV INFRASTRUCTURE
END-SEM SUBMISSI
O
N
t
O
bjec
ive: Evo
lves in
t
o an agen
t
ic
AI assistan
t t
hat reasons abo
ut
charging
demand patt
erns and generat
es opt
imized infrastru
c
ture and sched
uling
recommendat
ions.
Fu
t
nc
ional Requ
iremen
ts:
nalyze demand for high-l
oad l
ocat
ions.
Re
trieve infrastru
c
ture planning g
u
idelines.
Generat
e opt
imal charger placemen
t recommendat
ions.
Display sched
uling opt
imizat
ion insigh
ts.
A
TECHNICAL REQUIREMENTS (AGENTIC)
e).■
Framework: LangGraph (Workfl
ow & S
tat
idelines (Chroma/FAISS).■
RAG: Planning Gu
t.■
S
tat
e: Explici
t stat
e managemen
Logic:
pt
ion reasoning.■
O
imizat
STRUCTURED
O
UTPUT
ummary.■
A
nalysis: Charging Demand S
ion ID.■Locat
e: High-l
oad Locat
Plan: Infrastru
c
ture Expansion Recs.■
pt
ts.■
O
imize: Sched
uling Insigh
ing References.■
Refs: S
upport
END-SEM DELIVERA
BLES
■
u
ion.■
P
blicly host
ed applicat
ion.■
Agen
t workfl
ow doc
umen
tat
Re
trieval-au
l
ogic.
gmen
t
ed planning
■
■
Gi
tHu
Doc
umen
t
b Reposi
ory &
tat
ion.
Demo Video (Syst
em
Walkt
hro
u
gh).
Final
Art
ifac
ts: Host
ed Link, Gi
tHu
b Repo, Demo Video.
EVALUATI
O
N CRITERIA
PHASE WEIGHT CRITERIA
Mid-Sem
(Milest
one 1)
25%
Correc
t ML pipeline & Demand Predic
t
ion
t
Q
uali
y of Data Preprocessing & Evaluat
ion
t
UI Usabili
y & Domain Understanding
End-Sem
(Milest
one 2)
30%
t
Q
uali
y of Agen
t Reasoning & Planning
Re
trieval In
t
egrat
ion (RAG) & S
tat
e
Depl
oymen
t
u
t
S
ccess & Video Clari
y