# infusionsoft-python
![](https://img.shields.io/badge/version-0.1.6-success) ![](https://img.shields.io/badge/Python-3.8%20|%203.9%20|%203.10%20|%203.11-4B8BBE?logo=python&logoColor=white)

*InfusionSoft* API wrapper for Infusionsoft written in Python.

## Installing
```
pip install infusionsoft-python
```

## Usage
```python
from infusionsoft.client import Client
client = Client('CLIENT_ID', 'CLIENT_SECRET', 'OPTIONAL - access_token')
```
First time you will have to authorize your app to get the access_token. Follow these steps to do so:
#### Get authorization url
```python
url = client.oauth_access("REDIRECT_URL")
```
First, you need to generate a url and direct admin's browser to this url.
There she will see an Infusionsoft branded authorisation window.
When she clicks "Authorize", the browser will redirect the admin to the REDIRECT_URL that you have passed into this method.
A GET parameter named 'code' will be passed along side this request. You will need this CODE and the initial REDIRECT_URL to get the token.

Code sample using Flask:
```python
@app.route('/infusionsoft-auth', methods=['GET'])
def infusionsoft_auth():
    client = Client('CLIENT_ID', 'CLIENT_SECRET')

    code = request.args.get('code', None)
    if not code:
        url = client.oauth_access("127.0.0.1/infusionsoft-auth")
        return redirect(url, code=302)
```

#### Exchange the code for an access token
```python
token = client.exchange_code('REDIRECT_URL', 'CODE')
```
Once you've got the CODE parameter back, you will need to exchange it for a token, before it expires.
You need to use the same REDIRECT_URL that you've use to redirect your admin during the previous step and the CODE
that you've received.

This will get you both REFRESH_TOKEN and ACCESS_TOKEN for your application. **You will need to save both of these.**

access_token is used to sign every request you make to Infusionsoft. However, it expires every 24 hours.
refresh_token is used to get a new access_token and will expire in 90 days. Unless you refresh it within that period.

Here is the modified version of our Flask example:
```python
@app.route('/infusionsoft-auth', methods=['GET'])
def infusionsoft_auth():
    client = Client('CLIENT_ID', 'CLIENT_SECRET')

    code = request.args.get('code', None)
    if not code:
        url = client.oauth_access("127.0.0.1/infusionsoft-auth")
        return redirect(url, code=302)
    else:
        token = client.exchange_code("127.0.0.1/infusionsoft-auth", code)
        refresh_token = token.get('refresh_token')
        access_token = token.get('access_token')
        expiration_datetime = datetime.datetime.now() + datetime.timedelta(seconds=token.get('expires_in')) # This is the time when your access_token will expire exactly.
```

#### Set access token
Once you have an ACCESS_TOKEN you can start making requests. All you need to do is set it bore making a request.
```python
client = Client('CLIENT_ID', 'CLIENT_SECRET')
client.set_token('ACCESS_TOKEN')

list_contacts = client.get_contacts()   # Sample request.
```
Alternatively, you can set it on initialization.
```python
client = Client('CLIENT_ID', 'CLIENT_SECRET', 'ACCESS_TOKEN')

list_contacts = client.get_contacts()   # Sample request.
```

#### Refresh token
Before your ACCESS_TOKEN expires, it's a good idea to refresh it. You can put this task on cron, for example.
```python
token = client.refresh_token('REFRESH TOKEN')

refresh_token = token.get('refresh_token')
access_token = token.get('access_token')
expiration_datetime = datetime.datetime.now() + datetime.timedelta(seconds=token.get('expires_in')) # This is the time when your access_token will expire exactly.
```
Please note that even if you ACCESS_TOKEN expired, you can still call this method.
As long as your REFESH_TOKEN is not expired (usually 90 days).


#### Get Contacts
here you list the contacts, can receive limit, order, order_direction and offset.
for filter specific camps use this sintaxis: get_contacts(field="name", order_direction="descending")
```python
list_contacts = client.get_contacts(order="id", order_direction="descending")
```

#### Retrieve Contacts
here you can retrieve a contact, send the ID and the optional_properties values
```python
retrieve_contact = client.retrieve_contact(166, optional_properties="custom_fields,preferred_name,opt_in_reason,notes")
```

#### Create Contact
here you create a contact, you must to give a valid email or a phone number and that is send as a kwarg
data = {'email_addresses': [{'email': 'EMAIL@EMAIL.com', 'field': 'EMAIL1'}], 'given_name': 'NAME'}
```python
create_contact = client.create_contact(**data)
```

#### Delete Contact
here you delete a contact, is obligatory the id of the contact
```python
delete_contact = client.delete_contact('ID')
```

#### Update Contact
data = {'email_addresses': [{'email': 'EMAIL@EMAIL.com', 'field': 'EMAIL1'}], 'given_name': 'NAME'}
```python
update_contact = client.update_contact('184', **data)
```

#### Get Campaign
here you list the campaigns, can receive limit and offset
```python
list_campaigns = client.get_campaigns()
```

#### Retrieve Campaign
here you can retrieve a specific campaign, obligatory the id of the campaign
```python
retrieve_campaign = client.retrieve_campaign('ID')
```

#### Get Emails
here you can get all, can receive limit or offset
```python
list_emails = client.get_emails()
```

#### Get Opportunities
here you can list the opportunities, can receive limit, order, and offset
```python
list_opportunities = client.get_opportunities()
```

#### Get Opportunities Pipeline
here you can list the pipeline opportunities
```python
list_all_opportunities = client.get_opportunities_pipeline()
```

#### Retrieve Opportunity
here you can retrieve a specific opportunity, obligatory send the id
```python
retrieve_opportunity = client.retrieve_opportunity('ID')
```

#### Create Opportunity
here you can create an opportunity, obligatory opportunity_title, contact, and stage
data = {
    'contact': {
        'id': '170'
    },
    'stage': {
        'name': 'Stage Test',
        'id': 10,
        'details': {
            'check_list_items': [
                {'description': 'Test Opportunity'}
            ]
        }
    },
    'opportunity_title': 'OpportunityTitle'
}
```python
create_opportunity = client.create_opportunity(**data)
```

#### Update Opportunity
here you can update an opportunity, obligatory send the id of the opportunity and the data to update
data = {
    'contact': {
        'id': '170'
    },
    'stage': {
        'name': 'Stage Test',
        'id': 10,
        'details': {
            'check_list_items': [
                {'description': 'Test Opportunity'}
            ]
        }
    },
    'opportunity_title': 'OpportunityTitle'
}
```python
update_opportunity = client.update_opportunity('ID', **data)
```

#### Get Products
here you can list the products
```python
get_products = client.get_products()
```

#### Retrieve Product
here you can retrieve a specific product, just send the id of the product
```python
retrieve_product = client.retrieve_product('ID')
```

#### Get Tasks
here you can list the tasks, can receive limit, offset
```python
get_tasks = client.get_tasks()
```

#### Create Task
here you can list the tasks, can receive limit, offset
data = {'title': 'TASK TITLE', "contact": {"id": 170}}
```python
create_task = client.create_task(**data)
```

#### Delete Task
here you can delete a tasks, obligatory send the id of the task
```python
delete_task = client.delete_task('ID')
```

#### Update Task
here you can update a tasks, obligatory send the id of the task to update and the data
data = {'title': 'TASK TITLE', "contact": {"id": 170}}
```python
update_task = client.update_task('ID', **data)
```

#### Retrieve Task
here you can retrieve a tasks, obligatory send the id of the task
```python
retrieve_task = client.retrieve_task('ID')
```

#### Replace Task
here you can replace a task, obligatory send the id of the task
```python
replace_task = client.replace_task('ID')
```

#### Get Orders
here you can get orders, can receive limit, offset
```python
get_orders = client.get_orders()
```

#### Retrieve Order
here you can retrieve an order, obligatory send the id of the order
```python
retrieve_order = client.retrieve_order('ID')
```

#### Get Hook Events
here you can list the hooks events, just call the method
```python
get_hook_events = client.get_hook_events()
```

#### Get Webhooks
here you can get all the hook subscriptions, just call the method
```python
get_hook_subscriptions = client.get_hook_subscriptions()
```

#### Verify Hook Subscription
here you can verify a hook subscription, send the id of the webhook to verify it
```python
verify_hook = client.verify_hook_subscription('ID')
```

#### Create Hook Subscription
here you can create a hook subscription, send the hook event and the url callback
```python
create_hook = client.create_hook_subscription("opportunity.add", "URL")
```

#### Update Hook Subscription
here you can update a hook, send the hook id, event and url
```python
update_hook = petition.update_hook_subscription('ID', 'opportunity.delete', 'URL')
```

#### Delete Hook Subscription
here you can delete a hook subscription, is obligatory to send the hook id
```python
delete_hook = petition.delete_hook_subscription('ID')
```

#### List All Tags
Here you can get all available tags.
```python
all_tags = client.list_tags()
```

#### Apply Tag
Here you can apply a tag to a contact.
```python
res = client.apply_tag('TAG_ID', 'CONTACT_ID')
```
Or to multiple contacts at the same time.
```python
res = client.apply_tag('TAG_ID', ['CONTACT1_ID', 'CONTACT2_ID', ...])
```
The result will be a dict with contact IDs as keys and statuses as values.
```python
{'1': 'SUCCESS', '3': 'DUPLICATE'}
```

#### Remove Tag
Here you can remove previously applied tag from a contact.
```python
all_tags = remove_tag.list_tags('TAG_ID', 'CONTACT_ID')
```

## Error Handling
All library errors are inherited from the base **InfusionsoftException**.
You can either catch that, or you can catch more specific exceptions. Here is an example:
```python
from infusionsoft.client import Client
from infusionsoft.errors import InfusionsoftException, AuthError, TokenError, ConnectionError, DataError 


try:
    try:
        try:
            try:
                try:
                    client = Client('CLIENT_ID', 'CLIENT_SECRET', 'ACCESS_TOKEN')
                    list_contacts = client.get_contacts()   # Sample request.
                except DataError as e:
                    print('Something is wrong with the data.')
                    print(e)
            except ConnectionError as e:
                print('Something is wron with Infusionsoft connection.')
                print(e)
        except TokenError as e:
            print('Something is wrong with one of the tokens.')
            print(e)
    except AuthError as e:
        print('Authentication error.')
        print(e)
except InfusionsoftException as e:
    print('Something went wrong with Infusionsoft.')
    print(e)
```

## Requirements
- requests

## Tests
```
infusionsoft/test.py
```

## TODO Endpoints
- All Appointments Section
- All File Section
- All Tag Section

## Contributing
We are always grateful for any kind of contribution including but not limited to bug reports, code enhancements, bug fixes, and even functionality suggestions.
#### You can report any bug you find or suggest new functionality with a new [issue](https://github.com/GearPlug/infusionsoft-python/issues).
#### If you want to add yourself some functionality to the wrapper:
1. Fork it ( https://github.com/GearPlug/infusionsoft-python )
2. Create your feature branch (git checkout -b my-new-feature)
3. Commit your changes (git commit -am 'Adds my new feature')
4. Push to the branch (git push origin my-new-feature)
5. Create a new Pull Request
