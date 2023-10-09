import sys
import logging
from public_address import get_public_ipv6_address
from dnspod_ddns import DnsPodCN_DDNSClient

domain = 'google.com'
subdomain = 'www'
login_token = 'xxxxxx'
log_filename = 'log.txt'

logger = logging.getLogger()
formatter = logging.Formatter('%(asctime)s %(message)s')


def get_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    return stream_handler


def get_file_handler():
    file_handler = logging.FileHandler(filename=log_filename, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    return file_handler


logger.addHandler(get_stream_handler())
logger.addHandler(get_file_handler())
logger.setLevel(logging.DEBUG)

logger.info('===== Start =====')
my_ipv6_addr = get_public_ipv6_address()
if my_ipv6_addr == '':
    logger.info('No IPv6 public address found. Exit now...')
    sys.exit(1)

client = DnsPodCN_DDNSClient(login_token)
record_ipv6_addr = client.get_AAAA_record_IPv6_address(
    subdomain=subdomain, domain_name=domain)
if record_ipv6_addr == '':
    logger.warning('Can not get record from DDNS API. Exit now...')
    sys.exit(2)

if my_ipv6_addr == record_ipv6_addr:
    logger.warning(f'Address is not changed {
                   my_ipv6_addr}. No need to update.')
    sys.exit(0)

success = client.update_AAAA_record(
    my_ipv6_addr, subdomain=subdomain, domain_name=domain)
if success:
    logger.info(f'SUCCESS: Updated the AAAA record for {
                subdomain}.{domain} to {my_ipv6_addr}')
else:
    logger.info(f'ERROR: Failed to update the AAAA record for {
                subdomain}.{domain} to {my_ipv6_addr}.')
