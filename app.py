from flask import Flask, render_template, send_file
import xml.etree.ElementTree as ET
import requests
from PyPDF2 import PdfMerger
import pathlib
import os

app = Flask(__name__)

printer_url = 'http://192.168.1.3'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/print", methods=['GET'])
def scan():
    startScanning()
    jobNumber = getLatestJobNumber()
    
    response = requests.get(printer_url + '/Scan/Jobs/'+ str(jobNumber) +'/Pages/1')
    print(response.status_code)
    
    with open("scans/input/scan-"+ jobNumber +".pdf","wb") as bin_file:
        bin_file.write(response.content)
        
    
    
    return "Hello, Flask!"

def startScanning():
    response = requests.post(printer_url + '/Scan/Jobs', data= '<scan:ScanJob xmlns:scan="http://www.hp.com/schemas/imaging/con/cnx/scan/2008/08/19" xmlns:dd="http://www.hp.com/schemas/imaging/con/dictionaries/1.0/"><scan:XResolution>300</scan:XResolution><scan:YResolution>300</scan:YResolution><scan:XStart>0</scan:XStart><scan:YStart>0</scan:YStart><scan:Width>2480</scan:Width><scan:Height>3508</scan:Height><scan:Format>Pdf</scan:Format><scan:CompressionQFactor>25</scan:CompressionQFactor><scan:ColorSpace>Color</scan:ColorSpace><scan:BitDepth>8</scan:BitDepth><scan:InputSource>Platen</scan:InputSource><scan:GrayRendering>NTSC</scan:GrayRendering><scan:ToneMap><scan:Gamma>0</scan:Gamma><scan:Brightness>1000</scan:Brightness><scan:Contrast>1000</scan:Contrast><scan:Highlite>0</scan:Highlite><scan:Shadow>0</scan:Shadow></scan:ToneMap><scan:ContentType>Document</scan:ContentType></scan:ScanJob>')
    print(response.status_code)
    
def getLatestJobNumber():
    response = requests.get(printer_url + "/Jobs/JobList")
    root = ET.fromstring(response.text)
    jobUrl = root[-1][0].text
    jobNumber = jobUrl.split('/')[-1]
    return jobNumber

@app.route("/download", methods=['GET'])
def mergePdf():
    merger = PdfMerger()
    
    inputFiles = pathlib.Path('scans/input')
    for item in inputFiles.iterdir():
        if item.is_file():
            print(item)
            merger.merge(0,item)
    
    merger.write("scans/output/result.pdf")
    merger.close()
    
    return send_file('scans/output/result.pdf',as_attachment=True)

@app.route("/clear", methods=['GET'])
def cleanInput():
    inputFiles = pathlib.Path('scans/input')
    for item in inputFiles.iterdir():
        if item.is_file():
            print(item)
            os.remove(item)
    return "remove done"