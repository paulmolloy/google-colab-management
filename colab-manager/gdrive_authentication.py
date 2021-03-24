from pathlib import Path
from pydrive.drive import GoogleDrive
import os.path


import httplib2
import json
import webbrowser
import socket

from oauth2client import GOOGLE_REVOKE_URI, GOOGLE_TOKEN_URI, client
from oauth2client.client import GoogleCredentials
from oauth2client.tools import ClientRedirectHandler
from oauth2client.tools import ClientRedirectServer
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


import json
import sys

'''
JS Origins:
http://localhost:8080
Note to self Authorized Redirect URIs:
http://localhost:8080/

'''
sys.path.insert(1, '../../google-auth-library-python-oauthlib')


client_secrets_path = os.path.expanduser(
    '~/secrets/private_client_secrets.json')

creds_path = 'creds.txt'

GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = client_secrets_path


class AuthError(Exception):
    """Base error for authentication/authorization errors."""


class InvalidCredentialsError(IOError):
    """Error trying to read credentials file."""


class AuthenticationRejected(AuthError):
    """User rejected authentication."""


class AuthenticationError(AuthError):
    """General authentication error."""


class RefreshError(AuthError):
    """Access token refresh error."""


# Based on the PyDrive one.
def CustomLocalWebserverAuth(authorize_url, host_name='localhost',
                             port_numbers=None):
    """Authenticate and authorize from user by creating local web server and
    retrieving authentication code.
    This function is not for web server application. It creates local web server
    for user from standalone application.
    :param host_name: host name of the local web server.
    :type host_name: str.
    :param port_numbers: list of port numbers to be tried to used.
    :type port_numbers: list.
    :returns: str -- code returned from local web server
    :raises: AuthenticationRejected, AuthenticationError
    """
    if port_numbers is None:
        port_numbers = [8080, 8090]  # Mutable objects should not be default
        # values, as each call's changes are global.
    success = False
    port_number = 0
    for port in port_numbers:
        port_number = port
        try:
            httpd = ClientRedirectServer(
                (host_name, port), ClientRedirectHandler)
        except socket.error as e:
            pass
        else:
            success = True
            break
    if success:
        oauth_callback = 'http://%s:%s/' % (host_name, port_number)
    else:
        print('Failed to start a local web server. Please check your firewall')
        print('settings and locally running programs that may be blocking or')
        print('using configured ports. Default ports are 8080 and 8090.')
        raise AuthenticationError()
    #webbrowser.open(authorize_url, new=1, autoraise=True)
    webbrowser.open_new_tab(authorize_url)
    print('Your browser has been opened to authorize access to your Google Drive Colab:')
    print()
    print('    ' + authorize_url)
    print()
    httpd.handle_request()
    if 'error' in httpd.query_params:
        print('Authentication request was rejected')
        raise AuthenticationRejected('User rejected authentication')
    if 'code' in httpd.query_params:
        return httpd.query_params['code']
    else:
        print('Failed to find "code" in the query parameters of the redirect.')
        print('Try command-line authentication')
        raise AuthenticationError('No code found in redirect')


def drive_auth():
    gauth = GoogleAuth()
    # Try to load saved client credentials
    #gauth.client_config_file = client_secrets_path
    print(gauth.client_config)

    if(os.path.exists(creds_path)):
        gauth.LoadCredentialsFile(creds_path)
    if gauth.credentials is None:
        with open(client_secrets_path) as f:
            data = json.load(f)
            data = data['web']
            print(data)
            client_id = data['client_id']
            client_secret = data['client_secret']
            redirect_ris = data['redirect_uris']
            auth_uri = data['auth_uri']
            '''
            gauth.client_config['client_id']=client_id
            gauth.client_config['client_secret']=client_secret
            #gauth.client_config['redirect_uris']=redirect_uris
            gauth.client_config['auth_uri']=auth_uri
            gauth.client_config['access_type']='offline'
            '''

            # print(gauth.client_config)
            # Authenticate if they're not there
            url = "https:www.google.com"
            #webbrowser.open_new_tab(url)
            auth_url = gauth.GetAuthUrl()
            # Create authentication url user needs to visit
            code = CustomLocalWebserverAuth(auth_url)
            # Your customized authentication flow
            gauth.Auth(code)  # Authorize and build service from the code
            #gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile(creds_path)

    print(gauth.credentials)
    drive = GoogleDrive(gauth)

    return drive

def colab_gdrive_auth():
    client_id = ''
    client_secret = ''
    refresh_token = ''
    with open(client_secrets_path) as f:
        data = json.load(f)
        data = data['web']
        print(data)
        client_id = data['client_id']
        client_secret = data['client_secret']
        #refresh_token = data['refresh_token']

        #client_id,client_secret, refresh_token
        print(' client_id: ' + client_id)
        print(' client_secret: ' + client_secret)
        #print(' refresh_token: ' + refresh_token)

    auth_key = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token
    }
    userid = 'molloyp1@tcd.ie'

    credentials = client.OAuth2Credentials(
        access_token=None,
        client_id=auth_key['client_id'],
        client_secret=auth_key['client_secret'],
        # refresh_token=auth_key['refresh_token'],
        token_expiry=None,
        token_uri=GOOGLE_TOKEN_URI,
        user_agent=None,
        revoke_uri=GOOGLE_REVOKE_URI)

    credentials.refresh(httplib2.Http())
    credentials.authorize(httplib2.Http())
    cred = json.loads(credentials.to_json())
    cred['type'] = 'authorized_user'

    with open('adc.json', 'w') as outfile:
        json.dump(cred, outfile)

        auth.authenticate_user()
        gauth = GoogleAuth()
        gauth.credentials = credentials
        drive = GoogleDrive(gauth)
