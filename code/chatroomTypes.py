from typing import TypedDict

from datetime import datetime
from uuid import uuid4


class ConfirmationResponse(TypedDict):
    confirm: bool
    data: dict


class Activity(TypedDict):
    type: str
    timestamp: str
    details: dict


class NewUser(TypedDict):
    username: str
    email: str
    password: str

def newUserDefaultData(user:NewUser) -> dict:
    return {
        'user_uuid': str(uuid4()),
        'created_at': datetime.now().isoformat(),
        'last_login_at': None,
        'profile': {
            'displayName': user['username'],
            'bio': '',
            'avatar_url': None,
            'status': None,
            'custom_status': ''
        },
        'permissions': [],
        'blocked_users': [],
        'activity_log': []
        
    }, uuid4()

class User(TypedDict):
    class Profile(TypedDict):
        displayName: str
        bio: str
        avatar_url: str
        status: str
        custom_status: str
        
    user_uuid: str
    
    username: str
    email: str
    
    created_at: str
    last_login_at: str
    
    profile: Profile
    
    permissions: list[str]
    
    blocked_users: list[str]
    
    activity_log: list[Activity]


class Payload(TypedDict):
    authentication: str

class UserDisplayNameChangePayload(Payload):
    display_name: str
    
class UserEmailChangePayload(Payload):
    email: str
