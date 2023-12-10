import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

# import codecs
# from string import Template

# EmailSender = codecs.open("templates/EmailSender.html", "r", "UTF-8")
# html_content = f"""{EmailSender.read()}"""

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key["api-key"] = os.getenv("SENDINBLUE_API_KEY")


class SendiblueEmail:
    __api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    def Verification_OTP(
        self,
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
                # html_content=Template(html_content).safe_substitute(
                #     title=title,
                #     PIN=otp,
                #     noteExp=f"Mã xác nhận của bạn sẽ hết hạn sau {noteExp} phút.",
                # ),
                template_id=4,
                params={
                    "title": title,
                    "PIN": otp,
                    "noteExp": f"Mã xác nhận của bạn sẽ hết hạn sau {noteExp} phút.",
                },
                headers={
                    "accept": "application/json",
                    "content-type": "application/json",
                },
            )
            api_response = self.__api_instance.send_transac_email(
                send_smtp_email=email_campaigns
            )
            return api_response
        except ApiException as e:
            print(
                "Exception when calling EmailCampaignsApi->create_email_campaign: %s\n"
                % e
            )

    def Verification_Link(
        self,
        to,
        title,
        subject,
        nameLink,
        linkVerify,
        note1,
        noteExp=10,
    ):
        try:
            email_campaigns = sib_api_v3_sdk.SendSmtpEmail(
                subject=subject,
                sender={"name": "Phimhay247", "email": "account@phimhay247z.org"},
                to=[{"email": to}],
                template_id=5,
                params={
                    "title": title,
                    "linkVerify": linkVerify,
                    "nameLink": nameLink,
                    "note1": note1,
                    "noteExp": f"Yêu cầu này của bạn sẽ hết hiệu lực sau {noteExp} phút.",
                },
                headers={
                    "accept": "application/json",
                    "content-type": "application/json",
                },
            )
            api_response = self.__api_instance.send_transac_email(
                send_smtp_email=email_campaigns
            )
            return api_response
        except ApiException as e:
            print(
                "Exception when calling EmailCampaignsApi->create_email_campaign: %s\n"
                % e
            )
