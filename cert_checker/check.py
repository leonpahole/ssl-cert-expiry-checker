import OpenSSL
import ssl
import socket
import argparse
from datetime import datetime

parser = argparse.ArgumentParser()

# image paths
parser.add_argument('-l', help='Comma separated list of domains')
parser.add_argument(
    '-f', help='Path to file with domains listed (comma, space or new line separated)')

args = parser.parse_args()

domains_to_check = []

if args.l is not None:
    domains_to_check.extend(args.l.split(','))

if args.f is not None:
    f = open(args.f, "r")
    domains_to_check.extend(f.read().splitlines())
    f.close()

if len(domains_to_check) == 0:
    print('No domains to check.')
    exit(0)

print('Please wait...')

domain_info = []

for domain in domains_to_check:

    try:
        cert = ssl.get_server_certificate((domain, 443))
        x509 = OpenSSL.crypto.load_certificate(
            OpenSSL.crypto.FILETYPE_PEM, cert)
        expiry_time = datetime.strptime(
            x509.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ')
        domain_info.append({'domain': domain, 'expiry_time': expiry_time})
    except Exception as exc:
        print(f'Error when validating domain {domain}: {exc}')

domain_info_sorted = list(
    sorted(domain_info, key=lambda item: item['expiry_time']))

for domain in domain_info_sorted:
    print(f'Domain: {domain["domain"]} -> expiry: {domain["expiry_time"]}')
