import requests
import json
from base64 import b64encode

"""
    Documentation of the API: https://developer.infusionsoft.com/docs/rest/
"""


class Client:
    api_base_url = "https://api.infusionsoft.com/crm/rest/v1/"
    header = {"Accept": "application/json, */*", "content-type": "application/json"}

    def __init__(self, token):
        self.token = token
        self.header["Authorization"] = "Bearer " + self.token

    def make_request(self, method, endpoint, data=None, json=None, **kwargs):
        """
            this method do the request petition, receive the different methods (post, delete, patch, get) that the api allow
            :param method:
            :param endpoint:
            :param data:
            :param kwargs:
            :return:
        """
        url = '{0}{1}'.format(self.api_base_url, endpoint)

        if method == "get":
            response = requests.request(method, url, headers=self.header, params=kwargs)
        else:
            response = requests.request(method, url, headers=self.header, data=data, json=json)
        return self.parse_response(response)

    def _get(self, endpoint, data=None, json=None, **kwargs):
        return self.make_request('get', endpoint, data=data, json=json, **kwargs)

    def _post(self, endpoint, data=None, json=None, **kwargs):
        return self.make_request('post', endpoint, data=data, json=json, **kwargs)

    def _delete(self, endpoint, data=None, json=None, **kwargs):
        return self.make_request('delete', endpoint, data=data, json=json, **kwargs)

    def _patch(self, endpoint, data=None, json=None, **kwargs):
        return self.make_request('patch', endpoint, data=data, json=json, **kwargs)

    def parse_response(self, response):
        """
            This method get the response request and returns json data or raise exceptions
            :param response:
            :return:
        """
        if response.status_code == 204 or response.status_code == 201:
            return True
        elif response.status_code == 400:
            raise Exception(
                "The URL {0} retrieved an {1} error. Please check your request body and try again.\nRaw message: {2}".format(
                    response.url, response.status_code, response.text))
        elif response.status_code == 401:
            raise Exception(
                "The URL {0} retrieved and {1} error. Please check your credentials, make sure you have permission to perform this action and try again.".format(
                    response.url, response.status_code))
        elif response.status_code == 403:
            raise Exception(
                "The URL {0} retrieved and {1} error. Please check your credentials, make sure you have permission to perform this action and try again.".format(
                    response.url, response.status_code))
        elif response.status_code == 404:
            raise Exception(
                "The URL {0} retrieved an {1} error. Please check the URL and try again.\nRaw message: {2}".format(
                    response.url, response.status_code, response.text))
        return response.json()

    def oauth_access(self, client_id, callback):
        url = "https://signin.infusionsoft.com/app/oauth/authorize?client_id={0}&redirect_uri={1}&response_type={2}".format(
            client_id, callback, "code")
        return url

    def refresh_token(self, client_id, client_secret, re_token):
        """
            to refresh the token you must to give client_id, client_secret and refresh token
            :param client_id:
            :param client_secret:
            :param re_token:
            :return:
        """
        url = "https://api.infusionsoft.com/token"
        authorization = '{0}:{1}'.format(client_id, client_secret)
        header = {'Authorization': 'Basic {0}'.format(b64encode(authorization.encode('UTF-8')).decode('UTF-8'))}
        args = {'grant_type': 'refresh_token', 'refresh_token': re_token}
        response = requests.post(url, headers=header, data=args)
        return self.parse_response(response)

    def get_contact_custom_fields(self, **kwargs):
        # url = self.api_base_url + "{0}".format("contactCustomFields")
        # response = requests.get(url, headers=self.header)
        # return self.parse_response(response)
        return self._get('contactCustomFields', **kwargs)

    def get_contacts(self, **kwargs):
        """
            To get all the contacts you can just call the method, to filter use limit, order, offset.
            For other options see the documentation of the API
            :param limit:
            :param order:
            :param offset:
            :return:
        """
        return self._get('contacts', **kwargs)
        # url = self.api_base_url + "{0}".format("contacts")
        # response = requests.get(url, headers=self.header, params=kwargs)
        # return self.parse_response(response)

    def create_contact(self, email=None, phone_number=None, **kwargs):
        """
            For create a contact is obligatory to fill the email or the phone number, I also recommend to fill the given_name="YOUR NAME"
            :param email:
            :param phone_number:
            :param kwargs:
            :return:
        """
        params = {}
        if email is None:
            if phone_number is None:
                raise Exception("Necesito un telefono o un correo.")
            else:
                params["phone_numbers"] = [{"field": "PHONE1", "number": phone_number}]
        else:
            params["email_addresses"] = [{"email": email, "field": "EMAIL1"}]

            if phone_number is not None:
                params["phone_numbers"] = [{"field": "PHONE1", "number": phone_number}]
        params.update(kwargs)
        return self._post('contacts', json=params, **kwargs)

    def delete_contact(self, id):
        """
            To delete a contact is obligatory send the id of the contact to delete
            :param id:
            :return:
        """
        if id != "":
            endpoint = 'contacts/{0}'.format(id)
            return self._delete(endpoint)
        else:
            raise Exception("El id es obligatorio")

    def update_contact(self, id, **kwargs):
        """
            To update a contact you must to send the id of the contact to update
            For other options see the documentation of the API
            :param id:
            :param kwargs:
            :return:
        """
        params = {}
        if id != "":
            endpoint = 'contacts/{0}'.format(id)
            params.update(kwargs)
            return self._patch(endpoint, data=params)
        else:
            raise Exception("El id es obligatorio")

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
        if id != "":
            endpoint = 'campaigns/{0}'.format(id)
            return self._get(endpoint, **kwargs)
        else:
            raise Exception("El id es obligatorio")

    def get_emails(self, **kwargs):
        """
            To get the emails just call the method, if you need filter options see the documentation of the API
            :param limit:
            :param offset:
            :param kwargs:
            :return:
        """
        return self._get('emails', **kwargs)

    def get_opportunities(self, **kwargs):
        """
            To get the opportunities you can just call the method, also you can filter, see the options in the documentation API
            :param limit:
            :param order:
            :param offset:
            :param kwargs:
            :return:
        """
        return self._get('opportunities', **kwargs)

    def get_opportunities_pipeline(self, **kwargs):
        """
            This method will return a pipeline of opportunities
            :return:
        """
        return self._get('opportunity/stage_pipeline', **kwargs)

    def retrieve_opportunity(self, id, **kwargs):
        """
            To retrieve a campaign is necessary the campaign id
            For more options see the documentation of the API
            :param id:
            :return:
        """
        if id != "":
            endpoint = 'opportunities/{0}'.format(id)
            return self._get(endpoint, kwargs)
        else:
            raise Exception("El id es obligatorio")

    def create_opportunity(self, opportunity_title=None, contact=None, stage=None, **kwargs):
        """
            To create an opportunity is obligatory to send a title of the opportunity, the contact who have the opportunity, and stage
            For more information see the documentation of the API
            :param opportunity_title:
            :param contact:
            :param stage:
            :param kwargs:
            :return:
        """
        params = {}
        if opportunity_title is None and contact is None and stage is None:
            raise Exception("Necesito un titulo, un contacto y un escenario.")
        else:
            params["opportunity_title"] = opportunity_title
            params["contact"] = [{"first_name": contact}]
            params["stage"] = [{"name": stage}]
        params.update(kwargs)
        return self._post('opportunities', data=params, **kwargs)

    def update_opportunity(self, id, **kwargs):
        """
            To update an opportunity is obligatory the id, the other fields you can see in the documentation
            :param id:
            :param kwargs:
            :return:
        """
        params = {}
        if id != "":
            endpoint = 'opportunities/{0}'.format(id)
            params.update(kwargs)
            return self._patch(endpoint, data=params)
        else:
            raise Exception("El id es obligatorio")

    def get_hook_events(self, **kwargs):
        callback = "{0}/{1}".format("hooks", "event_keys")
        return self._get(callback, **kwargs)

    def get_hook_subscriptions(self, **kwargs):
        return self._get('hooks', **kwargs)

    def verify_hook_subscription(self, id):
        if id != "":
            callback = "{0}/{1}/{2}".format("hooks", id, "verify")
            return self._post(callback, data=None)
        else:
            raise Exception("El id es obligatorio")

    def create_hook_subscription(self, event, callback):
        if event is not None and callback is not None:
            args = {"eventKey": event, "hookUrl": callback}
            return self._post('hooks', data=args)
        else:
            raise Exception("El hook necesita un evento y una url")

    def update_hook_subscription(self, id, event, url):
        if id != "":
            callback = "{0}/{1}".format("hooks", id)
            args = {"eventKey": event, "hookUrl": url}
            return self._post(callback, data=args)
        else:
            raise Exception("El id es obligatorio")

    def delete_hook_subscription(self, id):
        if id != "":
            callback = "{0}/{1}".format("hooks", id)
            return self._delete(callback)
        else:
            raise Exception("El id es obligatorio")