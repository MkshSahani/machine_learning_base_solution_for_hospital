import smtplib
from email.mime.text import MIMEText


def mail_function(toaddr, body):
	msg = MIMEText(body,"html")
	subject = "The message of the patient............".title()
	msg['From'] = "mkshsahani852@gmail.com"
	msg['To'] = toaddr
	msg['Subject'] = subject
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login("youmail@address.com","password") # update this line to send mail. 
	server.send_message(msg)
	print("send the message........")
	server.quit()


if __name__ == "__main__":
	data = ''' this is testing mail setup '''
	mail_function("msco18333@gmail.com", data)
