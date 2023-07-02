'''
A class for accessing a gmail account
Requires proper auth tokens for oauth2 in an external directory
'''
__all__ = []

import datetime
import requests
import pytz
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from googleapiclient.errors import HttpError
import base64
from email.message import EmailMessage

__all__.append('GMailer')
class GMailer():

    def __init__(self,
                 credentials_path,
                 token_file='token.json',
                 credentials_file='credentials.json'):
        self.scopes = 'https://www.googleapis.com/auth/gmail.compose'
        creds = self.get_credentials_with_browser_flow(credentials_path, token_file, credentials_file)
        self.account = build('gmail', 'v1', http=creds.authorize(Http()))

    def get_credentials_with_browser_flow(self, credentials_path, token_file, credentials_file):
        '''Run authorization procedure. Use valid access token if it exists;
           otherwise, use refresh token to generate new access token.'''
        store = file.Storage('%s/%s'%(credentials_path, token_file))
        creds = store.get()
        print('creds exist' if creds else 'no creds exist')
        print('tokens invalid' if creds and creds.invalid else 'tokens valid')
        if not creds or creds.invalid:
            print('generating new tokens...')
            flow = client.flow_from_clientsecrets('%s/%s'%(credentials_path, credentials_file), self.scopes)
            creds = tools.run_flow(flow, store)
        return creds

    def get_labels(self, **kwargs):
        '''Return all labels for account'''
        try:
            label_result = self.account.users().labels().list(userId='me').execute()
            return label_result.get('labels', [])

        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f'An error occurred: {error}')
            return label_result.get('items', [])
        
    def create_draft(self, message, **kwargs):
        '''create an email draft'''
        try:
            if isinstance(message, str):
                raw_message = _message_text_to_b64(message)
            else:
                raw_message = _message_obj_to_b64(message)
            
            create_message = {
                'message': {
                    'raw': raw_message
                }
            }
            
            draft = self.account.users().drafts().create(userId="me",
                                                         body=create_message).execute()

            print(F'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')

        except HttpError as error:
            print(F'An error occurred: {error}')
            draft = None

        return draft
    
    def get_raw_draft(self, draft_id, **kwargs):
        return self.account.users().drafts().get(userId="me", id=draft_id, format='raw').execute()
    
    def get_draft(self, draft_id, format='raw', **kwargs):
        raw_draft = self.get_raw_draft(draft_id)
        if format=='string':
            raw_draft['message']['string'] = _message_b64_to_text(raw_draft['message']['raw'])
        return raw_draft

    
    def list_drafts(self, **kwargs):
        return self.account.users().drafts().list(userId="me", **kwargs).execute()
        
    def create_draft_from_template(self, template_id, replace_tuples=[], **kwargs):
        decoded_template = self.get_draft(template_id, format='string')
        new_message = decoded_template['message']['string']
        for rf, rt in replace_tuples:
            new_message = new_message.replace(rf, rt, 1)
        print(new_message)
        draft = self.create_draft(new_message)
        return draft
    
def _message_obj_to_b64(message):
    return base64.urlsafe_b64encode(message.as_bytes()).decode()

def _message_text_to_b64(message):
    return base64.urlsafe_b64encode(message.encode()).decode()

def _message_b64_to_text(message):
    return base64.urlsafe_b64decode(message.encode()).decode()


# def parse_gtime(dt_str, type='datetime'):
#     '''parses stupid google style datetime string'''
#     if type=='date':
#         return datetime.datetime.strptime(dt_str, '%Y-%m-%d')
#     # else, treat as datetime
#     if dt_str[-1] == 'Z': # UTC time
#         return datetime.datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S.%fZ')
#     else: # has UTC offset
#         c = dt_str.rfind(':') # have to remove final : in string :(
#         return datetime.datetime.strptime(dt_str[:c] + dt_str[c+1:], '%Y-%m-%dT%H:%M:%S%z').astimezone(pytz.utc).replace(tzinfo=None)
