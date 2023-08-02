import requests
import os


def Validate_Email(email):
    emailValidate = requests.get(
        f"https://emailvalidation.abstractapi.com/v1/?api_key={os.getenv('EMAIL_VALIDATION_API_KEY')}&email={email}"
    )

    # emailValidate = requests.get(
    #     f"https://mailbite.io/api/check?key={os.getenv('EMAIL_VALIDATION_API_KEY')}&email={email}"
    # )

    # emailValidate = requests.get(
    #     f"https://api.zerobounce.net/v2/validate?api_key={os.getenv('EMAIL_VALIDATION_API_KEY')}&email={email}"
    # )

    # emailValidate = requests.get(
    #     f"https://emailverification.whoisxmlapi.com/api/v2?apiKey={os.getenv('EMAIL_VALIDATION_API_KEY')}&emailAddress={email}"
    # )

    emailValidateResponse = emailValidate.json()

    ## Abstractapi
    isValid = emailValidateResponse["is_smtp_valid"]["value"] == True

    ## Mailbite
    # isValid = (
    #     emailValidateResponse["status"] == "ok"
    #     and emailValidateResponse["email_status"] == "VALID"
    # )

    # Zerobounce
    # isValid = emailValidateResponse["status"] == "valid"

    # WhoisXML
    # isValid = emailValidateResponse["smtpCheck"] == "true"

    if isValid:
        return True
    else:
        return False
