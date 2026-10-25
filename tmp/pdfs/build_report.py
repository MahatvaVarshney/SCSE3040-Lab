from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from pathlib import Path

out = Path('output/pdf/SCSE3040_P07_roll-number.pdf')
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Cover', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=23, leading=28, textColor=colors.HexColor('#102D46'), alignment=TA_LEFT, spaceAfter=8))
styles.add(ParagraphStyle(name='Sub', parent=styles['Normal'], fontSize=11, leading=16, textColor=colors.HexColor('#4B6477'), spaceAfter=14))
styles.add(ParagraphStyle(name='H1x', parent=styles['Heading1'], fontSize=16, leading=20, textColor=colors.HexColor('#102D46'), spaceBefore=8, spaceAfter=8))
styles.add(ParagraphStyle(name='H2x', parent=styles['Heading2'], fontSize=11, leading=14, textColor=colors.HexColor('#117C83'), spaceBefore=8, spaceAfter=5))
styles.add(ParagraphStyle(name='Bodyx', parent=styles['BodyText'], fontSize=9.5, leading=14, textColor=colors.HexColor('#263746'), spaceAfter=6))
styles.add(ParagraphStyle(name='Smallx', parent=styles['BodyText'], fontSize=8, leading=11, textColor=colors.HexColor('#526779')))
styles.add(ParagraphStyle(name='Code', parent=styles['Code'], fontName='Courier', fontSize=8.5, leading=13, backColor=colors.HexColor('#F1F5F8'), borderPadding=8, leftIndent=6, rightIndent=6, spaceBefore=3, spaceAfter=7))

def footer(canvas, doc):
    canvas.saveState(); w,h=A4
    canvas.setStrokeColor(colors.HexColor('#D9E2E8')); canvas.line(18*mm,15*mm,w-18*mm,15*mm)
    canvas.setFont('Helvetica',8); canvas.setFillColor(colors.HexColor('#63798A'))
    canvas.drawString(18*mm,10*mm,'SCSE3040 | Practical 07 | Evidence report')
    canvas.drawRightString(w-18*mm,10*mm,f'{doc.page}')
    canvas.restoreState()

def P(s, style='Bodyx'): return Paragraph(s, styles[style])
def box(title, text):
    t=Table([[P('<b>'+title+'</b><br/>'+text,'Bodyx')]], colWidths=[174*mm])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#F2F6F8')),('BOX',(0,0),(-1,-1),0.7,colors.HexColor('#CBD8E0')),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
    return t

story=[]
story += [Spacer(1,16*mm),P('PRACTICAL 07','Sub'),P('Putting the Model<br/>Behind an Address','Cover'),P('SCSE3040 Machine Learning Operations | Bennett University | Session 2026-27','Sub')]
meta=Table([[P('<b>Student name</b>','Bodyx'),P('________________________________','Bodyx')],[P('<b>Roll number</b>','Bodyx'),P('________________________________','Bodyx')],[P('<b>Batch</b>','Bodyx'),P('________________________________','Bodyx')],[P('<b>Laboratory date</b>','Bodyx'),P('________________________________','Bodyx')]],colWidths=[42*mm,132*mm],rowHeights=[12*mm]*4)
meta.setStyle(TableStyle([('BACKGROUND',(0,0),(0,-1),colors.HexColor('#EAF1F5')),('GRID',(0,0),(-1,-1),0.5,colors.HexColor('#CBD8E0')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('LEFTPADDING',(0,0),(-1,-1),8)]))
story += [meta,Spacer(1,10*mm),P('Purpose','H1x'),P('This report records the completed P07 serving practical: a trained delivery-time model exposed through a FastAPI service, with model information, live prediction calls in the notebook test client, and input validation. The project code was not changed for this report.','Bodyx'),box('Submission evidence status','Notebook outputs are present in the supplied project. The required live MLflow registry, serving terminal, and curl/response screenshots were not present in the workspace and are not represented as captured evidence here. Insert genuine screenshots before submitting.'),PageBreak()]

story += [P('1. Model and registry','H1x'),P('P07 model artifact and serving details','H2x')]
data=[[P('<b>Item</b>','Bodyx'),P('<b>Value from project</b>','Bodyx')],[P('Registered model','Bodyx'),P('Delivery-time model; registry name / production version needs confirmation from MLflow UI.','Bodyx')],[P('Model implementation','Bodyx'),P('LinearRegression','Bodyx')],[P('Model version','Bodyx'),P('Service response reports model_version 1.0.0. This is the app version, not independently confirmed as an MLflow registry version.','Bodyx')],[P('Run ID','Bodyx'),P('Not established from available P07 evidence. Copy from the MLflow registered model/version page.','Bodyx')],[P('Serving port','Bodyx'),P('8000 (configured command in P07 notebook).','Bodyx')]]
t=Table(data,colWidths=[43*mm,131*mm],repeatRows=1)
t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#EAF1F5')),('GRID',(0,0),(-1,-1),0.5,colors.HexColor('#CBD8E0')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
story += [t,Spacer(1,6*mm),P('Required screenshot: MLflow Model Registry','H2x'),P('Capture the actual registered model page with its model name, version number, and stage set to Production visible. Paste the screenshot below this heading in the final submission. The available files do not contain this registry screenshot, so the required production stage is unverified.','Bodyx'),box('Registry screenshot to insert','[Paste an uncropped screen capture of the MLflow Model Registry page here. Show the model name, version, and Production stage.]'),PageBreak()]

story += [P('2. Serving and prediction evidence','H1x'),P('P07 walkthrough results','H2x'),P('The executed notebook reports a training MAE of 1.92 minutes. Its TestClient successfully exercised the API endpoints and returned a prediction for a dry and a rainy version of the same order.','Bodyx')]
rows=[[P('<b>Check</b>','Bodyx'),P('<b>Observed result</b>','Bodyx')],[P('GET /health','Bodyx'),P('200; service reports status ok and model loaded.','Bodyx')],[P('POST /predict, dry order','Bodyx'),P('29.5 minutes (3 km, 15 min prep, traffic 1, no rain).','Bodyx')],[P('POST /predict, wet order','Bodyx'),P('35.0 minutes (same order, rain).','Bodyx')],[P('POST /predict, distance 30 km','Bodyx'),P('422 validation response.','Bodyx')],[P('POST /predict, distance 10 km','Bodyx'),P('200 accepted.','Bodyx')],[P('Notebook self-check','Bodyx'),P('9 of 9 checks passed.','Bodyx')]]
t=Table(rows,colWidths=[58*mm,116*mm],repeatRows=1)
t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#EAF1F5')),('GRID',(0,0),(-1,-1),0.5,colors.HexColor('#CBD8E0')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),3)]))
story += [t,Spacer(1,6*mm),P('Required screenshot: running MLflow serving terminal','H2x'),P('Capture the terminal after starting the model server. Keep the serving command, port, and server confirmation line visible. The notebook specifies port 8000. No live terminal screenshot was available in the project.','Bodyx'),box('Terminal screenshot to insert','[Paste a genuine screenshot of the terminal running mlflow models serve, with port and serving confirmation visible.]'),Spacer(1,7*mm),P('Required screenshot: curl request and response','H2x'),P('Capture the actual curl command and the prediction response returned by the running server. The notebook demonstrates TestClient requests, but those are not evidence of a live curl response.','Bodyx'),box('Request/response screenshot to insert','[Paste a genuine screenshot showing the curl command and the server prediction response.]'),PageBreak()]

story += [P('3. Configuration and disclosure','H1x'),P('Service configuration','H2x'),P('The P07 notebook specifies the following command to run the FastAPI application from the work directory:','Bodyx'),P('python -m uvicorn app:app --reload --port 8000','Code'),P('The application identifies itself as Delivery Time Predictor, version 1.0.0. It accepts distance_km values above zero and up to 25 km, prep_time_min from 0 to 120, traffic_level from 1 to 3, and rain as 0 or 1.','Bodyx'),P('AI use disclosure','H2x'),P('AI assistance was used to interpret the assignment instructions and assemble this report from the existing project outputs. No project code was changed. Verify and edit this disclosure if needed to accurately describe all AI tools used in completing the practical.','Bodyx'),P('Completion checklist','H2x')]
check=[['Required element','Status'],['Name, roll number, batch, lab date','Fill in above'],['Model Registry screenshot (Production stage visible)','Still required'],['Running MLflow serving terminal screenshot','Still required'],['curl request and prediction response screenshot','Still required'],['Model name, MLflow version, run ID','Confirm against Registry UI'],['AI use disclosure','Review for accuracy']]
t=Table([[P('<b>'+a+'</b>','Bodyx'),P('<b>'+b+'</b>','Bodyx')] if i==0 else [P(a,'Bodyx'),P(b,'Bodyx')] for i,(a,b) in enumerate(check)],colWidths=[105*mm,69*mm])
t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#EAF1F5')),('GRID',(0,0),(-1,-1),0.5,colors.HexColor('#CBD8E0')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),2)]))
story += [t,Spacer(1,7*mm),P('Source evidence: P07 notebook outputs and P07 serving application in the supplied workspace. The model registry screenshot and live serving/curl evidence must come from the student’s actual MLflow session.','Smallx')]

doc=SimpleDocTemplate(str(out),pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,topMargin=17*mm,bottomMargin=22*mm,title='SCSE3040 P07 Evidence Report',author='')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(out.resolve())
