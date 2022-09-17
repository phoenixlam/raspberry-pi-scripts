import socket
import fcntl
import struct
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import smtplib
import os
import datetime
from dotenv import load_dotenv
import requests
import json

class Util():
    def __init__(self):
        pass

    def get_uptime(self):
        uptime = os.popen('uptime -p').read()[:-1]
        return uptime

    def get_public_ip(self):
        response = requests.get('https://ifconfig.me')
        return response.text

    def get_ip_address(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            return socket.inet_ntoa(fcntl.ioctl(
                s.fileno(),
                0x8915,  # SIOCGIFADDR
                struct.pack('256s', bytes(ifname[:15], encoding='utf8'))
            )[20:24])
        except OSError as ex:
            return ''

    # Send email using gmail
    def send_email(self, from_email, to_email, app_password, subject, html):        
        host = 'smtp.gmail.com'
        port = 465
                
        #content_txt = 'mail body content'
        #attachment = 'test.png'

        ### Define email ###
        message = MIMEMultipart()
        # add From 
        message['From'] = Header(from_email)
        # add To
        message['To'] = Header(to_email)
        # add Subject
        message['Subject'] = Header(subject)
        # add content text
        message.attach(MIMEText(html, 'html', 'utf-8'))
        
        # add attachment
        #att_name = os.path.basename(attachment)
        #att1 = MIMEText(open(attachment, 'rb').read(), 'base64', 'utf-8')
        #att1['Content-Type'] = 'application/octet-stream'
        #att1['Content-Disposition'] = 'attachment; filename=' + att_name
        #message.attach(att1)
            
        ### Send email ###
        server = smtplib.SMTP_SSL(host, port) 
        server.login(from_email, app_password)
        server.sendmail(from_email, to_email, message.as_string()) 
        server.quit() 
        print('Sent email successfully')  

if __name__ == '__main__':
    # Collect info
    util = Util()
    public_ip = util.get_public_ip()

    ifnames = ['eth0', 'lo', 'wlan0'] # TODO add method for listing all interfaces
    ip_dict = {}
    for ifname in ifnames:
        ip = util.get_ip_address(ifname)
        ip_dict[ifname] = ip
        
    uptime = util.get_uptime()        

    # Prepare email
    load_dotenv()

    from_email   = os.getenv('FROM_EMAIL')
    to_email     = os.getenv('TO_EMAIL') # TODO support multi to
    app_password = os.getenv('APP_PASSWORD')

    now = datetime.datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M")
    subject = 'My Raspberry Pi information '+now_str
    
    html = '<!DOCTYPE html><html><head><title>'+subject+'</title></head><body>'
    html += 'Public IP: '+public_ip+'<br/><br/>'
    html += 'Private IPs: '+json.dumps(ip_dict)+'<br/><br/>'
    html += 'Uptime: '+uptime+'<br/><br/>'
    html += '</body></html>'

    util.send_email(from_email, to_email, app_password, subject, html)
        