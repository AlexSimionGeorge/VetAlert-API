from django.core.mail import send_mail
from django.conf import settings

class MailerService:
    @staticmethod
    def send_signup_email(email):
        """
        Sends an email to the given email address with the subject "VetAlert".

        :param email: The recipient's email address
        """
        subject = "VetAlert"
        message = "You have just signed up to VetAlert."
        from_email = settings.DEFAULT_FROM_EMAIL

        try:
            send_mail(subject, message, from_email, [email])
            return True
        except Exception as e:
            # Log the error if needed
            print(f"Error sending email: {e}")
            return False
