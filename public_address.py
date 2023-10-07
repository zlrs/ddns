import urllib3

def get_public_ipv6_address() -> str:
    """
    Get your IPv6 public address when requesting a website.
    """
    return get_public_address('IPv6')

def get_public_ipv4_address() -> str:
    """
    Get your IPv4 public address when requesting a website.
    """
    return get_public_address('IPv4')

def get_public_address(ip_type) -> str:
    """
    Get the public address, depending on |ip_type|.
    """
    http = urllib3.PoolManager()
    check_url = 'http://ip4only.me/api/' if ip_type == 'IPv4' else 'http://ip6only.me/api/'
    try:
        response = http.request("GET", check_url)
    except Exception:
        return ''
    if response.status != 200:
        print(f'response.status is not 200: {response.status}')
        return ''
    
    body = response.data.decode('utf-8')
    # Example response:
    # IPv4,167.220.255.99,v1.1,,,See http://ip6.me/docs/ for api documentation
    # IPv6,2404:f801:9000:18:c4cb:aca5:cf91:4821,v1.1,,,See http://ip6.me/docs/ for api documentation
    elements = body.split(',')
    assert(len(elements) >= 2)
    if ip_type == elements[0]:
        return elements[1]
    return ''


if __name__ == '__main__':
    print(get_public_ipv4_address())
    print(get_public_ipv6_address())
