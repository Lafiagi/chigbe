import requests
from django.conf import settings


from celery import shared_task

base_url = "settings.MAILGUN_BASE_URL"
api_key = ("api", "settings.MAILGUN_API_KEY")
sender = "support@refinditems.com"


@shared_task
def send_account_activation_email(email, otp):
    to = email
    otp = otp
    body = f"Hi {email},  Use the code {otp} to verify your email address."
    email_subject = "Sakalist: Account verification email"
    mailing_data = {
        "from": sender,
        "to": to,
        "subject": email_subject,
        "text": body,
    }

    resp = requests.post(base_url, auth=api_key, data=mailing_data)


@shared_task
def send_onboarding_email(
    full_name: str, email: str, account_type: str, code: str = ""
):
    link = f"https://refinditems.com/verify/{code}"
    to = email
    body = f"Hi {full_name},  Congratulations on concluding the first step of your registration as a ReFind {account_type}. Please click on this link  {link} to complete your verification process on the web, to immediately start enjoying endless opportunities on ReFind."
    email_subject = "Sakalist: Account verification email"

    if account_type.lower() == "subscriber":
        body = f"Hi {full_name},  Congratulations on concluding the first step of your registration as a ReFind {account_type}. Thank you for chosing ReFind."
        email_subject = "Sakalist: Welcome To ReFind"

    mailing_data = {
        "from": sender,
        "to": to,
        "subject": email_subject,
        "text": body,
    }

    resp = requests.post(base_url, auth=api_key, data=mailing_data)


@shared_task
def send_authorization_otp_mail(to, otp):
    body = f"Hi {to} Use the OTP below to proceed your with the next action:{otp}."
    email_subject = "Sakalist: Authorization OTP"

    mailing_data = {
        "from": sender,
        "to": to,
        "subject": email_subject,
        "text": body,
    }

    requests.post(base_url, auth=api_key, data=mailing_data)


@shared_task
def send_forgot_password_email(to, otp):
    body = f"Hi  {to}, use {otp} to reset your password"
    email_subject = "Sakalist: Forgot Password email"

    mailing_data = {
        "from": sender,
        "to": to,
        "subject": email_subject,
        "text": body,
    }

    res = requests.post(base_url, auth=api_key, data=mailing_data)


@shared_task
def send_account_verified_email(to):
    body = f"Hi  {to}, your email has successfully been verified, you can now login to your account."
    email_subject = "Sakalist: Verification Sucessful"

    mailing_data = {
        "from": sender,
        "to": to,
        "subject": email_subject,
        "text": body,
    }

    requests.post(base_url, auth=api_key, data=mailing_data)


@shared_task
def send_update_password_succcess_email(to):
    body = f"Hi  {to}, your password has successfully been updated. You can now Login to your account."
    email_subject = "Sakalist: Password Change Sucessful"

    mailing_data = {
        "from": sender,
        "to": to,
        "subject": email_subject,
        "text": body,
    }
    requests.post(base_url, auth=api_key, data=mailing_data)


@shared_task
def send_account_contact_artisan_email(to, service, phone):
    body = f"""
Hi  {to}, Your request for {service} has been accepted. Kindly Contact the artisan on {phone} to proceed with negotiations.


Disclaimer: Ensure once negotiation is concluded and all parties agreed to their terms, all payments and other transactions must be completed on ReFind platform.
Anything contrary will not be the responsinility of ReFind or its parents company Starlite Infosec Services.
All liabilities will be incured by the subscriber."""

    email_subject = "Sakalist: Congratulations! Request Accepted"

    mailing_data = {
        "from": sender,
        "to": to,
        "subject": email_subject,
        "text": body,
    }

    requests.post(base_url, auth=api_key, data=mailing_data)


@shared_task
def send_account_reject_client_request(to, service):
    body = f"Hi  {to}, Your request for {service} has been Rejected. You can Login to your account to find other vetted and verified artisans."
    email_subject = "Sakalist: Sorry! Request Rejected"

    mailing_data = {
        "from": sender,
        "to": to,
        "subject": email_subject,
        "text": body,
    }

    requests.post(base_url, auth=api_key, data=mailing_data)


@shared_task
def send_reject_order_mail(to, product):
    body = f"Hi  {to}, Your Order for {product} has been Rejected. You can Login to your account to find other vetted and verified vendors with the same product."
    email_subject = "Sakalist: Sorry! Order Rejected"

    mailing_data = {
        "from": sender,
        "to": to,
        "subject": email_subject,
        "text": body,
    }

    requests.post(base_url, auth=api_key, data=mailing_data)


@shared_task
def send_order_confirmed_mail(to, product):
    body = f"Hi  {to}, Your order for {product} has been Confirmed."
    email_subject = "Sakalist: Congratulations! Order Confirmed"

    mailing_data = {
        "from": sender,
        "to": to,
        "subject": email_subject,
        "text": body,
    }

    requests.post(base_url, auth=api_key, data=mailing_data)


@shared_task
def send_account_schedule_email(to, service):
    body = f"Hi  {to}, Your request for {service} has been scheduled. Kindly Login to your ReFind dashboard and make payment to proceed."
    email_subject = "Sakalist: Congratulations! Start Date Scheduled"

    mailing_data = {
        "from": sender,
        "to": to,
        "subject": email_subject,
        "text": body,
    }

    requests.post(base_url, auth=api_key, data=mailing_data)


@shared_task
def send_proceed_to_work_email(to, service, amount, phone):
    body = f"Hi  {to}, Payment of {amount} has been made for {service}. Kindly Contact the client on {phone} to get more information."
    email_subject = "Sakalist: Congratulations! Payment Recieved"

    mailing_data = {
        "from": sender,
        "to": to,
        "subject": email_subject,
        "text": body,
    }

    requests.post(base_url, auth=api_key, data=mailing_data)


@shared_task
def send_service_request_email(
    to,
    service,
):
    body = f"Hi  {to}, There is a new request for  {service}. Kindly login to your dashboard to get more information and take further action."
    email_subject = "Sakalist: Service Request Notification"

    mailing_data = {
        "from": sender,
        "to": to, 
        "subject": email_subject,
        "text": body,
    }

    requests.post(base_url, auth=api_key, data=mailing_data)


@shared_task
def send_deposit_mail(to, full_name, amount):
    body = f"Hi  {full_name}, Sum of {amount} has been deposited into your account successfully. Thank you for chosing ReFind."
    email_subject = "Sakalist: Deposit Success"

    mailing_data = {
        "from": sender,
        "to": to,
        "subject": email_subject,
        "text": body,
    }

    requests.post(base_url, auth=api_key, data=mailing_data)


@shared_task
def send_withdrawal_mail(to, full_name, amount):
    body = f"Hi  {full_name}, Sum of {amount} has been Withrawn from your wallet account on ReFind to your bank account successfully. Thank you for chosing ReFind."
    email_subject = "Sakalist: Withdrawal Success"

    mailing_data = {
        "from": sender,
        "to": to,
        "subject": email_subject,
        "text": body,
    }

    requests.post(base_url, auth=api_key, data=mailing_data)


@shared_task
def send_order_mail(to, full_name):
    body = f"Hi  {full_name}, You have a new Order, Login to to process the order. Thank you for chosing ReFind."
    email_subject = "Sakalist: New Customer Order"

    mailing_data = {
        "from": sender,
        "to": to,
        "subject": email_subject,
        "text": body,
    }

    requests.post(base_url, auth=api_key, data=mailing_data)