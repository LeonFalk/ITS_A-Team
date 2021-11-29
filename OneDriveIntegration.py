# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 12:05:29 2021

@author: Leon
"""

import onedrivesdk
from onedrivesdk.helpers import GetAuthCodeServer

redirect_uri = 'http://localhost:8080/'
client_secret = '2e1eacd6-8913-4c70-a47f-0b128efdb2e3'
scopes=['wl.signin', 'wl.offline_access', 'onedrive.readwrite']

client = onedrivesdk.get_default_client(
    client_id='981a7fa3-b9f5-4b6a-bb3e-392e8bda1366', scopes=scopes)

auth_url = client.auth_provider.get_auth_url(redirect_uri)

#this will block until we have the code
code = GetAuthCodeServer.get_auth_code(auth_url, redirect_uri)

client.auth_provider.authenticate(code, redirect_uri, client_secret)
