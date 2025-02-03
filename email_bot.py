import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
import os

def send_email_with_attachment(from_emails, to_emails, subject,passwords):
    # Ensure to_emails is a list
    if isinstance(to_emails, str):
        to_emails = [email.strip() for email in to_emails.split(",")]

    # Ensure from_emails and passwords are lists
    for from_email,password in zip(from_email,passwords):
        
        # Send email to each recipient separately
        for to_email in to_emails:
            try:
                file_path = "" # Replace with the file path for your resume
                  
                # Check if file exists
                if not os.path.exists(file_path):
                    print(f"File not found: {file_path}")
                    return
                
                # Create the email
                msg = MIMEMultipart()
                msg['From'] = from_email
                msg['To'] = to_email  # Send to one recipient
                msg['Subject'] = subject
                
                # HTML body with bold text and change the content as per your requirement
                html_body =  f"""
            <html>
            <body>
                <p>Hi,</p>
                <p>
                    I hope this email finds you well. As I reflect on the <b>past ten years</b>, 
                    I am grateful for the opportunities and challenges that have shaped my career in IT.
                </p>
                <p>
                    This is <b>SaiKrishna</b>, and I am a <b>Java Full Stack Developer</b> presently working with <b>Barclays</b>. 
                    I am about to complete my contract with them and am open to new opportunities coming my way. 
                    Please take a look at my attached resume and keep me in mind for opportunities that match my skill set.
                </p>
                <p>
                    I have an employer and am willing to work on <b>C2C</b> or <b>C2H</b>.
                </p>
                <p>
                    I really hope you can help me find a new opportunity. I've attached my resume for your review.
                </p>
                <p>Best Regards,<br>
                   <b>Saikrishna</b>
                   <br></br> <!-- Repace it with your Designation-->
                   <br>P: </br> <!-- Repace it with your phone number -->
                   <br>
                   E:   <!--Repace it with your Email number -->
                </p>
            </body>
            </html>
            """
                
                # Attach the HTML body
                msg.attach(MIMEText(html_body, 'html'))
                  
                # Attach the file
                with open(file_path, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f"attachment; filename={os.path.basename(file_path)}")
                    msg.attach(part)

                # Gmail SMTP server details
                smtp_server = "smtp.gmail.com"
                smtp_port = 587

                # Create SMTP session
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()  # Enable encryption
                server.login(from_email, password)  # Login to the server

                # Send email
                server.sendmail(from_email, to_email, msg.as_string())
                server.quit()
                print(f"Email sent successfully from {from_email} to {to_email}!")

            except smtplib.SMTPRecipientsRefused as e:
                print(f"Error: Invalid recipient address {to_email}.")
                print(f"Details: {e}")
            except Exception as e:
                print(f"Error sending email from {from_email} to {to_email}: {e}")

if __name__ == "__main__":
    
    # Input details
    
    from_email = [""] #Repalce it with   your email id
    passwords = [""]      #get the App password not the gmail password
    to_emails =[""]          #Here add the mail id to which you want to send the mail with format ["mail1","mail2"]

    subject = "" #Replace it with the subject of the mail

    # Send the email
    send_email_with_attachment(from_email, to_emails, subject,passwords)
    print("All mails sent successfully")