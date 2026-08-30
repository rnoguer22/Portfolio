import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from config import SMTP_SERVER, SMTP_PORT, EMAIL, EMAIL_PASSWD



# Function to send an OTP verification code to the user's email 
def send_email_verification(user_email: str, code: str):
    try:
        # We define the MIME message structure
        message = MIMEMultipart("alternative")
        message["Subject"] = "Verification Code - rnoguer's Portfolio"
        message["From"] = EMAIL 
        message["To"] = user_email

        text = f"Your verification code is {code}"
        html = f"""
        <html>
          <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
            <div style="max-width: 500px; background: #ffffff; padding: 30px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); margin: auto;">
              <h2 style="color: #2563eb; text-align: center;">Access verification</h2>
              <p style="color: #333333; font-size: 16px;">You have requested to access or synchronise your user session with this email in rnoguer's Portfolio App.</p>
              <p style="color: #333333; font-size: 16px;">Use this code to get access:</p>
              <div style="background: #eff6ff; border: 2px dashed #2563eb; padding: 15px; text-align: center; font-size: 28px; font-weight: bold; color: #1d4ed8; letter-spacing: 5px; border-radius: 8px; margin: 20px 0;">
                {code}
              </div>
              <p style="color: #666666; font-size: 14px; text-align: center;">If you have not requested this code, you can ignore this message.</p>
            </div>
          </body>
        </html>
        """
        # Inyect both text and html to the message 
        message.attach(MIMEText(text, "plain"))
        message.attach(MIMEText(html, "html"))

        # SMTP Google connection and secure login with TLS 
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL, EMAIL_PASSWD)
            server.sendmail(EMAIL, user_email, message.as_string())
        
        print(f"Verification email sent successfully to the user: {user_email}")
        return True
    
    except Exception as e:
        print(f"There has been a problem sending the verificacion email: {e}")
        return False 
