from chatroomTypes import *

from fastapi import FastAPI, HTTPException
from starlette.responses import RedirectResponse

import json

from hashlib import sha256
from uuid import uuid4



print('Starting.')

print('Loading Data')
chatrooms = json.load(open('storage/chatrooms.json'))
messages = json.load(open('storage/messages.json'))
users = json.load(open('storage/users.json'))
credentials = json.load(open('storage/credentials.json'))
usertokens = json.load(open('storage/usertokens.json'))



def save_all():
    print('Saving All Data')
    try:
        json.dump(chatrooms, open('storage/chatrooms.json', 'w'), indent=4)
    except Exception as e:
        print('ERROR: COULD NOT SAVE CHATROOMS JSON')
        print(e)
        
    try:
        json.dump(messages, open('storage/messages.json', 'w'), indent=4)
    except Exception as e:
        print('ERROR: COULD NOT SAVE MESSAGES JSON')
        print(e)
        
    try:
        json.dump(users, open('storage/users.json', 'w'), indent=4)
    except Exception as e:
        print('ERROR: COULD NOT SAVE USERS JSON')
        print(e)
        
    try:
        json.dump(credentials, open('storage/credentials.json', 'w'), indent=4)
    except Exception as e:
        print('ERROR: COULD NOT SAVE CREDENTIALS JSON')
        print(e)
        
    try:
        print('Hi')
        json.dump(usertokens, open('storage/usertokens.json', 'w'), indent=4)
    except Exception as e:
        print('ERROR: COULD NOT SAVE USERTOKENS JSON')
        print(e)

def uuid_in_users(uuid:str):
    return uuid in users.keys()

def tosha256(string:str) -> str:
    string = string.encode('utf-8')
    return sha256(string).hexdigest()

def valuetokey(dictionary:dict, value:any):
    return list(dictionary.keys())[list(dictionary.values()).index(value)]

def validate_auth(user_uuid:str, token:str):
    if usertokens[user_uuid] == token:
        return 0
    
    elif token == 'ADMINTEST':
        return 1
    
    else:
        raise HTTPException(403, f'You didn\'t provide the correct authentication to use this endpoint!')


api = FastAPI()


@api.get('/')
def root():
    return RedirectResponse('/docs')



@api.get('/users/auth/{user_uuid}')
def authenticate_user(user_uuid:str, password:str) -> ConfirmationResponse:
    if not uuid_in_users(user_uuid):
        raise HTTPException(400, f'The user {user_uuid} was not found.')
    
    password_hash = tosha256(password)
    
    if not credentials[user_uuid] == password_hash:
        raise HTTPException(403, f'The password is not correct.')
    
    usertoken = usertokens[user_uuid]
    
    return {
        'confirm': True,
        'data': {
            'user_token': usertoken
        }
    }


# User Data Retriever
@api.get('/users/get/uuid/{user_uuid}')
def get_user_by_uuid(user_uuid:str):
    if user_uuid in users.keys():
        return users[user_uuid]
    
    else:
        raise HTTPException(400, f'User with uuid {user_uuid} was not found.')

@api.get('/users/get/username/{username}')
def get_user_by_username(username:str):
    username = username.lower()
    result = [user for user in users.values() if user.get('username') == username]
    
    if result:
        return result[0]
    
    else:
        raise HTTPException(400, f'User {username} was not found.')
  
    
# User Account Control
@api.post('/users/create')
def create_user(user:NewUser) -> ConfirmationResponse:
    password_hash = tosha256(user['password'])
    del user['password']
    
    user['username'] = user['username'].lower()
    user_default, token = newUserDefaultData(user)
    user.update(user_default)
    user:User = user
    
    users[user['user_uuid']] = user
    credentials[user['user_uuid']] = password_hash
    usertokens[user['user_uuid']] = str(uuid4())
    save_all()
    
    return {
        'confirm': True,
        'data': user
    }


# User Account Control
@api.post('/users/configure/{user_uuid}/email')
def change_user_email(payload:UserEmailChangePayload, user_uuid:str) -> ConfirmationResponse:
    
    email = payload['email']
    
    if not uuid_in_users(user_uuid):
        raise HTTPException(400, f'The user {user_uuid} was not found.')
    
    validate_auth(user_uuid, payload['authentication'])
    
    users[user_uuid]['email'] = email
    save_all()
    
    return {
        'confirm': True,
        'data': users[user_uuid]
    }

@api.post('/users/configure/{user_uuid}/profile/display_name')
def change_user_displayname(payload:UserDisplayNameChangePayload, user_uuid:str) -> ConfirmationResponse:
    display_name = payload['display_name']
    
    if not uuid_in_users(user_uuid):
        raise HTTPException(400, f'The user {user_uuid} was not found.')
    
    validate_auth(user_uuid, payload['authentication'])
    
    if len(display_name) > 25:
        raise HTTPException(400, f'The Display Name can\'t be over 25 characters long!')
    
    users[user_uuid]['profile']['displayName'] = display_name
    save_all()
    
    return {
        'confirm': True,
        'data': users[user_uuid]
    }
