import pandas as pd, numpy as np, json, pathlib
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.pagesizes import A4
p=pathlib.Path('/mnt/data/coca_project');df=pd.read_csv(p/'data/CocaCola_Inventory_Distribution_MySQL_Ready.csv',parse_dates=['Date'])
for c in ['Market','Country','Product','Warehouse_ID','Transport_Mode','Sales_Channel','Season','Promotion']:
 print(c,df[c].nunique())
checks={
'below_reorder':int((df.Closing_Inventory_Units<=df.Reorder_Point_Units).sum()),
'below_safety':int((df.Closing_Inventory_Units<df.Safety_Stock_Units).sum()),
'overstock_1_without_closing_above_reorder':int(((df.Overstock_Flag==1)&(df.Closing_Inventory_Units<=df.Reorder_Point_Units)).sum()),
'closing_above_opening_plus_production':int((df.Closing_Inventory_Units>df.Opening_Inventory_Units+df.Production_Units).sum()),
'forecast_over':int((df.Forecast_Demand_Units>df.Demand_Units).sum()),
'forecast_under':int((df.Forecast_Demand_Units<df.Demand_Units).sum()),
'forecast_exact':int((df.Forecast_Demand_Units==df.Demand_Units).sum()),
'mean_lead':float(df.Lead_Time_Days.mean()),
'weighted_ape':float(abs(df.Forecast_Demand_Units-df.Demand_Units).sum()/df.Demand_Units.sum()*100),
'overstock_flag_pct':float(df.Overstock_Flag.mean()*100),
}
print(json.dumps(checks,indent=2))
market=df.groupby('Market').agg(rows=('Market','size'),demand=('Demand_Units','sum'),revenue=('Sales_Revenue_USD','sum'),overstock=('Overstock_Flag','mean'),lead=('Lead_Time_Days','mean'),waste=('Waste_Cost_USD','sum'),transport=('Transport_Cost_USD','sum')).sort_values('revenue',ascending=False)
print(market.round(2).to_string());
(p/'data/extended_audit.json').write_text(json.dumps(checks,indent=2));market.to_csv(p/'data/extended_market_metrics.csv')
styles=getSampleStyleSheet();styles.add(ParagraphStyle(name='SmallBodyX',parent=styles['BodyText'],fontSize=9.5,leading=14,spaceAfter=10));styles.add(ParagraphStyle(name='HeaderX',parent=styles['Heading2'],textColor=colors.HexColor('#153B60'),spaceBefore=14,spaceAfter=8))
flow=[]
def heading(s):flow.append(Paragraph(s,styles['HeaderX']))
def par(s):flow.append(Paragraph(s,styles['SmallBodyX']))
def tab(headers,rows,widths=None):
 t=Table([[Paragraph(str(x),styles['SmallBodyX']) for x in headers]]+[[Paragraph(str(x),styles['SmallBodyX']) for x in row] for row in rows],colWidths=widths,repeatRows=1,hAlign='LEFT');t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E9F0F7')),('LINEBELOW',(0,0),(-1,0),0.8,colors.HexColor('#28618C')),('VALIGN',(0,0),(-1,-1),'TOP'),('BOTTOMPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F6F8FB')])]))
 flow.append(t)
heading('Project improvement audit | 29 October 2026')
par('Coca-Cola Inventory &amp; Distribution | Evidence-based supplement to the initial project package. All calculations below were performed locally from the unchanged 50,000-row source CSV. This is not a substitute for MySQL, Databricks or Power BI execution evidence.')
heading('1. Gaps in the earlier package')
tab(['Deliverable','Current gap / required correction'],[['Faculty report','Initial report is 8 pages, not the approximately 30 pages specified. Expand only with evidence and meaningful commentary.'],['MySQL and DBeaver','SQL written but not run against a live MySQL instance; obtain actual 50,000-row import validation and saved outputs.'],['Databricks','Notebook/code prepared; Delta table creation and Spark execution not verified.'],['Power BI','Dashboard specifications are not a PBIX; build three measures, four visuals and slicers with checked totals.'],['Dataset provenance','Original public publisher or permitted provider has not been documented.'],['GitHub and presentation','Repository and individual demonstration require real publication and proof.'],['Faculty database requirement','Guideline names PostgreSQL, while chosen project implementation is MySQL. Request approval.']],[135,360])
heading('2. Further observed checks')
tab(['Check','Verified value','Interpretation'],[['Rows closing at/below supplied reorder point',f"{checks['below_reorder']:,}",'Potential review alerts, not necessarily orders.'],['Rows closing below safety stock',f"{checks['below_safety']:,}",'Investigate definitions and timestamps.'],['Overstock flag AND closing at/below reorder',f"{checks['overstock_1_without_closing_above_reorder']:,}",'Concurrent flags/thresholds require interpretation; overstock definition unknown.'],['Forecast above actual',f"{checks['forecast_over']:,}",'Row-level counts, no known forecast horizon.'],['Forecast below actual',f"{checks['forecast_under']:,}",'Forecast bias cannot be inferred without period details.'],['Forecast exactly equal actual',f"{checks['forecast_exact']:,}",'Exact matches.'],['Weighted absolute percentage error',f"{checks['weighted_ape']:.2f}%",'Sum of absolute errors divided by sum of recorded demand.']],[220,75,200])
heading('3. Source-derived market comparison')
tab(['Market','Demand units','Revenue USD','Overstock rate'],[[i,f'{r.demand:,.0f}',f'{r.revenue:,.2f}',f'{r.overstock*100:.1f}%'] for i,r in market.iterrows()],[135,105,130,125])
heading('4. Critical interpretation rules')
par('The 85.2% overstock-flagged share is NOT automatically 85.2% of physical inventory held in excess. The dataset lacks the documented algorithm behind Overstock_Flag. Reorder-point and safety-stock figures are pre-existing fields, not independently optimized policy recommendations. Sales and demand match for every record, so any unobserved lost sales cannot be measured here.')
par('The 3,841 inventory-balance discrepancies are based on an assumed equation: opening plus production minus sales minus waste equals closing. Inter-warehouse transfers, returns, adjustment events or time-boundary mismatches could explain deviations. Avoid correcting balances without system definitions.')
heading('5. Recommended work sequence')
par('<b>Step 1:</b> Verify dataset publisher/permission and define the row grain (warehouse-product-date-market or otherwise). <b>Step 2:</b> Confirm how overstock, stock-out, service level, turnover, demand and costs were calculated. <b>Step 3:</b> Import exact CSV to MySQL 8 using DBeaver, run the validation suite and export real results. <b>Step 4:</b> Execute the Python notebook end-to-end and preserve its output. <b>Step 5:</b> Execute Databricks Delta pipeline and save screenshots. <b>Step 6:</b> Build and reconcile Power BI with the source totals. <b>Step 7:</b> Fill report evidence sections, GitHub link and team contributions; then create a live demonstration script.')
heading('6. Faculty-aligned report architecture')
tab(['Pages','Chapter / evidence'],[['1-5','Cover, abstract, business problem, scope and limitations'],['6-8','Data source, complete dictionary, quality checks, workflow'],['9-11','MySQL design, import, live DBeaver query screenshots'],['12-15','Python methods, 3+ charts, substantive observations'],['16-18','Databricks / Delta methods and actual Spark output'],['19-22','Power BI KPIs, 4+ visuals, filters, screenshots'],['23-26','Cross-tool reconciliation; findings and recommendations'],['27-30','Conclusion, contribution, references, appendix and evidence']],[80,415])
par('No project section should imply a system was executed without screenshots or logs. The expansion above is an evidence roadmap, not a claim that those later stages are finished.')
out=p/'report'/'Project_Gap_and_Validation_Supplement.pdf'
doc=SimpleDocTemplate(str(out),pagesize=A4,leftMargin=48,rightMargin=48,topMargin=44,bottomMargin=44);doc.build(flow);print('OUTPUT',out)
