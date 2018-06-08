#!/usr/bin/env python3
#
#  A library for the Sector Alarm API
#  Mikael Schultz <mikael@dofiloop.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import datetime
import json
import os
import re
import tempfile

import requests

from .HTML import ParseHTMLToken


def log(message):
    """ If we're in debug-mode we should show a lot more output """
    if os.environ.get('DEBUG'):
        print(message)


def fix_user(user_string):
    """ Cleanup the user string in the status object to only contain username. """
    return user_string.replace('(av ', '').replace(')', '')


def fix_date(date_string):
    """ Convert the Sector Alarm way of stating dates to something sane (ISO compliant). """
    result = ""
    try:
        epoch = re.search(r'/Date\(([0-9]+?)\)/', date_string).group(1)
        date = datetime.datetime.fromtimestamp(int(epoch)/1000)
        result = date.isoformat()
    except AttributeError:
        result = ""

    return result


class connect(object):
    """ The class that returns the current status of the alarm. """

    __login_page = 'https://minasidor.sectoralarm.se/User/Login'
    __check_page = 'https://minasidor.sectoralarm.se/User/GetUserInfo/'
    __status_page = 'https://minasidor.sectoralarm.se/Panel/GetOverview/'
    __log_page = 'https://minasidor.sectoralarm.se/Panel/GetPanelHistory/'
    __arm_panel = 'https://minasidor.sectoralarm.se/Panel/ArmPanel'
    
    __cookie_file = os.path.join(tempfile.gettempdir(), 'cookies.jar')

    # Class constructor
    def __init__(self, email, password, site_id, panel_code):
        self.__email = email
        self.__password = password
        self.__site_id = site_id
        self.__session = requests.Session()
        self.__panel_code = panel_code

    # Do an initial request to get the CSRF-token
    def __get_csrf_token(self):

        response = self.__session.get(self.__login_page)
        response.raise_for_status()
        parser = ParseHTMLToken()
        parser.feed(response.text)
        if not parser.tokens[0]:
            raise Exception('Could not find CSRF-token.')

        return parser.tokens[0]

    def __get_status(self):
        '''
        Fetch and parse the actual alarm status page.
        '''
        response = self.__session.post(self.__status_page)
        response.raise_for_status()

        response_dict = {'AlarmStatus': response.json().get('Panel', {}).get('ArmedStatus', None)}
        response_dict['StatusAnnex'] = response.json().get('Panel', {}).get('StatusAnnex', None)
        response_dict['AnnexAvailable'] = response.json().get('Panel', {}).get('AnnexAvailable', None)
        
        return response_dict

    def __arm_annex(self):
        '''
        Arming the annex. 
        Returns a dict with the status as received from the api.
        '''
        payload = {
                'ArmCmd':'ArmAnnex',
                'PanelCode': self.__panel_code,
                'HasLocks': 'False',
                'id': self.__site_id
                }
        
        response = self.__session.post(self.__arm_panel, data = payload) 
        response.raise_for_status()
        
        log('Arming the annex, status ' + response.json().get('status', {}))
        
        return { 'status' : response.json().get('status', {})}
    
    def __disarm_annex(self):
        '''
        Disarming the annex. 
        Returns a dict with the status as received from the api.
        '''
        payload = {
                'ArmCmd':'DisarmAnnex',
                'PanelCode': self.__panel_code,
                'HasLocks': 'False',
                'id':self.__site_id
                }
        
        response = self.__session.post(self.__arm_panel, data = payload) 
        response.raise_for_status()
        
        log('Disarming the annex, status ' + response.json().get('status', {}))
        
        return { 'status' : response.json().get('status', {})}

    
    def __get_log(self):
        '''
        Fetch and parse the event log page.
        '''
        response = self.__session.get(self.__log_page + self.__site_id)
        response.raise_for_status()
        event_log = []
        for row in (response.json())['LogDetails']:
            row_data = row.copy()
            row_data['Time'] = fix_date(row_data.get('Time', None))
            event_log.append(row_data)

        return event_log

    def __save_cookies(self):
        '''
        Store the cookie-jar on disk to avoid having to login
        each time the script is run.
        '''
        with open(self.__cookie_file, 'w') as cookie_file:
            json.dump(
                requests.utils.dict_from_cookiejar(self.__session.cookies),
                cookie_file
            )
        log('Saved {0} cookie values'.format(
            len(requests.utils.dict_from_cookiejar(
                self.__session.cookies).keys())))

    def __load_cookies(self):
        '''
        Load the cookies from the cookie-jar to avoid logging
        in again if the session still is valid.
        '''
        try:
            with open(self.__cookie_file, 'r') as cookie_file:
                self.__session.cookies = requests.utils.cookiejar_from_dict(
                    json.load(cookie_file)
                )
        except IOError as message:
            if str(message)[:35] != '[Errno 2] No such file or directory':
                raise message

        log('Loaded {0} cookie values'.format(
            len(requests.utils.dict_from_cookiejar(
                self.__session.cookies).keys())))

    def __is_logged_in(self):
        '''
        Check if we're logged in.
        Returns bool
        '''
        response = self.__session.get(self.__check_page)
        if(response.status_code == 401):
            log('Got Unauthorized (401). Assuming that we are not logged in.')
            return False;
        elif(response.status_code == 200):
            return True;
        else:
            response.raise_for_status();


    def __login(self):
        '''
        Login to the site if we're not logged in already. First try any
        existing session from the stored cookie. If that fails we should
        login again.
        '''
        self.__load_cookies()

        # TODO: Check for requests.exceptions.ConnectionError
        if not self.__is_logged_in():
            log('Logging in')
            form_data = {
                'userID': self.__email,
                'password': self.__password
            }
            self.__session = requests.Session()
            # Get CSRF-token and add it to the form data.
            form_data['__RequestVerificationToken'] = self.__get_csrf_token()

            # Do the actual logging in.
            response = self.__session.post(self.__login_page + '?Returnurl=~%2F', data=form_data)
            response.raise_for_status()
            # Save the cookies to file.
            self.__save_cookies()
        else:
            log('Already logged in')

    def event_log(self):
        """
        Retrieve the event log, login if necessary.
        """
        self.__login()

        # Get event log
        return self.__get_log()

    def status(self):
        """
        Wrapper function for logging in and fetching the status
        of the alarm in one go that returns a dict.
        """
        self.__login()

        # Get the status
        status = self.__get_status()
        return status
    
    def arm_annex(self):
        """
        Wrapper function for arming the annex
        of the alarm.
        Returns a dict with the status as received from the api.
        """
        self.__login()
        
        result = self.__arm_annex()
        return result
    
    def disarm_annex(self):
        """
        Wrapper function for disarming the annex
        of the alarm.
        Returns a dict with the status as received from the api.
        """        
        self.__login()
        
        result = self.__disarm_annex()
        return result
