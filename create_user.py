from fusionauth.fusionauth_client import FusionAuthClient

# you must apply your own API key and URL in production
client = FusionAuthClient("[API-KEY]", "[FUSIONAUTH-SERVER-URL]")

user_request = {
    'sendSetPasswordEmail': False,
    'skipVerification': True,
    'user':{
        'email': 'art@vandalinc.com',
        'password': 'password'
    }
}

client_response = client.create_user(None, user_request)

# verify user created
if client_response.was_successful():
    print(client_response.success_response)
else:
    print(client_response.error_response)

