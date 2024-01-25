from flask import Flask,request,jsonify
import pickle
import time
import pyodbc
import pyttsx3
from io import BytesIO
import threading
import requests   
import base64 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from reportlab.pdfgen import canvas
 
model=pickle.load(open("Crop.pkl","rb"))

app=Flask(__name__)
@app.route('/')
def home():
    return "hello madhav abuj"
@app.route('/abuj',methods=["POST"])
def abuj():
    #return "hello abuj"
    mail=request.get_json()
    return  "helo this from flask and your list is"


@app.route('/predict',methods=["POST"])
def predict ():
    n = request.form.get('n')
    p = request.form.get("p")
    k = request.form.get("k")
    t = request.form.get("t")
    h = request.form.get("h")
    ph = request.form.get("ph")
    r = request.form.get("r")

    
    result=model.predict([[n,p,k,t,h,ph,r]])[0]
    
    
    return jsonify(str(result))

@app.route('/send',methods=["POST"])
def send ():
    
    data=request.get_json()
    import time
    dd=time.strftime("%d%S%M")
    d=str(time.strftime("%Y:%m:%d"))
    billNO=str(f"Bill-{dd}.pdf")
    r=200
    ttt =200
    if r==200:
        file=gmail2().getvalue()

        url = 'https://test.cashfree.com/api/v1/order/create'
        payload = {
            'secretkey': 'TESTcd50758e5f12d998a4830fc25bd0bf3cc1cf9373',
            'appId': 'TEST10015268da56d11397ec76a4592086251001',

            "orderId": billNO,
            "orderAmount": ttt,
            "orderNote": "Test Order",
            "orderCurrency": "INR",
            "customerName": "John Doe",
            "customerPhone": "9876543614",
            "customerEmail":request.form.get('email'),
            "returnUrl": "https://cashfree.com",
            "notifyUrl": "http://example.com/notify"
        }

        response = requests.request('POST',url,data=payload)
        d=dict(response.json())

        sender_email = 'abujpatil059@gmail.com'
        receiver_email = 'madhavabuj139@gmail.com'
        subject = "Your Bill Recipt"
        body = f'''Thanks for comming
        For Making Payment ONLine Plse click on bilow link
                '''
        password = 'pvaqevyonvdialyg'
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        attachment = MIMEApplication(file,_subtype="pdf")
        attachment.add_header('Content-Disposition','attachment',filename=billNO)
        msg.attach(attachment)
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        return data
       
def gmail2 (*karg) :
      data=request.get_json()
      d2=[]
      #d2=request.get_json()
      dd=time.strftime("%d%S%M")
      date=str(time.strftime("%Y:%m:%d"))
      billNO=str(f"Bill-{dd}.pdf")
      billN=str(f"Bill-{dd}.")
   
      buf=BytesIO()
      c = canvas.Canvas(buf,pagesize=(200, 250), bottomup=0)
      c.setFillColorRGB(0.8, 0, 0.7)
      c.line(70, 22, 180, 22)
      c.line(5, 45, 195, 45)
      c.line(15, 120, 185, 120)
      c.line(35, 108, 35, 220)
      c.line(115, 108, 115, 220)
      c.line(135, 108, 135, 220)
      c.line(160, 108, 160, 220)
      c.line(15, 220, 185, 220)
      c.translate(10, 40)
      c.scale(1, -1)
      #c.drawImage(file_name, 0, 0, width=50, height=30)
      c.scale(1, -1)
      c.translate(-10, -40)
      c.setFont("Times-Bold", 10)
      c.drawCentredString(125, 20,"Hotel Kanayy" )
      c.setFont("Times-Bold", 5)
      c.drawCentredString(125, 30, "Solapur-Dhule Rode")
      c.drawCentredString(125, 35,  " Manjarsumbha")
      c.setFont("Times-Bold", 6)
      c.drawCentredString(125, 42, "GST No")
      c.setFont("Times-Bold", 8)
      c.drawCentredString(100, 55, "Hotell_Bill")
      c.setFont("Times-Bold", 5)
      c.drawRightString(70, 70, "Bill No. :")
      c.drawRightString(100, 70, billN)
      c.drawRightString(70, 80, "Date :")
      c.drawRightString(100, 80, date)
      c.drawRightString(70, 90, "Customer Name :")
      c.drawRightString(100, 90, "---")
      c.drawRightString(70, 100, "Phone No. :")
      c.drawRightString(100, 100, "97XXXXXX")
      c.roundRect(15, 108, 170, 130, 10, stroke=1, fill=0)
      c.drawCentredString(25, 118, "S.No.")
      c.drawCentredString(75, 118, "Orders")
      c.drawCentredString(125, 118, "Price")
      c.drawCentredString(148, 118, "Qty.")
      c.drawCentredString(173, 118, "Total")
   
   
      c.drawString(30, 230, "Thanks for coming!!")
   
   
   
      a=75
      b=108
      sr=0
      tot=0
      for i in d2:
          sr+=1
          b+=10
          c.drawCentredString(25, int(f"{b+10}"), f"{sr}")
          c.drawCentredString(75, int(f"{b+10}"), f"{i[0]}")
          c.drawCentredString(125, int(f"{b+10}"), f"{i[1]}")
          c.drawCentredString(148, int(f"{b+10}"), f"{i[2]}")
          c.drawCentredString(173, int(f"{b+10}"), f"{i[3]}")
          tot+=int(i[3])
      s=str(f'RS- {tot}')
      c.drawRightString(180, 228,s)
      c.showPage()
      c.save()
      buf.seek(0)
      return buf
      
   


if __name__ == "__main__":
    app.run(debug=True)
