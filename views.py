from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
import json
from web3 import Web3, HTTPProvider
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
import random
from datetime import datetime

global uname, email, contract, web3, document_list
#function to call contract
def getContract():
    global contract, web3
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'Evault.json' #evault contract file
    deployed_contract_address = '0x2EAe644E2C3B821Dc828a10DA255002456A09584' #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
getContract()

def readDoc():
    global document_list, contract
    document_list = []
    count = contract.functions.getDocumentCount().call()
    for i in range(0, count):
        doc_name = contract.functions.getName(i).call()
        doc_type = contract.functions.getType(i).call()
        desc = contract.functions.getDesc(i).call()
        belongs = contract.functions.getBelongs(i).call()
        address = contract.functions.getAddress(i).call()
        phone = contract.functions.getPhone(i).call()
        criminal = contract.functions.getCriminalRecord(i).call()
        uid = contract.functions.getUid(i).call()
        today_date = contract.functions.getDate(i).call()
        file = contract.functions.getFile(i).call()
        document_list.append([doc_name, doc_type, desc, belongs, address, phone, criminal, uid, today_date, file])
readDoc()

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def AdminLogin(request):
    if request.method == 'GET':
       return render(request, 'AdminLogin.html', {})

def AddDocument(request):
    if request.method == 'GET':
       return render(request, 'AddDocument.html', {})

def CheckVault(request):
    if request.method == 'GET':
       return render(request, 'CheckVault.html', {})

def AdminLoginAction(request):
    if request.method == 'POST':
        user = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        if user == 'admin' and password == 'admin':
            context= {'data':'Welcome '+user}
            return render(request, 'AdminScreen.html', context)
        else:
            context= {'data':'Invalid Login'}
            return render(request, 'AdminLogin.html', context)

def AddDocumentAction(request):
    if request.method == 'POST':
        global document_list, contract
        today = str(datetime.now())
        document = request.POST.get('t1', False)
        doc_type = request.POST.get('t2', False)
        desc = request.POST.get('t3', False)
        name = request.POST.get('t4', False)
        address = request.POST.get('t5', False)
        phone = request.POST.get('t6', False)
        criminal = request.POST.get('t7', False)
        uid = request.POST.get('t8', False)
        filename = request.FILES['t9'].name
        myfile = request.FILES['t9'].read()
        if os.path.exists('VaultApp/static/files/'+filename):
            os.remove('VaultApp/static/files/'+filename)
        with open('VaultApp/static/files/'+filename, 'wb') as file:
            file.write(myfile)
        file.close()
        document_list.append([document, doc_type, desc, name, address, phone, criminal, uid, today, filename])
        msg = contract.functions.saveDocument(document, doc_type, desc, name, address, phone, criminal, uid, today, filename).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
        context= {'data':'Document Details Added to Blockchain with below Transaction Details<br/><br/>'+str(tx_receipt)}
        return render(request, 'AddDocument.html', context) 

def DownloadAction(request):
    if request.method == 'GET':
        filename = request.GET.get('filename', False)
        with open("VaultApp/static/files/"+filename, "rb") as file:
            content = file.read()
        file.close()
        response = HttpResponse(content,content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename='+filename
        return response

def matchVault(arr, document, des, person, criminal, uid):
    flag = False
    doc = document.lower()
    des = des.lower()
    criminal = criminal.lower()
    uid = uid.lower()
    for i in range(len(arr)):
        if arr[i] in document or arr[i] in des or arr[i] in criminal or arr[i] in uid or arr[i] in person:
            flag = True
            break
    return flag        
        

def CheckVaultAction(request):
    if request.method == 'POST':
        global document_list, contract
        input_data = request.POST.get('t1', False)
        input_data = input_data.strip().lower()
        input_data = input_data.split(" ")
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Document Name</font></th>'
        output+='<th><font size=3 color=black>Document Type</font></th>'
        output+='<th><font size=3 color=black>Description</font></th>'
        output+='<th><font size=3 color=black>Document Belongs To</font></th>'
        output+='<th><font size=3 color=black>Address</font></th>'
        output+='<th><font size=3 color=black>Phone No</font></th>'
        output+='<th><font size=3 color=black>Criminal Record</font></th>'
        output+='<th><font size=3 color=black>UID No</font></th>'
        output+='<th><font size=3 color=black>Upload Date</font></th></tr>'
        for i in range(len(document_list)):
            arr = document_list[i]
            flag = matchVault(input_data, arr[0], arr[2], arr[3], arr[6], arr[7])
            if flag:
                output+='<tr><td><font size=3 color=black>'+arr[0]+'</font></td>'
                output+='<td><font size=3 color=black>'+arr[1]+'</font></td>'
                output+='<td><font size=3 color=black>'+str(arr[2])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(arr[3])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(arr[4])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(arr[5])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(arr[6])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(arr[7])+'</font></td>'
                output+='<td><font size=3 color=black>'+str(arr[8])+'</font></td></tr>'
        output+="</table><br/><br/><br/><br/><br/><br/>"
        context= {'data':output}
        return render(request, 'ViewVault.html', context)            
        

def ViewDocument(request):
    if request.method == 'GET':
        global document_list
        output = '<table border=1 align=center>'
        output+='<tr><th><font size=3 color=black>Document Name</font></th>'
        output+='<th><font size=3 color=black>Document Type</font></th>'
        output+='<th><font size=3 color=black>Description</font></th>'
        output+='<th><font size=3 color=black>Document Belongs To</font></th>'
        output+='<th><font size=3 color=black>Address</font></th>'
        output+='<th><font size=3 color=black>Phone No</font></th>'
        output+='<th><font size=3 color=black>Criminal Record</font></th>'
        output+='<th><font size=3 color=black>UID No</font></th>'
        output+='<th><font size=3 color=black>Upload Date</font></th>'
        output+='<th><font size=3 color=black>Download Document Data</font></th></tr>'
        for i in range(len(document_list)):
            arr = document_list[i]
            output+='<tr><td><font size=3 color=black>'+arr[0]+'</font></td>'
            output+='<td><font size=3 color=black>'+arr[1]+'</font></td>'
            output+='<td><font size=3 color=black>'+str(arr[2])+'</font></td>'
            output+='<td><font size=3 color=black>'+str(arr[3])+'</font></td>'
            output+='<td><font size=3 color=black>'+str(arr[4])+'</font></td>'
            output+='<td><font size=3 color=black>'+str(arr[5])+'</font></td>'
            output+='<td><font size=3 color=black>'+str(arr[6])+'</font></td>'
            output+='<td><font size=3 color=black>'+str(arr[7])+'</font></td>'
            output+='<td><font size=3 color=black>'+str(arr[8])+'</font></td>'
            output+='<td><a href=\'DownloadAction?filename='+str(arr[9])+'\'><font size=3 color=black>Click Here</font></a></td></tr>'
        output+="</table><br/><br/><br/><br/><br/><br/>"
        context= {'data':output}
        return render(request, 'AdminScreen.html', context)              
        
   
