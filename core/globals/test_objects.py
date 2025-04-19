from users.models import User
from rest_framework_simplejwt.tokens import AccessToken
from uuid import uuid4, uuid1

def create_user(
    username=None,
    email=None,
    password=None
) : 

    return User.objects.create_user(
        username = username if username else f"{uuid1()}",
        email = email if email else f"{uuid1()}@gmail.com",
        password = password if password else "password",
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