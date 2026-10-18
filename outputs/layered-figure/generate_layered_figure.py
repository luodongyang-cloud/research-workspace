"""Editable functional-layer schematic; illustrative states, not experimental data.
Run: python generate_layered_figure.py [output-directory]
Optional rendering: install cairosvg, then rerun to obtain PNG and vector PDF.
"""
from pathlib import Path
import sys, math, random, json, xml.etree.ElementTree as ET
O=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent
O.mkdir(parents=True,exist_ok=True)
S=[]; ns='http://www.w3.org/2000/svg'
S.append('''<svg xmlns="http://www.w3.org/2000/svg" width="183mm" height="122mm" viewBox="0 0 1080 720"><defs><marker id="arrow" markerWidth="7" markerHeight="7" refX="6.3" refY="3.5" orient="auto" markerUnits="strokeWidth"><path d="M0 0 L7 3.5 L0 7 Z" fill="#323a44"/></marker><marker id="light-arrow" markerWidth="7" markerHeight="7" refX="6.3" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7 Z" fill="#ad93d0"/></marker></defs><rect width="1080" height="720" fill="white"/>''')
INK='#26313b';BLUE='#648fbd';PURPLE='#9e83be'
def group(i):S.append(f'<g id="{i}">')
def end():S.append('</g>')
def text(x,y,t,size=12.5,bold=False,anchor='start',color=INK):
 S.append(f'<text x="{x}" y="{y}" font-family="DejaVu Sans, Arial, sans-serif" font-size="{size}" text-anchor="{anchor}" fill="{color}"'+(' font-weight="bold"' if bold else '')+'>'+t+'</text>')
def rect(x,y,w,h,fill='white',stroke='#aeb7c2',r=0):S.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1"/>')
def path(d,color=INK,width=1.3,arrow=False,light=False,opacity=1):
 S.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" opacity="{opacity}"'+(f' marker-end="url(#{"light-arrow" if light else "arrow"})"' if arrow else '')+'/>')
def line(x,y,X,Y,**kw):path(f'M{x} {y} L{X} {Y}',**kw)
def circle(x,y,r,fill='white',stroke=INK):S.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>')
def mathlabel(x,y,parts,size=12.5):
 # parts: (text, shift), explicit dy restores baseline in common SVG renderers.
 curr=0;ss=[]
 for t,shift in parts:
  off=3 if shift=='sub' else -5 if shift=='sup' else 0
  ss.append(f'<tspan dy="{off-curr}" font-size="{10.7 if shift else size}">{t}</tspan>');curr=off
 text(x,y,''.join(ss),size)
def title(num,x,y,label):
 circle(x,y-4,10,'#f3f1f7','#d9d3e4');text(x,y,str(num),12.5,True,'middle');text(x+18,y,label,12.5,True)
def shirt(i,j,n=12):return (2<=j<=4 and 1<=i<=10) or (4<=j<=10 and 3<=i<=8)
def plane_group(i,x,y):
 group(i);S.append(f'<g transform="matrix(1 .12 -.65 .45 {x} {y})">')
def plane_end():end();end()
def frame(x,y,seed,alpha=1):
 plane_group('optical-frame-'+str(seed),x,y)
 S.append(f'<g opacity="{alpha}">');rect(-5,-5,230,130,'#fff','#9da6b1')
 rng=random.Random(seed)
 for j in range(12):
  for i in range(20):
   inside=shirt(int(i*12/20),j);v=(.75 if inside else .08)+rng.uniform(-.43,.43);g=int(251-205*max(0,min(1,v)))
   rect(i*11,j*10,10.9,9.9,f'#{g:02x}{g:02x}{g:02x}','none')
 end();plane_end()
text(26,30,'GaON/GaN 2TG1C1S: optical history and voltage-weighted inference',15,True)
text(25,57,'a',17,True);text(755,57,'b',17,True)
line(732,66,732,663,color='#dce1e7',width=1)
# layer 1
title(1,37,83,'Optical input sequence')
for x,y,seed,alpha in [(211,98,13,.42),(194,109,14,.65),(177,120,15,1)]:frame(x,y,seed,alpha)
line(421,139,459,113,arrow=True);text(467,116,'Time',12.5)
text(466,150,'Repeated signal',12.5);text(466,169,'Changing noise',12.5)
group('incident-optical-paths')
for x in [174,251,330]:line(x,238,x,258,color='#ad93d0',width=2.4,arrow=True,light=True)
end()
# sensor array, functional plane only
title(2,37,224,'Bias-free sensing and temporal processing')
plane_group('sensor-array',177,265);rect(-7,-7,234,134,'#eee8f5','#a998bc')
rng=random.Random(73)
for j in range(6):
 for i in range(10):
  v=(.82 if shirt(int(i*12/10),int(j*12/6)) else .13)+rng.uniform(-.08,.08)
  z=int(248-184*v);rect(i*22,j*20,19,17,f'#{z:02x}{z:02x}{z:02x}','#b8bac0')
# one sensor only, shared by inset
rect(88,60,19,17,'#9e83be','#443452')
plane_end()
text(466,270,'S: volatile optical state',12.5,True)
mathlabel(466,291,[('G',''),('ij','sub'),(' from light history','')])
text(466,311,'0 V external sensing bias')
text(466,331,'Accumulate in light; decay in dark')
text(124,362,'Internal state, not a digitized readout image',12.5)
# sparse aligned inter-plane connections
for x,y in [(252,314),(328,323)]:line(x,y+11,x,y+95,color='#a8b1bb',width=1.1)
# third layer
title(3,37,392,'Voltage weighting')
text(55,408,'and current summation')
plane_group('weight-circuit-plane',177,415);rect(-7,-7,234,134,'#f0f4f8','#97a8ba')
colors=['#719bc7','#dce8f3','#ffffff','#f4d7d4','#c8817b']
for j in range(4):
 for i in range(7):
  x=i*31+3;y=j*29+3
  rect(x,y,25,22,colors[(i+2*j)%5],'#9ba7b4')
  # Simplified capacitor/repeated cell symbol, no full addressing lines.
  line(x+8,y+5,x+8,y+17,width=1)
  line(x+14,y+5,x+14,y+17,width=1)
plane_end()
text(108,513,'Capacitor-stored weights')
for x,c in [(111,'#719bc7'),(146,'#ffffff'),(181,'#c8817b')]:rect(x,527,22,12,c,'#a2abb5')
text(113,556,'−',12.5);text(151,556,'0',12.5);text(186,556,'+',12.5)
# One-pixel circuit callout: S remains on sensor layer, not duplicated.
group('one-pixel-inset')
rect(443,365,272,161,'#fbfcfd','#c2cbd4',5)
text(455,383,'One pixel: TG1–C–TG2 → S above',12.5,True)
mathlabel(452,413,[('V',''),('in','sub')])
line(478,409,495,409)
rect(495,399,38,20,'white','#6d7a87',2);text(514,413,'TG1',10.7,False,'middle')
line(533,409,559,409);circle(559,409,2.4,INK,INK)
mathlabel(548,396,[('V',''),('C','sub')])
line(559,409,589,409);rect(589,399,38,20,'white','#6d7a87',2);text(608,413,'TG2',10.7,False,'middle');line(627,409,678,409)
text(656,397,'to S',10.7)
# exact C reference branch
line(559,409,559,432);line(548,432,570,432);line(548,438,570,438);line(559,438,559,449)
line(549,449,569,449);line(552,454,566,454);line(555,459,563,459);text(577,440,'C',12.5)
text(454,480,'Write: TG1 ON, TG2 OFF',12.5)
text(454,499,'Read: TG1 OFF, TG2 ON',12.5)
mathlabel(454,518,[('Fixed V',''),('in','sub'),('; variable t',''),('write','sub')],12.5)
# sensor selected-cell coordinate from its affine plane
sx=177+97.5-.65*68.5;sy=265+.12*97.5+.45*68.5
circle(sx,sy,3.3,'#9e83be','#443452')
# TG2 to same actual S pixel; does not add a second sensor.
path(f'M678 409 L701 409 L701 349 L{sx+9:.2f} 349 L{sx+9:.2f} {sy:.2f}',color='#8b78a4',arrow=True)
# Sensor read current terminal routes conceptually into common sum interface.
path(f'M{sx-7:.2f} {sy+7:.2f} L{sx-7:.2f} 341 L12 341 L12 476 L16 476',color='#657581',arrow=True)
text(33,460,'Pixel currents',10.7)
rect(16,469,76,37,'white','#8193a4',3);text(53,485,'Σ I',12.5,False,'middle');text(53,499,'Virtual GND',10.7,False,'middle')
end()
# mathematical chain, not a weight-only arrow into sum
group('product-then-sum')
mathlabel(274,535,[('I',''),('ij','sub'),(' ≈ G',''),('ij','sub'),(' · V',''),('C,ij','sub')])
mathlabel(274,557,[('I',''),('out','sub'),('(k)','sup'),(' ≈ Σ',''),('ij','sub'),(' G',''),('ij','sub'),(' · V',''),('C,ij','sub'),('(k)','sup')])
mathlabel(498,545,[('G ⊙ V',''),('(k)','sup')],12.5)
line(572,541,595,541,arrow=True);text(609,545,'Σ',15);line(626,541,651,541,arrow=True);text(660,545,'Scalar',12.5)
end()
# classification floating panel; templates precede independent outputs
title(4,37,591,'Classification from weighted outputs')
group('classification-result')
rect(108,607,604,66,'#fbfcfe','#b5c1ce',5)
for n in range(3):
 x=122+n*37
 for j in range(3):
  for i in range(3):rect(x+i*7,617+j*7,6.6,6.6,colors[(i+j+n)%5],'none')
 text(x+8,653,str(n+1),10.7,False,'middle')
text(123,667,'Templates k',10.7)
line(232,635,258,635,arrow=True)
mathlabel(269,636,[('I',''),('out','sub'),('(1)','sup'),(', I',''),('out','sub'),('(2)','sup'),(', …','')])
line(379,635,399,635,arrow=True)
text(409,622,'One current per weight template',10.7)
# illustrative uncalibrated class scores; T-shirt wins, no numeric values
for x,h,c in [(434,14,'#cbd3dd'),(470,29,'#9e83be'),(506,10,'#cbd3dd'),(542,17,'#cbd3dd')]:rect(x,659-h,18,h,c,'none')
line(423,659,573,659,width=.8)
text(594,646,'T-shirt',12.5,True,color='#77598d');text(591,663,'Illustrative scores',10.7)
# real output arrow from summation interface enters template evaluation, not all classes directly
path('M53 506 L53 636 L103 636',arrow=True)
mathlabel(25,550,[('I',''),('out','sub'),('(k)','sup')],10.7)
end()
# synchronized traces
text(778,83,'Schematic response',13.5,True)
X0=778;X1=1050;split=.62;W=X1-X0
rect(X0,111,W*split,500,'#f1edf7','none')
rect(X0+W*split,111,W*(1-split),500,'#eaf2fa','none')
text(X0+W*split/2,102,'Sensing',12.5,False,'middle')
text(X0+W*(1+split)/2,102,'Readout',12.5,False,'middle')
pulses=[(.07,.12),(.19,.24),(.31,.36),(.43,.48)];rp=[(.69,.73,.42),(.80,.84,.9),(.91,.95,.66)]
def optical(t):return any(a<=t<b for a,b in pulses)
def voltage(t):return next((v for a,b,v in rp if a<=t<b),0.)
N=4000;g=.02;Gs=[]
for n in range(N+1):
 t=n/N;g+=((1-g)*14 if optical(t) else -g*1.5)/N;Gs.append(g)
assert len({round(b-a,5) for a,b in pulses})==1
assert max(b for a,b in pulses)<min(a for a,b,v in rp)
assert all(not optical(n/N) or voltage(n/N)==0 for n in range(N+1))
for k,(lab,baseline) in enumerate([('Optical pulses',206),('Photoconductance G',331),('Read voltage',456),('Read current I',581)]):
 group('response-trace-'+str(k));text(X0+3,baseline-72,lab,12.5)
 if k==2:mathlabel(X0+170,baseline-72,[('V',''),('read','sub')])
 line(X0+4,baseline+2,X1,baseline+2,color='#969fa9',width=.8)
 pts=[]
 for n in range(N+1):
  t=n/N;z=.9*optical(t) if k==0 else Gs[n] if k==1 else voltage(t) if k==2 else Gs[n]*voltage(t)*1.8
  pts.append(f'{X0+4+(W-5)*t:.3f},{baseline-49*z:.3f}')
 S.append('<polyline points="'+' '.join(pts)+'" fill="none" stroke="#171d24" stroke-width="1.7"/>');end()
line(X0+4,627,X1,627,arrow=True);text(X1,649,'Time',12.5,False,'end')
text(780,674,'No measured values',10.7)
text(26,704,'Conceptual functional layers, not a physical 3D stack.',12.5)
S.append('</svg>')
svg=O/'2TG1C1S_layered.svg';svg.write_text('\n'.join(S))
# Retain the illustrative temporal model and assumptions for scientific review.
(O/'design-notes.md').write_text('''# Layered Fig. 1 draft\n\nConceptual functional layers, not a physical 3D stack. Spatial layer order does not establish sensing/write chronology or validated parallel operation. The same selected sensor is used by the single-pixel inset; no extra S is drawn in the circuit layer. TG1 connects V_in to the capacitor node; C connects that node to reference ground; TG2 connects it to the selected S in the sensor layer, whose read current enters a virtual-ground summation interface. Rest-of-array icons are intentionally abstract.\n\nLight history establishes volatile G; capacitor voltage V_C provides a distinct electrical state. Weight writing uses fixed V_in and variable TG1 on duration. Readout assumes approximately ohmic behavior, small switch drops and negligible capacitor droop over short pulses. Signed capacitor weights are shown conceptually as requested; right-hand traces illustrate positive read voltages only. Implementation of negative voltages requires author confirmation.\n\nClassification uses separate scalar currents from successive weight templates. The score-card geometry is illustrative, uncalibrated and contains no measured values. G is an internal state, not an already digitized readout image. Pixel count is conceptual.\n\nAll four traces are generated from one arbitrary accumulation/decay model. Four identical optical pulses occur in sensing; G rises during pulses and continuously decays in dark. Three read-voltage pulses occur after the last optical pulse; current is the pointwise product of G and voltage. No measured performance, energy or accuracy is implied.\n\nSVG uses editable text and grouped vector shapes. Fonts: DejaVu Sans, with Arial/sans-serif fallback. No image model or third-party generated component was used. Perspective conveys functional separation, as explicitly requested, rather than device fabrication geometry. Red/blue/white denote signed electrical weights as explicitly requested. Publication eligibility and scientific interpretation require author review.\n\n## Caption\n(a) Functional layers for optical-history encoding, capacitor weight storage, current summation and template-based classification in a GaON/GaN photomemristive 2TG1C1S array. Optical input produces volatile conductance G at zero externally applied sensor bias. TG1 writes capacitor voltage V_C; TG2 applies it to the same sensor during readout. Each template produces one scalar summed current; successive templates support classification. (b) Shared-time schematic responses: optical pulses, conductance, sensor read voltage and read current.\n''')
try:
 import cairosvg
 cairosvg.svg2png(url=str(svg),write_to=str(O/'2TG1C1S_layered.png'),output_width=3240,output_height=2160)
 cairosvg.svg2pdf(url=str(svg),write_to=str(O/'2TG1C1S_layered.pdf'))
 print('Created SVG, PNG and vector PDF in',O)
except ImportError:
 print('SVG created. Install cairosvg to render PNG/PDF.')
