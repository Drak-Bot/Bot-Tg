import socket
import whois


def domain_info(domain):
    """
    Retrieve WHOIS information for the specified domain.

    Parameters:
    - domain (str): The domain to look up.

    Returns:
    - dict: A dictionary containing WHOIS information.
    """
    try:
        w = whois.whois(domain)
        return w.__dict__
    except Exception as e:
        return {'error': str(e)}


def dns_records(domain):
    """
    Retrieve DNS records for the specified domain.

    Parameters:
    - domain (str): The domain to look up.

    Returns:
    - dict: A dictionary containing DNS records.
    """ 
    try:
        records = {"A": socket.gethostbyname(domain)}
        return records
    except Exception as e:
        return {'error': str(e)}
