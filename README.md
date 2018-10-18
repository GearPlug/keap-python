# infusionsoft-python

InfusionSoft API wrapper for Infusionsoft written in Python.

## Installing
```
pip install infusionsoft-python
```

## Usage
```
from infusionsoft.client import Client
client = Client('CLIENT_ID', 'CLIENT_SECRET', 'OPTIONAL - access_token')
```
#### Get authorization url
```
url = client.oauth_access("REDIRECT_URL")
```

#### Exchange the code for an access token
```
token = client.exchange_code('REDIRECT_URL', 'CODE')
```

#### Refresh token
```
token = client.refresh_token('REFRESH TOKEN')
```

#### Set token
```
token = client.set_token('TOKEN')
```

#### Get Contacts
here you list the contacts, can receive limit, order, order_direction and offset.
for filter specific camps use this sintaxis: get_contacts(field="name", order_direction="descending")
```
list_contacts = client.get_contacts(order="id", order_direction="descending")
```

#### Retrieve Contacts
here you can retrieve a contact, send the ID and the optional_properties values
```
retrieve_contact = client.retrieve_contact(166, optional_properties="custom_fields,preferred_name,opt_in_reason,notes")
```

#### Create Contact
here you create a contact, you must to give a valid email or a phone number and that is send as a kwarg
data = {'email_addresses': [{'email': 'EMAIL@EMAIL.com', 'field': 'EMAIL1'}], 'given_name': 'NAME'}
```
create_contact = client.create_contact(**data)
```

#### Delete Contact
here you delete a contact, is obligatory the id of the contact
```
delete_contact = client.delete_contact('ID')
```

#### Update Contact
data = {'email_addresses': [{'email': 'EMAIL@EMAIL.com', 'field': 'EMAIL1'}], 'given_name': 'NAME'}
```
update_contact = client.update_contact('184', **data)
```

#### Get Campaign
here you list the campaigns, can receive limit and offset
```
list_campaigns = client.get_campaigns()
```

#### Retrieve Campaign
here you can retrieve a specific campaign, obligatory the id of the campaign
```
retrieve_campaign = client.retrieve_campaign('ID')
```

#### Get Emails
here you can get all, can receive limit or offset
```
list_emails = client.get_emails()
```

#### Get Opportunities
here you can list the opportunities, can receive limit, order, and offset
```
list_opportunities = client.get_opportunities()
```

#### Get Opportunities Pipeline
here you can list the pipeline opportunities
```
list_all_opportunities = client.get_opportunities_pipeline()
```

#### Retrieve Opportunity
here you can retrieve a specific opportunity, obligatory send the id
```
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
```
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
```
update_opportunity = client.update_opportunity('ID', **data)
```

#### Get Products
here you can list the products
```
get_products = client.get_products()
```

#### Retrieve Product
here you can retrieve a specific product, just send the id of the product
```
retrieve_product = client.retrieve_product('ID')
```

#### Get Tasks
here you can list the tasks, can receive limit, offset
```
get_tasks = client.get_tasks()
```

#### Create Task
here you can list the tasks, can receive limit, offset
data = {'title': 'TASK TITLE', "contact": {"id": 170}}
```
create_task = client.create_task(**data)
```

#### Delete Task
here you can delete a tasks, obligatory send the id of the task
```
delete_task = client.delete_task('ID')
```

#### Update Task
here you can update a tasks, obligatory send the id of the task to update and the data
data = {'title': 'TASK TITLE', "contact": {"id": 170}}
```
update_task = client.update_task('ID', **data)
```

#### Retrieve Task
here you can retrieve a tasks, obligatory send the id of the task
```
retrieve_task = client.retrieve_task('ID')
```

#### Replace Task
here you can replace a task, obligatory send the id of the task
```
replace_task = client.replace_task('ID')
```

#### Get Orders
here you can get orders, can receive limit, offset
```
get_orders = client.get_orders()
```

#### Retrieve Order
here you can retrieve an order, obligatory send the id of the order
```
retrieve_order = client.retrieve_order('ID')
```

#### Get Hook Events
here you can list the hooks events, just call the method
```
get_hook_events = client.get_hook_events()
```

#### Get Webhooks
here you can get all the hook subscriptions, just call the method
```
get_hook_subscriptions = client.get_hook_subscriptions()
```

#### Verify Hook Subscription
here you can verify a hook subscription, send the id of the webhook to verify it
```
verify_hook = client.verify_hook_subscription('ID')
```

#### Create Hook Subscription
here you can create a hook subscription, send the hook event and the url callback
```
create_hook = client.create_hook_subscription("opportunity.add", "URL")
```

#### Update Hook Subscription
here you can update a hook, send the hook id, event and url
```
update_hook = petition.update_hook_subscription('ID', 'opportunity.delete', 'URL')
```

#### Delete Hook Subscription
here you can delete a hook subscription, is obligatory to send the hook id
```
delete_hook = petition.delete_hook_subscription('ID')
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
