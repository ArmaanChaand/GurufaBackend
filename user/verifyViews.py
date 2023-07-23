from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.http import HttpResponse
from .models import User

def send_verification_email(request, user):
    # Generate the verification link
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    domain = get_current_site(request).domain
    verification_link = reverse('verify_email', kwargs={'uidb64': uid, 'token': token})

    # Build the email subject and content
    subject = 'Verify your email address'
    message = render_to_string('verify_email.html', {
        'first_name': user.first_name,
        'email': user.email,
        'verification_link': f'http://{domain}{verification_link}',
    })

    # Send the email
    send_mail(subject, '', 'your_email@example.com', [user.email], html_message=message)

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_email_verified = True  # Update the user's status or perform any other desired action
        user.save()
        return HttpResponse('email_verification_successful')  # Redirect to a success page
    else:
        return HttpResponse('email_verification_failed')  # Redirect to a failure page


from twilio.rest import Client




def send_register_sms(user_phone_number):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    message = client.messages.create(
                        body="This is test SMS from Gurufa Kids.",
                        from_=str(settings.TWILIO_PHONE_NUMBER),
                        to=str(user_phone_number),
                    )
    print(message.sid)