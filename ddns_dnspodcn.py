from public_address import get_public_ipv6_address
from dnspod_ddns import DnsPodCN_DDNSClient

my_ipv6_addr = get_public_ipv6_address()
if not my_ipv6_addr or len(my_ipv6_addr) == 0:
    exit(0)

domain = 'my_server.com'
subdomain = 'www'
login_token = '<dnspodcn_api_token>'
client = DnsPodCN_DDNSClient(login_token)
success = client.update_AAAA_record(my_ipv6_addr, subdomain=subdomain, domain_name=domain)
if success:
    print(f'SUCCESS: Updated the AAAA record for {subdomain}.{domain} to {my_ipv6_addr}')
else:
    print(f'ERROR: Failed to update the AAAA record for {subdomain}.{domain} to {my_ipv6_addr}.')
