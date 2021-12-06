from fusionauth.fusionauth_client import FusionAuthClient

client = FusionAuthClient('API-KEY', 'URL')

# retrieve a user by email
client_response = client.retrieve_user_by_email('art@vandalinc.com')
if client_response.was_successful():
    print(client_response.success_response)
else:
    print(client_response.error_response)