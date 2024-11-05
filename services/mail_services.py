import requests
from django.conf import settings

from background_task import background
from celery import shared_task


class MailSender:
    def __init__(self, email, otp=None):
        self.base_url = settings.MAILGUN_BASE_URL
        self.api_key = ("api", settings.MAILGUN_API_KEY)
        self.sender = settings.MAILGUN_SENDER
        self.to = email
        self.otp = otp
    
    @shared_task
    def send_account_activation_email(self):

        body = "Hi " + self.to + " Use the OTP below to verify your email \n" + self.otp
        email_subject = "sakalist: Account verification email"

        mailing_data = {
            "from": self.sender,
            "to": self.to,
            "subject": email_subject,
            "text": body,
        }

        requests.post(self.base_url, auth=self.api_key, data=mailing_data)

    @shared_task
    def send_authorization_otp_mail(self):
        body = f"Hi {self.to} Use the OTP below to proceed your with the next action:{self.otp}"
        email_subject = "sakalist: Authorization OTP"

        mailing_data = {
            "from": self.sender,
            "to": self.to,
            "subject": email_subject,
            "text": body,
        }

        requests.post(self.base_url, auth=self.api_key, data=mailing_data)     
   
    @shared_task
    def send_forgot_password_email(self):
        forgot_pass_url = f"https://sakalist.ng/changepass/{self.otp}"
        body = f"Hi  {self.to}  follow the link below to change your password {forgot_pass_url}"
        email_subject = "sakalist: Forgot Password email"

        mailing_data = {
            "from": self.sender,
            "to": self.to,
            "subject": email_subject,
            "text": body,
        }

        res = requests.post(self.base_url, auth=self.api_key, data=mailing_data)
        print(f"Our response data is:{res.json()}")
    
    @shared_task
    def send_account_verified_email(self):
        login_url = "https://sakalist.ng/login/"
        body = f"Hi  {self.to}, your email has successfully been verified follow the link below to login to your account {login_url}"
        email_subject = "sakalist: Verification Sucessful"

        mailing_data = {
            "from": self.sender,
            "to": self.to,
            "subject": email_subject,
            "text": body,
        }

        requests.post(self.base_url, auth=self.api_key, data=mailing_data)
    
    @shared_task
    def send_update_password_succcess_email(self):
        login_url = "https://sakalist.ng/login/"
        body = f"Hi  {self.to}, your password has successfully been updated"
        email_subject = "sakalist: Password Change Sucessful"

        mailing_data = {
            "from": self.sender,
            "to": self.to,
            "subject": email_subject,
            "text": body,
        }
        requests.post(self.base_url, auth=self.api_key, data=mailing_data)