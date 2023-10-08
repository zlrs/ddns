from public_address import get_public_ipv6_address
from dnspod_ddns import DnsPodCN_DDNSClient

domain = 'my_server.com'
subdomain = 'www'
login_token = '<dnspodcn_api_token>'
client = DnsPodCN_DDNSClient(login_token)

my_ipv6_addr = get_public_ipv6_address()
if my_ipv6_addr == '':
    print('WARNING: No IPv6 public address found. Exit now...')
    exit(1)

record_ipv6_addr = client.get_AAAA_record_IPv6_address(subdomain=subdomain, domain_name=domain)
if record_ipv6_addr == '':
    print('WARNING: Can not get record from DDNS API. Exit now...')
    exit(2)

if my_ipv6_addr == record_ipv6_addr:
    print(f'INFO: Address is not changed {my_ipv6_addr}. No need to update.')
    exit(0)

success = client.update_AAAA_record(my_ipv6_addr, subdomain=subdomain, domain_name=domain)
if success:
    print(f'SUCCESS: Updated the AAAA record for {subdomain}.{domain} to {my_ipv6_addr}')
else:
    print(f'ERROR: Failed to update the AAAA record for {subdomain}.{domain} to {my_ipv6_addr}.')
