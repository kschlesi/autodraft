'''
A class for creating draft emails in a gmail account
Requires proper auth tokens for oauth2 in an external directory
'''
__all__ = []

import datetime
import requests
import pytz
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

__all__.append('DraftWriter')
class DraftWriter():

    def __init__(self,
                 credentials_path,
                 token_file='token.json',
                 credentials_file='credentials.json'):
        self.scopes = 'https://www.googleapis.com/auth/gmail.readonly'
        creds = self.get_credentials_with_browser_flow(credentials_path, token_file, credentials_file)
        self.account = build('gmail', 'v1', http=creds.authorize(Http()))

    def get_credentials_with_browser_flow(self, credentials_path, token_file, credentials_file):
        '''Run authorization procedure. Use valid access token if it exists;
           otherwise, use refresh token to generate new access token.'''
        store = file.Storage('%s/%s'%(credentials_path, token_file))
        creds = store.get()
        print('creds exist' if creds else 'no creds exist')
        print('tokens invalid' if creds.invalid else 'tokens valid')
        if not creds or creds.invalid:
            print('generating new tokens...')
            flow = client.flow_from_clientsecrets('%s/%s'%(credentials_path, credentials_file), self.scopes)
            creds = tools.run_flow(flow, store)
        return creds

    def get_labels(self, **kwargs):
        '''Return all labels for account'''
        try:
            label_result = self.account.users().labels().list(userId='me').execute()
            labels = label_result.get('labels', [])

            if not labels:
                print('No labels found.')
                return
            print('Labels:')
            for label in labels:
                print(label['name'])

        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            print(f'An error occurred: {error}')
            return label_result.get('items', [])

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
