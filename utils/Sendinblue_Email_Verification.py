from string import Template
import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import codecs

EmailSender = codecs.open("templates/EmailSender.html", "r", "UTF-8")

# sib_api_v3_sdk.configuration.api_key["api-key"] = os.getenv("SENDINBLUE_API_KEY")
# api_instance = sib_api_v3_sdk.EmailCampaignsApi()
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key["api-key"] = os.getenv("SENDINBLUE_API_KEY")
api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
    sib_api_v3_sdk.ApiClient(configuration)
)

html_content = f"""{EmailSender.read()}"""


def Email_Verification(
    to,
    otp,
    title="Xác minh tài khoản của bạn",
    noteExp=1,
):
    try:
        email_campaigns = sib_api_v3_sdk.SendSmtpEmail(
            subject="Mã xác thực email của bạn",
            sender={"name": "Phimhay247", "email": "account@phimhay247z.org"},
            to=[{"email": to}],
            html_content=Template(html_content).safe_substitute(
                title=title,
                PIN=otp,
                noteExp=f"Mã xác nhận của bạn sẽ hết hạn sau {noteExp} phút.",
            ),
            headers={
                "accept": "application/json",
                "content-type": "application/json",
            },
        )
        api_response = api_instance.send_transac_email(send_smtp_email=email_campaigns)
        return api_response
    except ApiException as e:
        print(
            "Exception when calling EmailCampaignsApi->create_email_campaign: %s\n" % e
        )
