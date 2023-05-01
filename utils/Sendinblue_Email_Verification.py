from string import Template
from utils.OTP_Generation import generateOTP
import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

# Instantiate the client\
# sib_api_v3_sdk.configuration.api_key["api-key"] = os.getenv("SENDINBLUE_API_KEY")
# api_instance = sib_api_v3_sdk.EmailCampaignsApi()
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key["api-key"] = os.getenv("SENDINBLUE_API_KEY")
api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
    sib_api_v3_sdk.ApiClient(configuration)
)
html_content = """<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office"><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="format-detection" content="telephone=no"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Mã xác thực email của bạn</title><style type="text/css" emogrify="no">#outlook a { padding:0; } .ExternalClass { width:100%; } .ExternalClass, .ExternalClass p, .ExternalClass span, .ExternalClass font, .ExternalClass td, .ExternalClass div { line-height: 100%; } table td { border-collapse: collapse; mso-line-height-rule: exactly; } .editable.image { font-size: 0 !important; line-height: 0 !important; } .nl2go_preheader { display: none !important; mso-hide:all !important; mso-line-height-rule: exactly; visibility: hidden !important; line-height: 0px !important; font-size: 0px !important; } body { width:100% !important; -webkit-text-size-adjust:100%; -ms-text-size-adjust:100%; margin:0; padding:0; } img { outline:none; text-decoration:none; -ms-interpolation-mode: bicubic; } a img { border:none; } table { border-collapse:collapse; mso-table-lspace:0pt; mso-table-rspace:0pt; } th { font-weight: normal; text-align: left; } *[class="gmail-fix"] { display: none !important; } </style><style type="text/css" emogrify="no"> @media (max-width: 600px) { .gmx-killpill { content: ' \03D1';} } </style><style type="text/css" emogrify="no">@media (max-width: 600px) { .gmx-killpill { content: ' \03D1';} .r0-c { box-sizing: border-box !important; text-align: center !important; valign: top !important; width: 320px !important } .r1-o { border-style: solid !important; margin: 0 auto 0 auto !important; width: 320px !important } .r2-c { box-sizing: border-box !important; text-align: center !important; valign: middle !important; width: 100% !important } .r3-o { border-style: solid !important; margin: 0 auto 0 auto !important; width: 100% !important } .r4-i { background-color: #ffffff !important; padding-bottom: 20px !important; padding-left: 15px !important; padding-right: 15px !important; padding-top: 20px !important } .r5-c { box-sizing: border-box !important; display: block !important; valign: middle !important; width: 100% !important } .r6-o { border-style: solid !important; width: 100% !important } .r7-i { padding-left: 0px !important; padding-right: 0px !important } .r8-c { box-sizing: border-box !important; text-align: left !important; valign: top !important; width: 64px !important } .r9-o { border-style: solid !important; margin: 0 auto 0 0 !important; width: 64px !important } .r10-c { box-sizing: border-box !important; text-align: left !important; valign: top !important; width: 100% !important } .r11-o { border-style: solid !important; margin: 0 auto 0 0 !important; width: 100% !important } .r12-i { padding-top: 0px !important; text-align: center !important } .r13-c { box-sizing: border-box !important; text-align: center !important; valign: top !important; width: 100% !important } .r14-i { background-color: #ffffff !important; padding-bottom: 20px !important; padding-left: 10px !important; padding-right: 10px !important; padding-top: 20px !important } .r15-c { box-sizing: border-box !important; display: block !important; valign: top !important; width: 100% !important } .r16-i { padding-top: 15px !important; text-align: center !important } .r17-i { padding-bottom: 15px !important; padding-top: 15px !important; text-align: left !important } .r18-c { box-sizing: border-box !important; text-align: center !important; valign: top !important; width: 150px !important } .r19-o { border-bottom-color: #0071ce !important; border-bottom-width: 1px !important; border-left-color: #0071ce !important; border-left-width: 1px !important; border-right-color: #0071ce !important; border-right-width: 1px !important; border-style: solid !important; border-top-color: #0071ce !important; border-top-width: 1px !important; margin: 0 auto 0 auto !important; margin-bottom: 0px !important; margin-top: 0px !important; width: 150px !important } .r20-i { background-color: #111c20 !important; padding-bottom: 10px !important; padding-left: 15px !important; padding-right: 15px !important; padding-top: 10px !important; text-align: center !important } .r21-i { background-color: #eff2f7 !important; padding-bottom: 20px !important; padding-left: 15px !important; padding-right: 15px !important; padding-top: 20px !important } .r22-i { color: #3b3f44 !important; padding-bottom: 0px !important; padding-top: 15px !important; text-align: center !important } .r23-i { color: #3b3f44 !important; padding-bottom: 0px !important; padding-top: 0px !important; text-align: center !important } .r24-i { color: #3b3f44 !important; padding-bottom: 15px !important; padding-top: 15px !important; text-align: center !important } .r25-c { box-sizing: border-box !important; text-align: center !important; width: 100% !important } .r26-i { padding-bottom: 15px !important; padding-left: 0px !important; padding-right: 0px !important; padding-top: 0px !important } .r27-c { box-sizing: border-box !important; text-align: center !important; valign: top !important; width: 129px !important } .r28-o { border-style: solid !important; margin: 0 auto 0 auto !important; width: 129px !important } body { -webkit-text-size-adjust: none } .nl2go-responsive-hide { display: none } .nl2go-body-table { min-width: unset !important } .mobshow { height: auto !important; overflow: visible !important; max-height: unset !important; visibility: visible !important; border: none !important } .resp-table { display: inline-table !important } .magic-resp { display: table-cell !important } } </style><!--[if !mso]><!--><style type="text/css" emogrify="no"> </style><!--<![endif]--><style type="text/css">p, h1, h2, h3, h4, ol, ul { margin: 0; } a, a:link { color: #0092ff; text-decoration: underline } .nl2go-default-textstyle { color: #3b3f44; font-family: arial,helvetica,sans-serif; font-size: 18px; line-height: 1.5; word-break: break-word } .default-button { color: #ffffff; font-family: arial,helvetica,sans-serif; font-size: 16px; font-style: normal; font-weight: bold; line-height: 1.15; text-decoration: none; word-break: break-word } .default-heading1 { color: #1F2D3D; font-family: arial,helvetica,sans-serif; font-size: 36px; word-break: break-word } .default-heading2 { color: #1F2D3D; font-family: arial,helvetica,sans-serif; font-size: 32px; word-break: break-word } .default-heading3 { color: #1F2D3D; font-family: arial,helvetica,sans-serif; font-size: 24px; word-break: break-word } .default-heading4 { color: #1F2D3D; font-family: arial,helvetica,sans-serif; font-size: 18px; word-break: break-word } a[x-apple-data-detectors] { color: inherit !important; text-decoration: inherit !important; font-size: inherit !important; font-family: inherit !important; font-weight: inherit !important; line-height: inherit !important; } .no-show-for-you { border: none; display: none; float: none; font-size: 0; height: 0; line-height: 0; max-height: 0; mso-hide: all; overflow: hidden; table-layout: fixed; visibility: hidden; width: 0; } </style><!--[if mso]><xml> <o:OfficeDocumentSettings> <o:AllowPNG/> <o:PixelsPerInch>96</o:PixelsPerInch> </o:OfficeDocumentSettings> </xml><![endif]--><style type="text/css">a:link{color: #0092ff; text-decoration: underline;}</style></head><body text="#3b3f44" link="#0092ff" yahoo="fix" style=""> <table cellspacing="0" cellpadding="0" border="0" role="presentation" class="nl2go-body-table" width="100%" style="width: 100%;"><tr><td align="center" class="r0-c"> <table cellspacing="0" cellpadding="0" border="0" role="presentation" width="600" class="r1-o" style="table-layout: fixed; width: 600px;"><tr><td valign="top" class=""> <table width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation"><tr><td class="r2-c" align="center"> <table cellspacing="0" cellpadding="0" border="0" role="presentation" width="100%" class="r3-o" style="table-layout: fixed; width: 100%;"><!-- --><tr><td class="r4-i" style="background-color: #ffffff; padding-bottom: 20px; padding-top: 20px;"> <table width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation"><tr><th width="16.67%" valign="middle" class="r5-c" style="font-weight: normal;"> <table cellspacing="0" cellpadding="0" border="0" role="presentation" width="100%" class="r6-o" style="table-layout: fixed; width: 100%;"><!-- --><tr><td valign="top" class="r7-i"> <table width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation"><tr><td class="r8-c" align="left"> <table cellspacing="0" cellpadding="0" border="0" role="presentation" width="64" class="r9-o" style="table-layout: fixed; width: 64px;"><tr><td class="" style="font-size: 0px; line-height: 0px;"> <img src="https://img.mailinblue.com/6019991/images/content_library/original/644e129c3a26b96fb4044108.png" width="64" border="0" class="" style="display: block; width: 100%;"></td> </tr></table></td> </tr></table></td> </tr></table></th> <th width="83.33%" valign="middle" class="r5-c" style="font-weight: normal;"> <table cellspacing="0" cellpadding="0" border="0" role="presentation" width="100%" class="r6-o" style="table-layout: fixed; width: 100%;"><!-- --><tr><td valign="top" class="r7-i"> <table width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation"><tr><td class="r10-c" align="left"> <table cellspacing="0" cellpadding="0" border="0" role="presentation" width="100%" class="r11-o" style="table-layout: fixed; width: 100%;"><tr><td align="left" valign="top" class="r12-i nl2go-default-textstyle" style="color: #3b3f44; font-family: arial,helvetica,sans-serif; font-size: 18px; line-height: 1.5; word-break: break-word; text-align: left;"> <div><h2 class="default-heading2" style="margin: 0; color: #1f2d3d; font-family: arial,helvetica,sans-serif; font-size: 32px; word-break: break-word;">Phimhay247</h2></div> </td> </tr></table></td> </tr></table></td> </tr></table></th> </tr></table></td> </tr></table></td> </tr><tr><td class="r13-c" align="center"> <table cellspacing="0" cellpadding="0" border="0" role="presentation" width="100%" class="r3-o" style="table-layout: fixed; width: 100%;"><!-- --><tr><td class="r14-i" style="background-color: #ffffff; padding-bottom: 20px; padding-top: 20px;"> <table width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation"><tr><th width="100%" valign="top" class="r15-c" style="font-weight: normal;"> <table cellspacing="0" cellpadding="0" border="0" role="presentation" width="100%" class="r6-o" style="table-layout: fixed; width: 100%;"><!-- --><tr><td valign="top" class="r7-i"> <table width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation"><tr><td class="r10-c" align="left"> <table cellspacing="0" cellpadding="0" border="0" role="presentation" width="100%" class="r11-o" style="table-layout: fixed; width: 100%;"><tr><td align="center" valign="top" class="r16-i nl2go-default-textstyle" style="color: #3b3f44; font-family: arial,helvetica,sans-serif; font-size: 18px; word-break: break-word; line-height: 1.5; padding-top: 15px; text-align: center;"> <div><h2 class="default-heading2" style="margin: 0; color: #1f2d3d; font-family: arial,helvetica,sans-serif; font-size: 32px; word-break: break-word;">Xác minh tài khoản của bạn</h2></div> </td> </tr></table></td> </tr><tr><td class="r10-c" align="left"> <table cellspacing="0" cellpadding="0" border="0" role="presentation" width="100%" class="r11-o" style="table-layout: fixed; width: 100%;"><tr><td align="left" valign="top" class="r17-i nl2go-default-textstyle" style="color: #3b3f44; font-family: arial,helvetica,sans-serif; font-size: 18px; line-height: 1.5; word-break: break-word; padding-bottom: 15px; padding-top: 15px; text-align: left;"> <div><p style="margin: 0;">Nhập mã xác minh sau đây:</p></div> </td> </tr></table></td> </tr><tr><td class="r18-c" align="center"> <table cellspacing="0" cellpadding="0" border="0" role="presentation" width="150" class="r19-o" style="background-color: #111c20; border-bottom-color: #0071ce; border-bottom-width: 1px; border-collapse: separate; border-left-color: #0071ce; border-left-width: 1px; border-radius: 5px; border-right-color: #0071ce; border-right-width: 1px; border-style: solid; border-top-color: #0071ce; border-top-width: 1px; margin-bottom: 0px; margin-top: 0px; table-layout: fixed; width: 150px;"><tr><td align="center" valign="top" class="r20-i nl2go-default-textstyle" style="color: #3b3f44; font-family: arial,helvetica,sans-serif; font-size: 18px; word-break: break-word; background-color: #111c20; border-radius: 4px; line-height: 1.5; padding-bottom: 10px; padding-left: 15px; padding-right: 15px; padding-top: 10px; text-align: center;"> <div><p style="margin: 0;"><strong>$code</strong></p></div> </td> </tr></table></td> </tr><tr><td class="r10-c" align="left"> <table cellspacing="0" cellpadding="0" border="0" role="presentation" width="100%" class="r11-o" style="table-layout: fixed; width: 100%;"><tr><td align="left" valign="top" class="r17-i nl2go-default-textstyle" style="color: #3b3f44; font-family: arial,helvetica,sans-serif; font-size: 18px; line-height: 1.5; word-break: break-word; padding-bottom: 15px; padding-top: 15px; text-align: left;"> <div><p style="margin: 0;">Vui lòng không cung cấp mã này cho bất kỳ bên thứ 3 nào khác.</p></div> </td> </tr></table></td> </tr></table></td> </tr></table></th> </tr></table></td> </tr></table></td> </tr><tr><td class="r13-c" align="center"> <table cellspacing="0" cellpadding="0" border="0" role="presentation" width="100%" class="r3-o" style="table-layout: fixed; width: 100%;"><!-- --><tr><td class="r21-i" style="background-color: #eff2f7; padding-bottom: 20px; padding-top: 20px;"> <table width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation"><tr><th width="100%" valign="top" class="r15-c" style="font-weight: normal;"> <table cellspacing="0" cellpadding="0" border="0" role="presentation" width="100%" class="r6-o" style="table-layout: fixed; width: 100%;"><!-- --><tr><td valign="top" class="r7-i" style="padding-left: 15px; padding-right: 15px;"> <table width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation"><tr><td class="r10-c" align="left"> <table cellspacing="0" cellpadding="0" border="0" role="presentation" width="100%" class="r11-o" style="table-layout: fixed; width: 100%;"><tr><td align="center" valign="top" class="r22-i nl2go-default-textstyle" style="font-family: arial,helvetica,sans-serif; word-break: break-word; color: #3b3f44; font-size: 18px; line-height: 1.5; padding-top: 15px; text-align: center;"> <div><p style="margin: 0;">Phimhay247</p></div> </td> </tr></table></td> </tr><tr><td class="r10-c" align="left"> <table cellspacing="0" cellpadding="0" border="0" role="presentation" width="100%" class="r11-o" style="table-layout: fixed; width: 100%;"><tr><td align="center" valign="top" class="r23-i nl2go-default-textstyle" style="font-family: arial,helvetica,sans-serif; word-break: break-word; color: #3b3f44; font-size: 18px; line-height: 1.5; text-align: center;"> <div><p style="margin: 0; font-size: 14px;">Sóc Sơn, Hà Nội</p></div> </td> </tr></table></td> </tr><tr><td class="r10-c" align="left"> <table cellspacing="0" cellpadding="0" border="0" role="presentation" width="100%" class="r11-o" style="table-layout: fixed; width: 100%;"><tr><td align="center" valign="top" class="r22-i nl2go-default-textstyle" style="font-family: arial,helvetica,sans-serif; word-break: break-word; color: #3b3f44; font-size: 18px; line-height: 1.5; padding-top: 15px; text-align: center;"> <div><p style="margin: 0; font-size: 14px;">This email was sent to {{contact.EMAIL}}</p></div> </td> </tr></table></td> </tr><tr><td class="r10-c" align="left"> <table cellspacing="0" cellpadding="0" border="0" role="presentation" width="100%" class="r11-o" style="table-layout: fixed; width: 100%;"><tr><td align="center" valign="top" class="r23-i nl2go-default-textstyle" style="font-family: arial,helvetica,sans-serif; word-break: break-word; color: #3b3f44; font-size: 18px; line-height: 1.5; text-align: center;"> <div><p style="margin: 0; font-size: 14px;">You've received it because you've subscribed to our newsletter.</p></div> </td> </tr></table></td> </tr><tr><td class="r10-c" align="left"> <table cellspacing="0" cellpadding="0" border="0" role="presentation" width="100%" class="r11-o" style="table-layout: fixed; width: 100%;"><tr><td align="center" valign="top" class="r24-i nl2go-default-textstyle" style="font-family: arial,helvetica,sans-serif; word-break: break-word; color: #3b3f44; font-size: 18px; line-height: 1.5; padding-bottom: 15px; padding-top: 15px; text-align: center;"> <div><p style="margin: 0; font-size: 14px;"><a href="{{ mirror }}" style="color: #0092ff; text-decoration: underline;">View in browser</a> | <a href="{{ unsubscribe }}" style="color: #0092ff; text-decoration: underline;">Unsubscribe</a></p></div> </td> </tr></table></td> </tr><tr><td class="r25-c" align="center"> <table cellspacing="0" cellpadding="0" border="0" role="presentation" width="100%" class="r3-o" style="table-layout: fixed; width: 100%;"><tr><td valign="top" class="r26-i" style="padding-bottom: 15px;"> <table width="100%" cellspacing="0" cellpadding="0" border="0" role="presentation"><tr><td class="r27-c" align="center"> <table cellspacing="0" cellpadding="0" border="0" role="presentation" width="129" class="r28-o" style="table-layout: fixed;"><tr><td height="48" class="" style="font-size: 0px; line-height: 0px;"> <img src="https://creative-assets.mailinblue.com/rnb-assets/en.png" width="129" border="0" class="" style="display: block; width: 100%;"></td> </tr></table></td> </tr></table></td> </tr></table></td> </tr></table></td> </tr></table></th> </tr></table></td> </tr></table></td> </tr></table></td> </tr></table></td> </tr></table></body></html>"""

# Define the campaign settings\


def Email_Verification(to):
    try:
        email_campaigns = sib_api_v3_sdk.SendSmtpEmail(
            subject="Mã xác thực email của bạn",
            sender={"name": "Phimhay247", "email": "duyhieu@phimhay247.site"},
            to=[{"email": to}],
            html_content=Template(html_content).safe_substitute(
                code=generateOTP(length=6)
            ),
            headers={
                "accept": "application/json",
                "content-type": "application/json",
            },
        )
        api_response = api_instance.send_transac_email(send_smtp_email=email_campaigns)
        print(api_response)
    except ApiException as e:
        print(
            "Exception when calling EmailCampaignsApi->create_email_campaign: %s\n" % e
        )