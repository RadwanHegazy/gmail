from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from mail.models import Mail, MAIL_STATUS

@shared_task
def cleanup_deleted_mails():
    """
    Delete mails that have been in deleted state for more than 30 days
    """
    threshold_date = timezone.now() - timedelta(days=30)
    
    # Get all soft-deleted mails older than 30 days
    old_deleted_mails = Mail.objects.filter(
        status=MAIL_STATUS.deleted,
        datetime__lte=threshold_date
    )
    
    # Permanently delete these mails
    deletion_count = old_deleted_mails.delete()
    
    return f"Permanently deleted {deletion_count[0]} mails that were in trash for over 30 days"