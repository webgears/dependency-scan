#!/usr/bin/env python

from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

class SheetWriter:
    def __init__(self, spreadsheet_id, sheet):
        self.spreadsheet_id = spreadsheet_id
        self.sheet = sheet

    def send(self, values, value_input_option="USER_ENTERED"):
        """
        Writes to the spreadsheet
        """
        # Call the Sheets API and write
        body = {
            'values': values
        }
        service = self.__connect()
        sheet = service.spreadsheets()
        result = sheet.values().append(spreadsheetId=self.spreadsheet_id,
                                    valueInputOption=value_input_option, body=body, range=self.sheet,).execute()

        print('{0} cells appended.'.format(result \
                                        .get('updates') \
                                        .get('updatedCells')))

    @staticmethod
    def __connect():
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        store = file.Storage('token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flags = tools.argparser.parse_args('--auth_host_name localhost --logging_level INFO --noauth_local_webserver'.split())
            flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
            creds = tools.run_flow(flow, store, flags)
        service = build('sheets', 'v4', http=creds.authorize(Http()))
        return service