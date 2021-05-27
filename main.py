import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date
from datetime import datetime
from datetime import timedelta
import json

# generate credentials file (gauth.json) through Google Cloud Platform, specifically a service account
gauthFile = 'gauth.json'

#doucment name/id from Google Sheets
documentName = ['Business LTD','Invoice']
documentID = 'Unique Document ID goes here'

#Load json file in memory
gauthFile = 'gauth.json'
with open('gauth.json', 'r') as myfile:
    data=myfile.read()
jsonFile = json.loads(data)

#Client Details
scope = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(gauthFile,scope)

#Make your document edits here.. here are mine as an example.
sheet = gspread.authorize(credentials).open(documentName[0]).worksheet(documentName[1])

invoice_date = date.today().strftime('%b %Y')
po_reference_str = date.today().strftime('RG-PO041351768-%b%d')
date_issued_str = date.today().strftime('%d-%b-%Y')
due_date_str = (datetime.now() + timedelta(days=10)).strftime('%d-%b-%Y')
desc_str = date.today().strftime("Business's %B Monthly Fixed Fee")

sheet.update_cell(5,7,po_reference_str)
sheet.update_cell(6,7,date_issued_str)
sheet.update_cell(7,7,due_date_str)
sheet.update_cell(12,2,desc_str)

#Download the file
export_url = f'https://docs.google.com/spreadsheets/export?format=pdf&id={documentID}'
exportedFilename = 'Business LTD Invoice'
headers = {'Authorization': 'Bearer ' + credentials.create_delegated(jsonFile['client_email']).get_access_token().access_token}
res = requests.get(export_url, headers=headers)
with open(f"{exportedFilename} {invoice_date}.pdf", 'wb') as f:
    f.write(res.content)
