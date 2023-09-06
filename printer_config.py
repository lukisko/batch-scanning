from flask import Flask, render_template, send_file
import xml.etree.ElementTree as ET
import requests
from PyPDF2 import PdfMerger
import pathlib
import os
from interfaces import printer_interface

printer_url = 'http://192.168.1.13'

class HP_officeJet_pro_9010(printer_interface):
    def make_scan_job() -> str:
        startScanning()
        jobNumber = getLatestJobNumber()
        return jobNumber
    
    def wait_and_get_scan(job_id) -> requests.Response:
        received_request = requests.get(printer_url + '/eSCL/ScanJobs/'+ str(job_id) +'/NextDocument')
        return received_request
    
def startScanning():
    response = requests.post(printer_url + '/eSCL/ScanJobs', data= '<scan:ScanSettings xmlns:scan="http://schemas.hp.com/imaging/escl/2011/05/03" xmlns:copy="http://www.hp.com/schemas/imaging/con/copy/2008/07/07" xmlns:dd="http://www.hp.com/schemas/imaging/con/dictionaries/1.0/" xmlns:dd3="http://www.hp.com/schemas/imaging/con/dictionaries/2009/04/06" xmlns:fw="http://www.hp.com/schemas/imaging/con/firewall/2011/01/05" xmlns:scc="http://schemas.hp.com/imaging/escl/2011/05/03" xmlns:pwg="http://www.pwg.org/schemas/2010/12/sm"><pwg:Version>2.1</pwg:Version><scan:Intent>Document</scan:Intent><pwg:ScanRegions><pwg:ScanRegion><pwg:Height>3507</pwg:Height><pwg:Width>2481</pwg:Width><pwg:XOffset>0</pwg:XOffset><pwg:YOffset>0</pwg:YOffset></pwg:ScanRegion></pwg:ScanRegions><pwg:InputSource>Platen</pwg:InputSource><scan:DocumentFormatExt>application/pdf</scan:DocumentFormatExt><scan:XResolution>300</scan:XResolution><scan:YResolution>300</scan:YResolution><scan:ColorMode>RGB24</scan:ColorMode><scan:CompressionFactor>35</scan:CompressionFactor><scan:Brightness>1000</scan:Brightness><scan:Contrast>1000</scan:Contrast></scan:ScanSettings>')
    print(response.status_code)

def getLatestJobNumber():
    response = requests.get(printer_url + "/eSCL/ScannerStatus")
    root = ET.fromstring(response.text)
    jobUrl = root[3][0][1].text # TODO change this in future for looking into tags directly
    jobNumber = jobUrl
    print('job id:',jobNumber)
    return jobNumber