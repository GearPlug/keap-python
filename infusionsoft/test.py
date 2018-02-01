from infusionsoft.client import Client

"""
MAIN INSTANCE
here you instance the main class, obligatory send the access token
"""
client_id = "kbj7nhv3b7yezsrxck2cc749"
client_secret = "UMtN6PGPud"
access_token = "87dyzmcukud8cb327mzm4xcw"
refresh_token = "m5cwmajgqxh6mv26bd47u2gz"
callback = ""
petition = Client(access_token)

"""
OAUTH URL
here you will get the url to do the oauth petition, you have to send the client id and the callback url
"""
# oauth = petition.oauth_access("client_id", "callback")
# print(oauth)

"""
REFRESH TOKEN
here you can refresh the token, are obligatory the client id, client secret and the refresh token
"""
# refresh_token = petition.refresh_token(client_id, client_secret, refresh_token)
# print(refresh_token)

"""
CONTACT TEST
here you can list all the custom fields of the contacts
"""
# custom_fields = petition.get_contact_custom_fields()
# print(custom_fields)

""" 
    ***here you create a contact, you must to give a valid email or a phone number and that is send as a kwarg
    data = {'email_addresses': [{'email': 'EMAIL@EMAIL.com', 'field': 'EMAIL1'}], 'given_name': 'NAME'}
"""
# create_contact = petition.create_contact(**data)
# print(create_contact)

""" ***here you delete a contact, is obligatory the id of the contact"""
# delete_contact = petition.delete_contact(180)
# print(delete_contact)

""" 
    ***here you can update a contact, is obligatory the id of the contact to update
    To update just use this sintaxis: update_contact('YOURID', given_name="name", email_addresses=[{"email":"email@email.com","field":"EMAIL1"}]) 
"""
# update_contact = petition.update_contact('184', given_name="Hernan", family_name="Herrera", email_addresses=[{"email":"hernan_herre@gmail.com","field":"EMAIL1"}])
# print(update_contact)

""" 
    ***here you list the contacts, can receive limit, order, and offset.
    For filter specific camps use this sintaxis: get_contacts(field="name", order_direction="descending")
"""
# list_contacts = petition.get_contacts(order="id", order_direction="descending")
# print(list_contacts['contacts'])

"""
    ***here you can retrieve a contact, send the ID and the optional_properties values
"""
# retrieve_contact = petition.retrieve_contact(166, optional_properties="custom_fields,preferred_name,opt_in_reason,notes")
# print(retrieve_contact)

"""
CAMPAIGN TEST
here you list the campaigns, can receive limit and offset
"""
# list_campaigns = petition.get_campaigns()
# print(list_campaigns)

""" ***here you can retrieve a specific campaign, obligatory the id of the campaign"""
# retrieve_campaign = petition.retrieve_campaign('')
# print(retrieve_campaign)

"""
EMAIL TEST
here you can get all, or some emails, receive limit or offset
"""
# list_emails = petition.get_emails()
# print(list_emails)

"""
OPPORTUNITIES TEST
here you can list the opportunities, can receive limit, order, and offset
"""
# list_opportunities = petition.get_opportunities()
# print(list_opportunities)

""" ***here you can list all t3jpyhrhu2r9ac6cw4uta7sf9he opportunities in pipeline, not receive anyshit"""
# list_all_opportunities = petition.get_opportunities_pipeline()
# print(list_all_opportunities)

""" ***here you can retrieve a specific opportunity, obligatory send the id"""
# retrieve_opportunity = petition.retrieve_opportunity("")
# print(retrieve_opportunity)

""" 
    ***here you can create an opportunity, obligatory opportunity_title, contact, and stage as a json array
    "opportunity_title": "YOURTITLE",
    "contact": {
        "company_name": "COMPANYNAME",
        "email": "COMPANY@EMAIL.COM",
        "first_name": "NAME",
        "id": ID,
        "job_title": "JOBNAME",
        "last_name": "LASTNAME",
        "phone_number": "PHONENUMBER"
    },
    "stage": {
        "id": ID,
        "name": "NAME",
    },
"""
# create_opportunity = petition.create_opportunity()
# print(create_opportunity)

""" 
    ***here you can update an opportunity, obligatory send the id of the opportunity and the data to update as a json array
"""
# update_opportunity = petition.update_opportunity(ID, opportunity_title="NAME")
# print(update_opportunity)

"""
PRODUCT METHOD TEST
here you can list the products    
"""
# get_products = petition.get_products()
# print(get_products)


"""
TASK METHOD TEST
here you can list the tasks
"""
# get_tasks = petition.get_tasks()
# print(get_tasks)


"""
ORDER METHOD TEST
here you can list the order
"""
# get_orders = petition.get_orders()
# print(get_orders)

"""
HOOKS METHODS TEST
here you can list the hooks events, just call the method
"""
# get_hook_events = petition.get_hook_events()
# print(get_hook_events)


""" ***here you can verify a hook subscription"""
# verify_hook = petition.verify_hook_subscription("74")
# print(verify_hook)

""" ***here you can create a hook subscription, send the hook event and the url callback"""
# create_hook = petition.create_hook_subscription("opportunity.add", "http://23bc0c82.ngrok.io/api/callback")
# print(create_hook)

""" ***here you can update a hook, send the hook id, event and url"""
# update_hook = petition.update_hook_subscription()
# print(update_hook)

""" ***here you can delete a hook subscription, is obligatory to send the hook id"""
# delete_hook = petition.delete_hook_subscription(126)
# print(delete_hook)

""" ***here you can get all the hook subscriptions, just call the method"""
# get_hook_subscriptions = petition.get_hook_subscriptions()
# print(get_hook_subscriptions)
