"""
    Documentation of the API: https://developer.infusionsoft.com/docs/rest/
"""

import requests
from base64 import b64encode
from .errors import TokenError, AuthError, DataError, ConnectionError


class Client:

    api_base_url = "https://api.infusionsoft.com/crm/rest/v1/"
    header = {"Accept": "application/json, */*", "content-type": "application/json"}

    def __init__(self, client_id=None, client_secret=None, token=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = token

    def make_request(self, method, endpoint, data=None, json_data=None, **kwargs):
        """
            This method do the request petition,
            receive the different methods (post, delete, patch, get) that the api allows.
            :param method:
            :param endpoint:
            :param data:
            :param json_data:
            :param kwargs:
            :return:
        """
        if not self.token:
            raise TokenError("To make petitions the token is required.")

        self.header["Authorization"] = "Bearer " + self.token
        url = '{0}{1}'.format(self.api_base_url, endpoint)

        if method == "get":
            response = requests.request(method, url, headers=self.header, params=kwargs)
        else:
            response = requests.request(method, url, headers=self.header, data=data, json_data=json_data)
            response = requests.request(method, url, headers=self.header, data=data, json=json_data)
        return self.parse_response(response)


    def _get(self, endpoint, data=None, **kwargs):
        return self.make_request('get', endpoint, data=data, **kwargs)

    def _post(self, endpoint, data=None, json_data=None, **kwargs):
        return self.make_request('post', endpoint, data=data, json_data=json_data, **kwargs)

    def _delete(self, endpoint, **kwargs):
        return self.make_request('delete', endpoint, **kwargs)

    def _patch(self, endpoint, data=None, json_data=None, **kwargs):
        return self.make_request('patch', endpoint, data=data, json_data=json_data, **kwargs)

    def _put(self, endpoint, json_data=None, **kwargs):
        return self.make_request('put', endpoint, json_data=json_data, **kwargs)

    @staticmethod
    def parse_response(response):
        """
            This method get the response request and returns json_data data or raise exceptions
            :param response:
            :return:
        """
        if response.status_code == 204 or response.status_code == 201:
            return True
        elif response.status_code == 400:
            raise DataError(
                "The URL {0} retrieved an {1} error. "
                "Please check your request body and try again.\nRaw message: {2}".format(
                    response.url,
                    response.status_code,
                    response.text
                )
            )
        elif response.status_code == 401:
            raise AuthError(
                "The URL {0} retrieved and {1} error. Please check your credentials, "
                "make sure you have permission to perform this action and try again.".format(
                    response.url,
                    response.status_code
                )
            )
        elif response.status_code == 403:
            raise AuthError(
                "The URL {0} retrieved and {1} error. Please check your credentials, "
                "make sure you have permission to perform this action and try again.".format(
                    response.url,
                    response.status_code
                )
            )
        elif response.status_code == 404:
            raise ConnectionError(
                "The URL {0} retrieved an {1} error. Please check the URL and try again.\n"
                "Raw message: {2}".format(
                    response.url,
                    response.status_code,
                    response.text
                )
            )
        return response.json()

    def oauth_access(self, callback):
        """
            This method return the main url to begin the oauth flow
            :param client_id:
            :param callback:
            :return:
        """
        if self.client_id is None:
            raise AuthError("client_id is required to obtain the url.")
        if callback is None:
            raise AuthError("callback is required to obtain the url.")

        url = "https://signin.infusionsoft.com/app/oauth/authorize?client_id={0}" \
              "&redirect_uri={1}&response_type={2}&scope={3}".format(
            self.client_id,
            callback,
            "code",
            "full"
        )
        return url

    def exchange_code(self, redirect_uri, code):
        """
            This method receive the code send in the first flow step, later make the petition to get the token
            :param redirect_uri:
            :param code:
            :return:
        """
        if self.client_id is None:
            raise AuthError("client_id is required for the code exchange.")
        if self.client_secret is None:
            raise AuthError("client_secret is required for the code exchange.")
        if not redirect_uri:
            raise AuthError("redirect_uri is required for the code exchange.")
        if not code:
            raise AuthError("code is required for the code exchange.")

        data = {
            'client_id': self.client_id,
            'redirect_uri': redirect_uri,
            'client_secret': self.client_secret,
            'code': code,
            'grant_type': 'authorization_code',
        }
        url = "https://api.infusionsoft.com/token"
        response = requests.post(url, data=data)
        return self.parse_response(response)

    def refresh_token(self, refresh_token):
        """
            To refresh the token you must to give client_id, client_secret and refresh token
            :param refresh_token:
            :return:
        """
        if self.client_id is None:
            raise TokenError("client_id is required for the refresh token to be obtained.")
        if self.client_secret is None:
            raise TokenError("client_secret is required for the refresh token to be obtained.")
        if not refresh_token:
            raise TokenError("refresh_token is required for the refresh token to be obtained.")

        url = "https://api.infusionsoft.com/token"
        authorization = '{0}:{1}'.format(self.client_id, self.client_secret)
        header = {'Authorization': 'Basic {0}'.format(b64encode(authorization.encode('UTF-8')).decode('UTF-8'))}
        args = {'grant_type': 'refresh_token', 'refresh_token': refresh_token}
        response = requests.post(url, headers=header, data=args)
        return self.parse_response(response)

    def set_token(self, token):
        """
            Sets the Token for its use in this library.
            :param token: A string with the Token.
            :return:
        """
        if not token:
            raise TokenError("token is required for it to be set.")
        self.token = token

    def get_data(self, endpoint, **kwargs):
        return self._get(endpoint, **kwargs)

    def create_data(self, endpoint, **kwargs):
        if kwargs is not None:
            params = {}
            params.update(kwargs)
            return self._post(endpoint, json_data=params)

    def update_data(self, endpoint, data_id, **kwargs):
        if not data_id:
            raise DataError("The data_id is required.")

        params = {}
        url = '{0}/{1}'.format(endpoint, data_id)
        params.update(kwargs)
        return self._patch(url, json_data=params)

    def delete_data(self, endpoint, data_id):
        if not data_id:
            raise DataError("The data_id is required.")

        url = '{0}/{1}'.format(endpoint, data_id)
        return self._delete(url)

    def get_contact_custom_fields(self):
        return self._get('contactCustomFields')

    def get_contacts(self, **kwargs):
        """
            To get all the contacts you can just call the method, to filter use limit, order, offset.
            For other options see the documentation of the API
            :return:
        """
        return self._get('contacts', **kwargs)

    def retrieve_contact(self, id, **kwargs):
        if not id:
            raise DataError("The ID is required.")

        endpoint = 'contacts/{0}'.format(id)
        return self._get(endpoint, **kwargs)

    def create_contact(self, **kwargs):
        """
            For create a contact is obligatory to fill the email or the phone number.
            I also recommend to fill the given_name="YOUR NAME"
            :param email:
            :param phone_number:
            :param kwargs:
            :return:
        """
        if kwargs is not None:
            params = {}
            params.update(kwargs)
            return self._post('contacts', json_data=params)
        raise DataError("To create a contact is necessary a valid name and email")

    def delete_contact(self, id):
        """
            To delete a contact is obligatory send The ID of the contact to delete
            :param id:
            :return:
        """
        if not id:
            raise DataError("The ID is required.")

        endpoint = 'contacts/{0}'.format(id)
        return self._delete(endpoint)

    def update_contact(self, id, **kwargs):
        """
            To update a contact you must to send The ID of the contact to update
            For other options see the documentation of the API
            :param id:
            :param kwargs:
            :return:
        """
        if not id:
            raise DataError("The ID is required.")

        params = {}
        endpoint = 'contacts/{0}'.format(id)
        params.update(kwargs)
        return self._patch(endpoint, json_data=params)

    def get_campaigns(self, **kwargs):
        """
            To get the campaigns just call the method or send options to filter
            For more options see the documentation of the API
            :param limit:
            :param offset:
            :return:
        """
        return self._get('campaigns', **kwargs)

    def retrieve_campaign(self, id, **kwargs):
        """
            To retrieve a campaign is necessary the campaign id
            For more options see the documentation of the API
            :param id:
            :param kwargs:
            :return:
        """
        if not id:
            raise DataError("The ID is required.")

        endpoint = 'campaigns/{0}'.format(id)
        return self._get(endpoint, **kwargs)

    def get_emails(self, **kwargs):
        """
            To get the emails just call the method, if you need filter options see the documentation of the API.
            :param limit:
            :param offset:
            :param kwargs:
            :return:
        """
        return self._get('emails', **kwargs)

    def get_opportunities(self, **kwargs):
        """
            To get the opportunities you can just call the method.
            Also you can filter, see the options in the documentation API.
            :param limit:
            :param order:
            :param offset:
            :param kwargs:
            :return:
        """
        return self._get('opportunities', **kwargs)

    def get_opportunities_pipeline(self):
        """
            This method will return a pipeline of opportunities
            :return:
        """
        return self._get('opportunity/stage_pipeline')

    def retrieve_opportunity(self, id, **kwargs):
        """
            To retrieve a campaign is necessary the campaign id
            For more options see the documentation of the API
            :param id:
            :return:
        """
        if not id:
            raise DataError("The ID is required.")

        endpoint = 'opportunities/{0}'.format(id)
        return self._get(endpoint, kwargs)

    def create_opportunity(self, **kwargs):
        """
            To create an opportunity is obligatory to send a title of the opportunity,
            the contact who have the opportunity, and stage.
            For more information see the documentation of the API.
            :param opportunity_title:
            :param contact:
            :param stage:
            :param kwargs:
            :return:
        """
        if kwargs:
            params = {}
            params.update(kwargs)
            return self._post('opportunities', json_data=params)

    def update_opportunity(self, id, **kwargs):
        """
            To update an opportunity is obligatory The ID, the other fields you can see in the documentation.
            :param id:
            :param kwargs:
            :return:
        """
        if not id:
            raise DataError("The ID is required.")

        params = {}
        endpoint = 'opportunities/{0}'.format(id)
        params.update(kwargs)
        return self._patch(endpoint, json_data=params)

    def get_products(self, **kwargs):
        return self._get('products/search', **kwargs)

    def retrieve_product(self, id):
        if not id:
            raise DataError("The ID is required.")

        endpoint = "products/{0}".format(id)
        return self._get(endpoint)

    def get_tasks(self, **kwargs):
        return self._get('tasks', **kwargs)

    def create_task(self, **kwargs):
        if not kwargs:
            raise DataError("title and a due_date are required to create a task.")

        params = {}
        params.update(kwargs)
        return self._post('tasks', json_data=params)

    def delete_task(self, id):
        if not id:
            raise DataError("The ID is required.")

        endpoint = 'tasks/{0}'.format(id)
        return self._delete(endpoint)

    def update_task(self, id, **kwargs):
        if not id:
            raise DataError("The ID is required.")

        params = {}
        endpoint = 'tasks/{0}'.format(id)
        params.update(kwargs)
        return self._patch(endpoint, json_data=params)

    def retrieve_task(self, id):
        if not id:
            raise DataError("The ID is required.")

        endpoint = "tasks/{0}".format(id)
        return self._get(endpoint)

    def replace_task(self, id, **kwargs):
        if not id:
            raise DataError("The ID is required.")

        endpoint = "tasks/{0}".format(id)
        return self._put(endpoint, **kwargs)

    def get_orders(self, **kwargs):
        return self._get('orders', **kwargs)

    def retrieve_order(self, id):
        if not id:
            raise DataError("The ID is required.")

        endpoint = "tasks/{0}".format(id)
        return self._get(endpoint)

    def get_hook_events(self):
        callback = "{0}/{1}".format("hooks", "event_keys")
        return self._get(callback)

    def get_hook_subscriptions(self):
        return self._get('hooks')

    def verify_hook_subscription(self, id):
        if not id:
            raise DataError("The ID is required.")
        callback = "{0}/{1}/{2}".format("hooks", id, "verify")
        return self._post(callback, data=None)

    def create_hook_subscription(self, event, callback):
        if not event:
            raise DataError("The event is required.")
        if not callback:
            raise DataError("The callback is required.")

        args = {"eventKey": event, "hookUrl": callback}
        return self._post('hooks', json_data=args)

    def update_hook_subscription(self, id, event, url):
        if not id:
            raise DataError("The ID is required.")

        callback = "{0}/{1}".format("hooks", id)
        args = {"eventKey": event, "hookUrl": url}
        return self._post(callback, json_data=args)

    def delete_hook_subscription(self, id):
        if not id:
            raise DataError("The ID is required.")

        callback = "{0}/{1}".format("hooks", id)
        return self._delete(callback)
