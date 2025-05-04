from celery import shared_task
from users.models import User
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

    data['sender'] = User.objects.get(id=data['sender'])
    data['reciver'] = User.objects.get(id=data['reciver'])

    if is_body_safe(data.get('body')) and is_user_safe(data.get('sender')) and is_bypass_maximum_mails_per_day(data.get('sender')) and is_attachment_safe(data.get('attchments')): 
        data['status'] = MAIL_STATUS.okay.value
    else:
        data['status'] = MAIL_STATUS.spammed.value



    attachments = data.pop('attachments')
    real_time_data = data.copy()
    body = data.pop('body')
    model = Mail.objects.create(**data)
    model.set_body(body)

    for attch in attachments : 
        atch_model = Attachment.objects.get(id=attch)
        model.attachments.add(atch_model)

    model.save()

    if data['status'] == MAIL_STATUS.okay.value :
        serializer = ListMailSerializer(real_time_data)
        send_notification(
            to_user_id=real_time_data.get('reciver'),
            **serializer.data
        )