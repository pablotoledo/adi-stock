import socket
import requests

def check_dns(domain):
    try:
        ip = socket.gethostbyname(domain)
        print(f"{domain} resolves to {ip}")
        return True
    except socket.gaierror:
        print(f"Failed to resolve {domain}")
        return False

def check_http(url):
    try:
        response = requests.get(url, timeout=5)
        print(f"{url} is accessible, status code: {response.status_code}")
        return True
    except requests.RequestException as e:
        print(f"Failed to access {url}: {str(e)}")
        return False

domains_to_check = [
    "finance.yahoo.com",
    "query1.finance.yahoo.com",
    "query2.finance.yahoo.com"
]

print("Checking DNS resolution:")
for domain in domains_to_check:
    check_dns(domain)

print("\nChecking HTTP accessibility:")
for domain in domains_to_check:
    check_http(f"https://{domain}")