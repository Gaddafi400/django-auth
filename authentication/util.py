from django.core.mail import send_mail
from django.core.mail import EmailMessage

from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_welcome_email(from_email: str, user_email: str, subject: str, message: str) -> None:
    """
    Sends a email to the user.

    Parameters:
    - from_email (str): The email address from which the email will be sent.
    - user_email (str): The email address of the recipient user.
    - subject (str): The subject of the email.
    - message (str): The body/content of the email.

    Returns:
    - None
    """
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=True)


def send_confirmation_email(from_email: str, user_email: str, subject: str, message: str) -> None:
    """
    Sends an email to the user.

    Parameters:
    - from_email (str): The email address from which the email will be sent.
    - user_email (str): The email address of the recipient user.
    - subject (str): The subject of the email.
    - message (str): The body/content of the email.

    Returns:
    - None
    """
    email = EmailMessage(subject, message, from_email, [user_email])
    email.send(fail_silently=True)


def send_activation_email(request, email, username, uid, token):
    # Build the activation link URL
    domain = request.get_host()
    activation_link = f"http://{domain}{reverse('authentication:activate', kwargs={'uidb64': uid, 'token': token})}"

    # Load the email template
    email_subject = 'Account Activation'
    email_template = 'authentication/email_confirmation.html'

    # Render the email template with the required context
    email_html = render_to_string(email_template,
                                  {'domain': domain,
                                   'username': username,
                                   'uid': uid,
                                   'token': token,
                                   'activation_link': activation_link
                                   })
    email_text = strip_tags(email_html)  # Strip HTML tags to get plain text version

    # Create the EmailMultiAlternatives object
    from_email = 'your_email@example.com'  # Replace with your desired "from" email address
    email_message = EmailMultiAlternatives(email_subject, email_text, from_email, to=[email])
    email_message.attach_alternative(email_html, 'text/html')  # Attach HTML version of the email template

    # Send the email (fail silently)
    try:
        email_message.send()
    except Exception:
        pass  # Fail silently, without raising an exception
