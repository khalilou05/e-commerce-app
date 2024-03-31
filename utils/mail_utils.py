from smtplib import SMTP_SSL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage

# with SMTP_SSL("mail.privateemail.com", 465) as sm:


# print(za)
# za.add_attachment()
# l = sm.login(
#     "contact@code4you.pro",
#     "bakhlalou05",
# )
# mess = MIMEMultipart()
# msg = """
# <html>
# <style>
# p {
#     color: blue;

# }
# </style>
# <body>
# <img src="https://f005.backblazeb2.com/file/apiimages05/Piasalogo.svg" />
# <p><p>
# </body>
# </html>
# """
# mess.attach(MIMEText(msg, "html"))
# print(l)
# s = sm.sendmail("contact@code4you.pro", "contact@code4you.pro", mess.as_string())
# print(s)
