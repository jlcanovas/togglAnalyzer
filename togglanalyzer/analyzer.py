import mysql.connector
import requests
from togglanalyzer import storage
from requests.auth import HTTPBasicAuth

APP_ID = 'togglAnalyzer'
TOGGL_URL = 'https://toggl.com/reports/api/v2/details'

class TogglAnalyzer(object):

    def __init__(self, config):
        self.config = config

    def retrieve(self, starting_date, ending_date):
        """Retrieves the data from toggl"""

        print 'Retrieving data from ' + starting_date + ' to ' + ending_date
        url = TOGGL_URL + "?workspace_id=" + self.config.WORKSPACE + "&user_agent=" + APP_ID + "&since=" + starting_date + "&until=" + ending_date
        headers = {'content-type': 'application/json'}
        r = requests.get(url, headers=headers, auth=HTTPBasicAuth(self.config.API_TOKEN, 'api_token'))

        total_count = r.json()['total_count']
        per_page = r.json()['per_page']
        page_number = 1

        print 'Found ' + str(total_count) + ' entries'

        toggl_storage = storage.TogglStorage(self.config)
        analyzed = per_page
        self.retrieve_page(toggl_storage, page_number, analyzed, total_count, r.json()['data'])

        if(total_count > per_page):
            while(analyzed < total_count):
                page_number = page_number + 1
                url = TOGGL_URL + "?workspace_id=" + self.config.WORKSPACE + "&user_agent=" + APP_ID + "&since=" + starting_date + "&until=" + ending_date + "&page=" + str(page_number)
                headers = {'content-type': 'application/json'}
                r = requests.get(url, headers=headers, auth=HTTPBasicAuth(self.config.API_TOKEN, 'api_token'))

                if analyzed + 50 >= total_count:
                    analyzed = total_count
                else :
                    analyzed = analyzed + per_page
                self.retrieve_page(toggl_storage, page_number, analyzed, total_count, r.json()['data'])

    def retrieve_page(self, toggl_storage, page_number, analyzed, total_count, page):
        """Retrieves a specific page"""
        print 'Page ' + str(page_number) + ' (' + str(analyzed) + '/' + str(total_count) + ' entries)...'
        for elem in page:
            id = elem['id']
            description = elem['description']
            start = elem['start']
            end = elem['end']
            user = elem['user']
            project = elem['project']
            toggl_storage.add_entry(id, description, start, end, user, project)
