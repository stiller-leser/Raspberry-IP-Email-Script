#Raspberry emails IP

This script should be added to the cronjobs to be executed in the interval you want.
For example if you would like the script to be executed every hour you should use
    0 */1 * * * python /path/to/script/getIP.py

##Setup needed

There are severl options within the script, that need to be configured once.

###First and foremost your email-settings:

* SSL = True / False -> Is your email-provider using a SSL-connection?
* SERVER = "smtp.example.com" -> The smtp-server of your provider
* PORT = "666" -> The port the provider's smtp-server is usin
* FROM_ADDR = "sendEmailFromHere@something.com" -> This address is going to be used to send the mail. The above configuration needs to be suitable for it
* TO_ADDR = "thisAccountReceivesEmail@something.com" -> The email is going to be send to this account
* LOGIN = FROM_ADDR -> Only change this if your provider does not use the email-address as login
* PASS = "secretPassword" -> The password for the FROM_ADDR goes here
* SUBJECT = "TheSubjectOfTheEmail" -> The email is going to have this subject
* CERROR = "ERROR" -> This error-message will show up in the email if one provider couldn't be reached
* ERROR_COLOR = "red" -> Color for CERROR-text in HTML-Notation
* SMTP_TIMEOUT = 60 -> If there is a problem with the email-server the script is going to wait x-seconds before the connection is closed
* TIME_TO_WAIT = 60 -> If this has happened, we are going to wait a certain time and send the mail again, or at least try
* MAX_SEND_TRIALS = 5 -> How often are we going to try to send the mail?
* PROVIDERS = {} -> Here you could add an website where you get you're IP is shown. Needs to be the full address of this site

