import datetime

from celery import shared_task
from .models import Loan
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_loan_notification(loan_id):
    try:
        loan = Loan.objects.get(id=loan_id)
        member_email = loan.member.user.email
        book_title = loan.book.title
        send_mail(
            subject='Book Loaned Successfully',
            message=f'Hello {loan.member.user.username},\n\nYou have successfully loaned "{book_title}".\nPlease return it by the due date.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[member_email],
            fail_silently=False,
        )
    except Loan.DoesNotExist:
        pass


def check_overdue_loans():
    today_date = datetime.datetime.now()
    overdue_loans = Loan.objects.filter(is_returned=False, due_date__lt=today_date)
    overdue_members = []

    for loan in overdue_loans:
        send_mail(
            subject='Over due book loan',
            message=f"Hello {loan.member.user.username},\n\nYour book titled {loan.book.title} is due for return",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=loan.member,
            fail_silently=False,
        )

