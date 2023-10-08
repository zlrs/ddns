from third_party.dnspod_python.dnspod import apicn


class DDNSClient:
    """
    The abstract class for all DDNS clients.
    """

    def __init__(self):
        pass

    def get_AAAA_record_IPv6_address(self, subdomain, domain_name) -> str:
        """
        Get the IPv6 address of the domain.
        """
        return ''

    def update_AAAA_record(self, ipv6_addr, subdomain, domain_name) -> bool:
        """
        Update an AAAA record that resolves |domain_name| to |ipv6_addr|.
        The record MUST be exist.
        """
        return False

    def update_A_record(self, ipv4_addr, subdomain, domain_name) -> bool:
        """
        Update an A record that resolves |domain_name| to |ipv6_addr|.
        The record MUST be exist.
        Example: update_A_record('1.1.1.1', 'www', 'google.com')
        """
        return False


class DnsPodCN_DDNSClient(DDNSClient):
    """
    The implementation of DDNSClient for DnsPodCN https://dnspod.cn/.
    """

    def __init__(self, token):
        self.login_token = token
        self.line_type = '默认'.encode("utf8")
        self.ttl = 600
        super().__init__()

    def get_AAAA_record_IPv6_address(self, subdomain, domain_name) -> str:
        record: dict = self._get_record('AAAA', subdomain, domain_name)
        ipv6_addr = record.get('value', '')
        return ipv6_addr

    def update_AAAA_record(self, ipv6_addr, subdomain, domain_name) -> bool:
        record_id = self.get_record_id('AAAA', subdomain, domain_name)
        if record_id <= 0:
            return False

        # https://docs.dnspod.cn/api/record-modify/
        api = apicn.RecordModify(record_id=record_id, sub_domain=subdomain, record_type='AAAA', record_line=self.line_type,
                                 value=ipv6_addr, ttl=self.ttl, domain_or_domain_id=apicn.DomainOrDomainId(domain_name), login_token=self.login_token)
        res_record = api().get('record', {})
        res_record_id = res_record.get('id')

        assert record_id == res_record_id
        return record_id == res_record_id

    def update_A_record(self, ipv4_addr, subdomain, domain_name) -> bool:
        record_id = self.get_record_id('A', subdomain, domain_name)
        if record_id <= 0:
            return False

        # https://docs.dnspod.cn/api/record-modify/
        api = apicn.RecordModify(record_id=record_id, sub_domain=subdomain, record_type='A', record_line=self.line_type,
                                 value=ipv4_addr, ttl=self.ttl, domain_or_domain_id=apicn.DomainOrDomainId(domain_name), login_token=self.login_token)
        res_record = api().get('record', {})
        res_record_id = res_record.get('id')

        assert record_id == res_record_id
        return record_id == res_record_id

    def get_record_id(self, record_type: str, subdomain, domain_name) -> int:
        """
        Search for a record and return its ID.
        Return value 0 represents falure.
        """
        record: dict = self._get_record(record_type, subdomain, domain_name)
        record_id_str = record.get('id')
        if record_id_str and len(record_id_str):
            return int(record_id_str)
        return 0

    def _get_record(self, record_type: str, subdomain, domain_name) -> dict:
        # https://docs.dnspod.cn/api/record-list/
        record_list = apicn.RecordList(domain_or_domain_id=apicn.DomainOrDomainId(
            domain_name), login_token=self.login_token)
        records: list = record_list().get('records', [])

        filtered_records = list(filter(lambda r: r.get(
            'name') == subdomain and r.get('type') == record_type, records))
        # There should be only 1 record for a type and name, right?
        assert len(filtered_records) == 1
        return filtered_records[0]


if __name__ == "__main__":
    dnspod = DnsPodCN_DDNSClient('')
    print(dnspod.update_A_record('1.1.1.5', 'test_apicn', 'your_domain.com'))
