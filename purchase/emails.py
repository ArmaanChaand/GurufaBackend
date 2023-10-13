from user.verifyViews import sendHtmlEmail

def sendBookingConfirmationMail(user_email, user_first_name,course_name, level_name, booking_id):
    """BOOKING CONFIRMATION EMAIL"""
    subject = 'Your booking has been confirmed.'
    context = {
        "first_name": user_first_name,
        "course_name": course_name,
        "level_name": level_name,
        "booking_id": booking_id
    }
    # Send the email
    sendHtmlEmail(subject=subject, recipient_list=[user_email], email_template_name='booking_confirmation.html', email_template_context=context)