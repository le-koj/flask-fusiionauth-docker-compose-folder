import os
from flask import Flask, request, render_template, send_from_directory, session
from fusionauth.fusionauth_client import FusionAuthClient
import pkce

api_key = ""
client_id = ""
client_secret = ""
host_ip = "localhost"

base_uri = f"http://{host_ip}"

client = FusionAuthClient(api_key, f"{base_uri}:9011")

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route("/")
def index():
    code_verifier, code_challenge = pkce.generate_pkce_pair()

    login_uri = f"{base_uri}:9011/oauth2/authorize?client_id={client_id}\
                &response_type=code&redirect_uri=http%3A%2F%2F{host_ip}\
                %3A5000%2Foauth-callback&code_challenge={code_challenge}\
                &code_challenge_method=S256"

    register_uri = f"{base_uri}:9011/oauth2/register?client_id={client_id}\
                    &response_type=code&redirect_uri=http%3A%2F%2F{host_ip}\
                    %3A5000%2Foauth-callback&code_challenge={code_challenge}\
                    &code_challenge_method=S256"

    # save the verifier in session to send it to the token endpoint
    session['code_verifier'] = code_verifier
    return render_template(
                            "public/index.html",
                            login_uri=login_uri,
                            register_uri=register_uri
                            )

@app.route("/oauth-callback")
def oauth_callback():
    if not request.args.get("code"):
        uri = f"{base_uri}:5000/"
        return render_template(
            "public/error.html",
            uri=uri,
            msg="Failed to get auth token",
            reason=request.args["error_reason"],
            description=request.args["error_description"]
        )

    # get access token from fusionauth
    tok_resp = client.exchange_o_auth_code_for_access_token_using_pkce(
        request.args.get("code"),
        f"{base_uri}:5000/oauth-callback",
        session["code_verifier"],
        client_id,
        client_secret
    )

    if not tok_resp.was_successful():
        print(f"Failed to get token! Error: {tok_resp.error_response}")
        uri = f"{base_uri}:5000/"
        return render_template(
            "public/error.html",
            uri=uri,
            msg="Failed to get auth token",
            reason=tok_resp.error_response["error_reason"],
            description=tok_resp.error_response["error_description"]
        )

    user_resp = client.retrieve_user_using_jwt(tok_resp.success_response["access_token"])

    if not user_resp.was_successful():
        print(f"Failed to get user info! Error: {user_resp.error_response}")
        uri = f"{base_uri}:5000/"
        return render_template(
            "public/error.html",
            uri=uri,
            msg="Failed to get user info.",
            reason=tok_resp.error_response["error_reason"],
            description=tok_resp.error_response["error_description"]
        )

    registrations = user_resp.success_response["user"]["registrations"]
    if registrations is None or len(registrations) == 0 or not \
        any(r["applicationId"] == client_id for r in requirements):
        print("User not registered for the application")
        uri = f"{base_uri}:5000/"
        return render_template(
            "public/error.html",
            uri=uri,
            msg="User not registered for this application.",
            reason="Application Id not found in user object",
            description="Did you create a registration for this user and this application"
        )

    uri = f"{base_uri}:9011/oauth2/logout?client_id={client_id}"
    return render_template(
                "public/logged_in.html",
                uri=uri,
                user_id=user_resp.success_response["user"]["id"],
                email=user_resp.success_response["user"]["email"],
                created_at = user_resp.success_response["user"]["insertInstant"],
                updated_at=user_resp.success_response["user"]["lastUpdatedInstant"],
                last_login=user_resp.success_response["user"]["lastLoginInstant"],
                pwd_updated=user_resp.success_response["passwordLastUpdateInstant"],
                pwd_change=user_resp.success_response["user"]["passwordChangeRequired"]
            )

@app_route("/logout")
def logout():
    uri = f"{base_uri}:5000/"
    return render_template("public/logged_out.html", uri=uri)


if __name__ == "__main__":
    app.run(debug=True)


    
