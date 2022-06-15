from twilio.rest import Client
import smtplib
account_sid = "xxx"
auth_token = "xxx"
my_email = "xxx"
password = "xxx"


class NotificationManager:
    def __init__(self):
        self.client = Client(account_sid, auth_token)

    def send_message(self, message_text):
        message = self.client.messages.create(
            body=message_text,
            from_='+12059645513',
            to='xxx'
        )
        print(message.sid)

    def send_email(self, email, message):
        with smtplib.SMTP("smtp.mail.ru", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            try:
                connection.sendmail(from_addr=my_email, to_addrs=email,
                                    msg=f"Subject:New low price flight!\n\n{message}")
                print("Message sended")
            except UnicodeEncodeError:
                print("Problems with link")
