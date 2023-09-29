import ssl
import socket
import datetime

domain_ports = [
    ("expired.badssl.com", 443),
    ("gorattle.com", 443),
]
 
def check_ssl_cert_expiry(domain, port):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((domain, port)) as sock:
            print(sock)
            with context.wrap_socket(sock, server_hostname=domain) as sslsock:
                print(sslsock)
                cert = sslsock.getpeercert()
                print(cert)
                not_after_str = cert['notAfter']
                print(not_after_str)
                not_after = datetime.datetime.strptime(not_after_str, "%b %d %H:%M:%S %Y %Z")
                days_left = (not_after - datetime.datetime.now()).days
                print(f"Days left for domain {domain}: {days_left}")
                return days_left
    except Exception as e:
        print(f"Error checking SSL certificate for {domain}: {e}")
        pass
    
    
# def send_slack_alert():
    
for domain, port in domain_ports:
    days_left = check_ssl_cert_expiry(domain, port)
    if days_left is not None and days_left < 15:
        send_slack_alert(domain, days_left)