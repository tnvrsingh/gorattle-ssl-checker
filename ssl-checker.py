import os
import ssl
import socket
import datetime
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

domain_ports = [
    ("expired.badssl.com", 443),
    ("gorattle.com", 443),
]

load_dotenv()

slack_token = os.getenv("slack_token")
slack_channel = os.getenv("slack_channel")
 
def check_ssl_cert_expiry(domain, port):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, port)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as sslsock:
                cert = sslsock.getpeercert()
                not_after_str = cert['notAfter']
                not_after = datetime.datetime.strptime(not_after_str, "%b %d %H:%M:%S %Y %Z")
                days_left = (not_after - datetime.datetime.now()).days
                print(f"Days left for domain {domain}: {days_left}")
                return days_left
    except Exception as e:
        print(f"Error checking SSL certificate for {domain}: {e}")
        pass
    
# Function to send Slack alert
def send_slack_alert(domain, days_left):
    try:
        client = WebClient(token=slack_token)
        message = f"The SSL certificate for {domain} will expire in {days_left} days."
        response = client.chat_postMessage(channel=slack_channel, text=message)
        print(f"Slack alert sent for {domain}: {response['ts']}")
    except SlackApiError as e:
        print(f"Error sending Slack alert for {domain}: {e.response['error']}")    
    
for domain, port in domain_ports:
    days_left = check_ssl_cert_expiry(domain, port)
    if days_left is not None and days_left < 15:
        send_slack_alert(domain, days_left)