"""Generate a four-page, LinkedIn-ready PDF case study from evaluation metrics."""
from pathlib import Path
import json, math
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs'/'PROJECT_CASE_STUDY.pdf'
m=json.loads((ROOT/'artifacts'/'evaluation_manifest.json').read_text(encoding='utf8'))
W,H=A4
bg=HexColor('#0B1627'); card=HexColor('#142842'); card2=HexColor('#172F49'); mint=HexColor('#60E3CF'); white=HexColor('#F4F8FC'); light=HexColor('#CEDCEB'); muted=HexColor('#A1B7CA'); coral=HexColor('#FFB59D'); stroke=HexColor('#31506A')
for name, fname in [('R','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'),('B','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(name,fname))

c=canvas.Canvas(str(OUT),pagesize=A4,pageCompression=1)
c.setTitle('Agentic Payment Trust Lab | Project 05')
c.setAuthor('Adiputera Saadon')
c.setSubject('Educational agentic payment governance simulation')

def txt(text,x,top,width=470,size=10,leading=None,font='R',color=light,max_lines=None):
    if isinstance(leading, str) and not isinstance(font, str):
        color, font, leading = font, leading, None
    leading=leading or size*1.5
    lines=simpleSplit(str(text),font,size,width)
    if max_lines: lines=lines[:max_lines]
    c.setFillColor(color);c.setFont(font,size)
    for j,line in enumerate(lines): c.drawString(x,top-j*leading,line)
    return top - len(lines)*leading

def pill(text,x,top,fg=mint,fill=card):
    size=8.4; width=pdfmetrics.stringWidth(text,'B',size)+24
    c.setFillColor(fill);c.roundRect(x,top-18,width,23,11,fill=1,stroke=0)
    c.setFont('B',size);c.setFillColor(fg);c.drawString(x+12,top-10,text)
    return width

def roundbox(x,bottom,w,h,fill=card,line=None,r=12):
    c.setFillColor(fill); c.setStrokeColor(line or fill)
    c.roundRect(x,bottom,w,h,r,fill=1,stroke=bool(line))

def accent_line(x,y,x2,y2,color=mint,w=1.5):
    c.setStrokeColor(color); c.setLineWidth(w); c.line(x,y,x2,y2)

def page(k,eyebrow):
    c.setFillColor(bg);c.rect(0,0,W,H,fill=1,stroke=0)
    c.setFillColor(mint);c.rect(0,H-9,W,9,fill=1,stroke=0)
    txt('P R O J E C T   0 5   /   A I   G O V E R N A N C E',42,H-43,500,8,font='B',color=mint)
    txt(eyebrow.upper(),42,H-68,515,8.5,font='B',color=muted)
    accent_line(42,64,W-42,64,stroke,0.7)
    txt('AGENTIC PAYMENT TRUST LAB',42,45,400,8,font='B',color=muted)
    txt(f'{k}  /  4',W-92,45,60,8,font='B',color=mint)

def metricbox(x,bottom,w,kicker,value,sub,main_color=white):
    roundbox(x,bottom,w,100)
    txt(kicker.upper(),x+15,bottom+80,w-30,8,font='B',color=muted)
    txt(value,x+15,bottom+54,w-30,21,font='B',color=main_color)
    txt(sub,x+15,bottom+29,w-30,7.6,color=light)

def footer():c.showPage()

# 1 - Cover
page(1,'Executive case study')
pill('FICTIONAL DATA  /  NO MONEY MOVEMENT',42,714)
txt('When AI agents\ncan propose payments,\nwho controls the money?',42,669,500,29,40,'B',white)
txt('AGENTIC PAYMENT TRUST LAB',42,515,490,12,'B',mint)
txt('An educational experiment in delegated authority, buyer-approved invoices, independent runtime controls and accountable human intervention.',42,487,480,11,17,'R',light)
# Stylised rails and controls
for i,lab in enumerate(['APPROVED INVOICE','DELEGATED AGENT','INDEPENDENT GATE']):
    xx=42+i*173
    roundbox(xx,291,161,80,card2)
    txt(f'0{i+1}',xx+13,347,44,9,'B',mint)
    txt(lab,xx+13,320,142,9,'B',white)
    if i<2:
        accent_line(xx+163,330,xx+171,330,mint,2)
for i,(label,col) in enumerate([('ALLOW',mint),('HOLD',coral),('BLOCK',HexColor('#FE8691'))]):
    xx=42+i*173
    roundbox(xx,235,161,39,card)
    c.setFillColor(col);c.circle(xx+18,254,5,stroke=0,fill=1)
    txt(label,xx+32,251,126,9,'B',white)
metricbox(42,112,161,'Synthetic proposals',f"{m['total_synthetic_proposals']:,}",'13 scripted scenario families')
metricbox(215,112,161,'Test holdout',str(m['test_proposals']),'Separate from model training')
metricbox(388,112,165,'Fictional supplier IDs','12','3 delegated agent mandates')
footer()

# 2 - Design and purpose
page(2,'Business case and control architecture')
txt('Automate the routine.\nChallenge the exception.',42,731,520,25,34,'B',white)
txt('Corporate supplier payment services need speed without confusing delegated execution with unchecked decision authority.',42,651,515,10.5,17,'R',light)
pill('REFERENCE CASE  /  BUYER-APPROVED PAYMENTS',42,589)
roundbox(42,434,510,132,card)
txt('Why this lab now',58,545,440,12,'B',mint)
txt('Visa, BILL and Billtrust announced a live pilot in October 2026 allowing trusted agents to complete eligible supplier invoice payments that buyers had already approved. This lab studies the governance boundary, not that commercial implementation.',58,519,475,9.5,15,'R',light)
steps=[('01','AUTHORITY','Known agent; supplier scope; amount limit'),('02','EVIDENCE','Buyer approval; payee registry; duplicate check'),('03','POLICY','Independent ALLOW / HOLD / BLOCK gate'),('04','OVERSIGHT','Human exception review; mocked audit export')]
for i,(num,title,sub) in enumerate(steps):
    yy=336-i*66
    roundbox(42,yy,510,57,card2)
    txt(num,58,yy+37,37,13,'B',mint)
    txt(title,107,yy+37,155,10,'B',white)
    txt(sub,245,yy+35,295,8.4,'R',light)
    if i<3:
        accent_line(296,yy-1,296,yy-9,mint,1.2)
txt('Governance objective',42,91,160,9,'B',mint)
txt('Reject unauthorised payment proposals while measuring legitimate-payment friction and documenting human review.',166,91,385,8.7,'R',light)
footer()

# 3 - Metrics
page(3,'Synthetic benchmark findings')
txt('Safety must be measured\nalongside payment friction.',42,730,520,24,34,'B',white)
txt('Holdout = 255 fictional proposals. 120 were labelled unsafe through scripted case design, not inferred from the gate.',42,642,515,9.8,15,'R',light)
metricbox(42,496,161,'Policy intervention recall',f"{m['policy']['recall']*100:.1f}%",'HOLD or BLOCK on unsafe cases',mint)
metricbox(215,496,161,'Anomaly model recall',f"{m['anomaly_model']['recall']*100:.1f}%",'Isolation Forest alerts',white)
metricbox(388,496,165,'Policy precision',f"{m['policy']['precision']*100:.1f}%",'Share of alerts labelled unsafe',white)

txt('Held-out performance comparison',42,460,495,12,'B',mint)
rows=[('Policy recall',m['policy']['recall'],mint),('Isolation Forest recall',m['anomaly_model']['recall'],coral),('Policy precision',m['policy']['precision'],mint),('Legitimate straight-through',m['policy_legitimate_straight_through'],mint),('Legitimate false hold rate',m['policy_false_hold_rate_legitimate'],coral)]
for i,(label,val,col) in enumerate(rows):
    top=426-i*45
    txt(label,42,top,245,9.2,'R',white)
    roundbox(258,top-10,255,15,card2,r=5)
    c.setFillColor(col);c.roundRect(258,top-10,max(1,val*255),15,5,stroke=0,fill=1)
    txt(f'{val*100:.1f}%',520,top,40,9,'B',light)
roundbox(42,102,510,84,card)
txt('SGD '+format(m['scripted_unsafe_value_intervened_sgd'],',.2f'),58,158,465,20,'B',mint)
txt('Face value of scripted unsafe proposals intercepted by HOLD or BLOCK.',58,137,470,8.5,'R',light)
txt('Not real losses avoided; no transactions or funds existed.',58,120,465,8.5,'R',coral)
footer()

# 4 - Assurance, limitations, credit
page(4,'Governance lessons and future development')
txt('What the experiment\nmeans for a board.',42,731,515,26,35,'B',white)
txt('Decision-support value comes from a verifiable chain of authority, payment evidence, control rationale and human accountability - not from a confident anomaly score.',42,641,500,10.2,16,'R',light)
items=[
('01','DEFINED AUTHORITY','Link every proposal to the correct agent, invoice approval, beneficiary and spending mandate.'),
('02','PROPORTIONATE INTERVENTION','Block hard violations; hold evidence gaps for independent review; avoid needless supplier delays.'),
('03','MEASURABLE ASSURANCE','Track unsafe intervention recall, legitimate false holds, anomalous misses and control limitations.'),
('04','HUMAN ACCOUNTABILITY','Record an investigator decision and rationale without permitting a review note to bypass controls.'),
]
for i,(num,head,body) in enumerate(items):
    bottom=517-i*90
    roundbox(42,bottom,510,80,card)
    txt(num,56,bottom+54,34,14,'B',mint)
    txt(head,99,bottom+55,435,10,'B',white)
    txt(body,99,bottom+34,428,8.7,13,'R',light)
roundbox(42,107,510,65,HexColor('#27314A'))
txt('LIMITATIONS  /  NO PRODUCTION SECURITY CLAIMS',55,151,480,8.4,'B',coral)
txt('Scripted case families overlap with rule design. No payment APIs, real credentials, authenticated mandates, true bank verification, immutable logs or external validation are implemented.',55,134,480,8.3,12,'R',light)
txt('Reference context  |  Visa agentic B2B pilot (20 Oct 2026)  /  MAS SAFR (Jul 2026)  /  MAS AI guidelines (Oct 2026)',42,87,510,7.2,'R',muted)
# Authorship credit at the END of final page above footer rule.
txt('By Adiputera Saadon',W-239,76,197,10,'B',mint)
footer()

c.save()
print(OUT)
