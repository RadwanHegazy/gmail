from users.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile

MAIL_BLACKLIST_WORDS = [
    # Financial scams
    'winner', 'won', 'prize', 'lottery', 'jackpot',
    'cash', 'money', 'dollars', '$$$', 'profit',
    'million', 'billion', 'thousands', '100k', 'rich',
    
    # Urgency words
    'urgent', 'immediate', 'act now', 'limited time', 'expires',
    
    # Free offers
    'free', 'discount', 'sale', 'offer', 'deal',
    'bonus', 'gift', 'exclusive',
    
    # Investment scams
    'investment', 'invest', 'stocks', 'crypto', 'bitcoin',
    'forex', 'trading', 'opportunity',
    
    # Suspicious content
    'password', 'account', 'verify', 'suspended', 'login',
    'security', 'update', 'bank', 'paypal',
    
    # Miracle promises
    'guarantee', 'guaranteed', 'promise', 'risk-free',
    'miracle', 'amazing', 'incredible', 'fantastic',
    
    # Adult content markers
    'adult', 'dating', 'singles', 'meet',
    
    # Aggressive words
    'kill', 'killer', 'die', 'death', 'hack',
    
    # Generic spam markers
    'click here', 'subscribe', 'unsubscribe', 'opt out',
    'bulk', 'mass', 'spam', 'advertisement'
]

MAIL_BLACKLIST_ATTCHMENTS = [
    "application/vnd.microsoft.portable-executable"
    "text/x-shellscript",
    "application/bat", 
    "application/x-bat"
    "application/javascript"
]

def is_body_safe(body: str) -> bool:
    """
    Check if an email body is safe (not spam) by analyzing blacklisted words.
    
    Args:
        body (str): The email body text to analyze
        
    Returns:
        bool: True if the email is safe, False if likely spam
        
    The method calculates a spam score based on the frequency of blacklisted words
    relative to the total word count in the email body.
    """
    if not body or not isinstance(body, str):
        return True
        
    # Split on whitespace and punctuation for more accurate word matching
    words = body.lower().split()
    total_words = len(words)
    
    if total_words == 0:
        return True
        
    # Count occurrences of blacklisted words
    spam_word_count = sum(1 for word in words if word in MAIL_BLACKLIST_WORDS)
    
    # Calculate spam ratio: (spam words / total words)
    spam_ratio = (spam_word_count / total_words) * 100
    
    # Email is considered spam if more than 5% of words are blacklisted
    return spam_ratio <= 5


def is_bypass_maximum_mails_per_day(user: User) -> bool:
    """
    Check if a user is not sending too many emails per day.
    
    Args:
        user (User): The user to check
        
    Returns:
        bool: True if user's email sending pattern is safe, False if exceeding limits
    """
    # Get count of emails sent by user in last 24 hours
    emails_today = User.objects.filter(
        sender = user,
        created_at__gte=datetime.now() - timedelta(days=1)
    ).count()
    
    # Return False if user sent more than 100 emails in 24 hours
    return emails_today <= 100


def is_user_safe(user : User) -> bool :
    """
        Check sender is spammed.
    """
    return user.is_spammed == False


def is_attachment_safe(attachments:list[int]) -> bool :
    if not any(attchments) :
        return True

    for attch in attachments :
        attch = Attachment.objects.get(id=attch)
        if attch.content_type in MAIL_BLACKLIST_ATTCHMENTS : 
            return False

    return True
