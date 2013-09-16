#!/usr/bin/python

import urllib2
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import os

class getIP():
    """This class will mail the users ip"""
    
    #Server-Settings to be used
    SSL = True #Connect with ssl?
    SERVER = "smtp.mail.yahoo.com"
    PORT = 465
        
    #Addresses to be used
    FROM_ADDR = ""
    TO_ADDR = ""
    
    #Login credentials
    LOGIN = FROM_ADDR
    PASS = ""
    
    #Subject of the eMail
    SUBJECT = "Raspberry IP Update"
    
    #Define error messages if a provider couldn't be reached
    CERROR = "Could not reach provider"
    
    #Color for errors in a HTML conform notation
    ERROR_COLOR = "red"
    
    #Trials if the delivery of the mail fails
    SMTP_TIMEOUT = 60 #seconds
    TIME_TO_WAIT = 60 #seconds
    MAX_SEND_TRIALS = 5
    
    #Dictionary with PROVIDERS and their addresses
    PROVIDERS = {
                 "dynDns" : "http://checkip.dyndns.org",
                 "wieIstMeineIp" : "http://wieistmeineip.de",
                 "eigeneIp" : "http://www.eigene-ip.de"
                 }
    
    """These settings should be changed. Proceed with caution"""
    
    #Define filename of the file in which IPS should be safed
    SCRIPT_LOCATION = os.path.join(os.path.abspath(os.curdir)) + "/" #Location where the script is executed
    FILENAME = SCRIPT_LOCATION + "ips.txt"
    DEVIDER = "#!!!#" #<- DO NOT CHANGE THIS, if you do not know what it does below line 80
    
    #Empty dictionary for IPS
    IPS = {}
    
    def refreshIps(self):
        for provider in self.PROVIDERS:
            
            #Try to reach the provider
            try:
                #Get the IP from the provider
                request = urllib2.urlopen(self.PROVIDERS[provider]).read()
                
                #Use regEx to find IP in the HTML, which you get back
                ip = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}", request)
            
            except:
                #Couldn't connect to the IP-Provider, send error message instead
                self.IPS[provider] = "<font color='" + self.ERROR_COLOR + "'>" + self.CERROR + "</font>"
            
            else:    
                #Add Ip to IPS
                self.IPS[provider] = ip[0]
    
    def compareAndHandleIp(self):
        """Check if the last IP is equal to the current one"""
        
        #Initialize some variables needed
        message = ""
        emailmessage = ""
        ipsChanged = False
        fileNotFound = False
                            
        #Try to open the ipFile and read it
        try:
            fileIps = {}
            with open(self.FILENAME) as f:
                for line in f:
                    (key,value) = line.split(self.DEVIDER);
                    fileIps[key] = value.replace("\n","") #Remove the newline
        
        except:
            #Couldn't open the file or something else went wrong
            fileNotFound = True
        
        else:    
            """
            If you were able to open the ipFile, compare IPs to current ones
            by getting data from ipFile
            """
            
            for provider, ip in fileIps.items():
                if (ip != self.IPS[provider]):
                    ipsChanged = True                    

                emailmessage += "<b>" + provider + "</b><br><i>" + self.IPS[provider] + "<br>"
                message += provider + self.DEVIDER + self.IPS[provider] + "\n" #Even though they might be the same, something somewhere changed
                                
        #If changes are needed      
        if ipsChanged:
            #File needs to be closed and reopened to replace it each time
            ipFile = open(self.FILENAME,"w")
            ipFile.write(message)
            ipFile.close()
            
            #Mail the message to the address you defined above
            ipClass.buildMessage(emailmessage) 

        #If the ipFile is not found, dump the PROVIDERS and IPS into message    
        if fileNotFound:
            
            emailmessage += "<font color='" + self.ERROR_COLOR + "'>"
            emailmessage += "Couldn't open " + self.FILENAME + " , but here are the IPs:\n"
            emailmessage += "</font>"
            
            #Connect the name of the provider with the returned IP
            for provider, ip in self.IPS.items():
                emailmessage += "<b>" + provider + "</b>" + "\n" + "<i>" + ip + "</i>" + "\n"
                
            #Mail the message to the address you defined above
            ipClass.buildMessage(emailmessage)
    
    def buildMessage(self,message):
        #This function will build the message, which is later send to the user
        
        #Define Subject, To and From for the eMail
        MESSAGE = MIMEMultipart('alternative')
        MESSAGE["subject"] = self.SUBJECT
        MESSAGE["To"] = self.TO_ADDR
        MESSAGE["FROM"] = self.FROM_ADDR
        
        message = message.replace("\n", "<br>")
        
        #Define message text as html
        MESSAGE_BODY = MIMEText(message,"html")
        
        #Attach message to eMail
        MESSAGE.attach(MESSAGE_BODY)
        
        self.mailIp(MESSAGE, 0)
                            
    
    def mailIp(self, MESSAGE, trials):
        #This function will mail the IP-Addresses to a specific eMail-Address
        
        try:
            #Connect to server
            if self.SSL:
                server = smtplib.SMTP_SSL(self.SERVER, self.PORT, self.SMTP_TIMEOUT)        #For non-SSL-use server = smtplib.SMTP(mailserver)
            else:
                server = server = smtplib.SMTP(self.SERVER, self.PORT, self.SMTP_TIMEOUT)
            #Login
            server.login(self.LOGIN, self.PASS)
        
            #Send eMail
            server.sendmail(self.FROM_ADDR, self.TO_ADDR, MESSAGE.as_string())
        
            #Close connection
            server.quit()
            
        except Exception:
            #If something fails try to call yourself again with the timeout set above
            if(trials < self.MAX_SEND_TRIALS):
                time.sleep(self.TIME_TO_WAIT)
                trials = trials + 1
                self.mailIp(MESSAGE, trials)
            else:
                print("I'll go to sleep. Maybe the zombie apocalypse hit")               


"""Class ends here"""

#Create new class instance 
ipClass = getIP()

#Get the new IPs from your providers
ipClass.refreshIps()

#Compare and handle the IPs you got
ipClass.compareAndHandleIp()
