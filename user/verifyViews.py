from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, OTP
from .serializers import userInfoSerializer
import random
from twilio.rest import Client


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
        'verification_link': f'https://{domain}{verification_link}',
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
        return redirect('https://gurufa.netlify.app/')
        # return redirect('http://localhost:5173/')
        # return HttpResponse('email_verification_successful')  # Redirect to a success page
    else:
        return redirect('https://gurufa.netlify.app/')
        # return redirect('http://localhost:5173/')
        # return HttpResponse('email_verification_failed')  # Redirect to a failure page





def sendOtpSMS(user_phone_number, otp):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)
    message = client.messages.create(
                        body=f"Your OTP phone verification from Gurufa Kids is {otp}",
                        from_=str(settings.TWILIO_PHONE_NUMBER),
                        to=str(user_phone_number),
                    )
    print(message.sid)


def generate_otp(user):
    otp_code = str(random.randint(1000, 9999))
    OTP.objects.create(user=user, otp_code=otp_code)
    return otp_code


def sendOTP(user):
    try:
        otp = generate_otp(user=user)
        sendOtpSMS(user_phone_number=user.phone_number,otp=otp)
        return otp
    except Exception as error:
        raise error

@api_view(['POST'])
def verify_phone(request):
    user = request.user
    otp_code = request.data.get('OTP')
    try:
        otp_instance = OTP.objects.get(user=user, otp_code=otp_code)
        user.is_phone_verified = True
        user.save()
        otp_instance.delete()
        return Response({'message': 'OTP verification successful.', 'user_data': userInfoSerializer(user).data}, status=status.HTTP_200_OK)
    except OTP.DoesNotExist:
        return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)


def send_password_reset_email(request):
    user = request.user
    # Generate the verification link
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    domain = get_current_site(request).domain
    verification_link = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})

    # Build the email subject and content
    subject = 'Reset Your Gurufa Password'
    message = render_to_string('reset_password_email.html', {
        'first_name': user.first_name,
        'email': user.email,
        'verification_link': f'https://{domain}{verification_link}',
    })

    # Send the email
    send_mail(subject, '', 'your_email@example.com', [user.email], html_message=message)