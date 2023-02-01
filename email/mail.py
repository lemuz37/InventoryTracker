import smtplib
from email.message import EmailMessage

EMAIL_ADDRESS = 'devicetrackingemail@gmail.com'
EMAIL_PASSWORD = 'gvzvgujxuaytxswf'

msg = EmailMessage()
msg['Subject'] = "Calibration Due in One Month"
msg['From'] = EMAIL_ADDRESS
msg['To'] = EMAIL_ADDRESS
msg.set_content('Test Email')

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())