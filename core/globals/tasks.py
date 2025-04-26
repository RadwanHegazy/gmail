from celery import shared_task
from mail.models import Mail, MAIL_STATUS, Attachment
from dj_notification.notify import send_notification
from mail.apis.serializers import ListMailSerializer
from .spam_detector import (
    is_body_safe,
    is_user_safe,
    is_bypass_maximum_mails_per_day,
    is_attachment_safe
)


@shared_task
def check_before_send (**kwargs) -> None :
    """
        - For check if the mail is spammed or not.

        - Args : 
            - Mail Data
        - rType : 
            - None
    """
    data = kwargs

    if is_body_safe(data.get('body')) and is_user_safe(data.get('sender')) and is_bypass_maximum_mails_per_day(data.get('sender')) and is_attachment_safe(data.get('attchments')): 
        data['status'] = MAIL_STATUS.okay
    else:
        data['status'] = MAIL_STATUS.spammed



    attachments = data.pop('attchments')
    real_time_data = data.copy()
    body = data.pop('body')
    model = Mail.objects.create(**data)
    model.set_body(body)

    for attch in attachments : 
        atch_model = Attachment.objects.create(file=attch)
        atch_model.save()
        model.attachments.add(atch_model)

    model.save()

    if data['status'] == MAIL_STATUS.okay :
        serializer = ListMailSerializer(real_time_data)
        send_notification(
            to_user_id=real_time_data.get('reciver'),
            **serializer.data
        )