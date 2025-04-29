from users.models import User
from rest_framework_simplejwt.tokens import AccessToken
from uuid import uuid1
from mail.models import Mail


def create_user(
    username=None,
    email=None,
    password=None,
    full_name = "Test User"
) : 

    return User.objects.create_user(
        username = username if username else f"{uuid1()}",
        email = email if email else f"{uuid1()}@gmail.com",
        password = password if password else "password",
        full_name = full_name
    )

def create_mail(
    from_ = None,
    to = None,
    header = "Test Header",
    body = "Test Body".encode(),
    is_read = False,
    status = "okay"
) : 
    return Mail.objects.create(
            sender=from_ if from_ else create_user(),
            reciver=to if to else create_user(),
            header=header,
            body=body,
            is_read=is_read,
            status=status
        )

def create_tokens(user=None) : 
    return str(
        AccessToken.for_user(
            user = user if user else create_user()
        )
    )

def create_headers(user=None) : 
    return {
        'Authorization' : f"Bearer {create_tokens(user)}"
    }