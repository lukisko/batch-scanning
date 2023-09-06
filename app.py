from flask import Flask, render_template, send_file
import xml.etree.ElementTree as ET
import requests
from PyPDF2 import PdfMerger
import pathlib
import os
import printer_config
from interfaces import printer_interface
from datetime import datetime

app = Flask(__name__)

printer_url = 'http://192.168.1.13'

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/print", methods=['GET'])
def scan():
    my_printer = printer_config.HP_officeJet_pro_9010
    jobNumber = my_printer.make_scan_job()
    
    response = my_printer.wait_and_get_scan(jobNumber)
    print(response.status_code)
    
    with open("scans/input/scan-"+ str(datetime.now()) +".pdf","wb") as bin_file:
        bin_file.write(response.content)
    
    return "Hello, Flask!"

@app.route("/download", methods=['GET'])
def mergePdf():
    merger = PdfMerger()
    
    inputFiles = pathlib.Path('scans/input')
    for item in sorted(inputFiles.iterdir(), reverse=True):
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

@app.route("/clearLast", methods=['GET'])
def cleanLastInput():
    inputFiles = pathlib.Path('scans/input')
    fileToRemove = max(inputFiles.iterdir())
    if fileToRemove.is_file():
        print(fileToRemove)
        os.remove(fileToRemove)
    return "remove done"