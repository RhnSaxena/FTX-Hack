import uuid
import os
# import pythoncom


from generateReport.cloud import upload_to_S3
from docxtpl import DocxTemplate
from docx2pdf import convert

def createDocx(context,file_name):
    doc = DocxTemplate("template.docx")
    doc.render(context)
    doc.save(file_name)

def createReport(data,fileName):
    print(1)
    createDocx(data,"{file}.{extention}".format(file=fileName,extention="docx"))
    print(2)
    pythoncom.CoInitialize()
    convert("{file}.{extention}".format(file=fileName,extention="docx"))
    print(31)
    response=upload_to_S3(fileName, "pdf")
    os.remove("{file}.{extention}".format(file=fileName,extention="docx"))
    os.remove("{file}.{extention}".format(file=fileName,extention="pdf"))
    print(4)
    
    if(response["success"] is True):
        return response["message"]
    else: 
        return response["message"]

    