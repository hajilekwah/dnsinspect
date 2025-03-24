import dns.resolver

def resolve_dns(domain, record_type):
    try:
        answers = dns.resolver.resolve(domain, record_type)
        results = []
        for rdata in answers:
            results.append(str(rdata))
        return results
    except Exception as e:
        return [f"Error: {str(e)}"]

def resolve_all_dns(domain):
    record_types = ["A", "AAAA", "MX", "NS", "TXT", "CAA", "SOA"]
    all_results = {}

    for rtype in record_types:
        try:
            answers = dns.resolver.resolve(domain, rtype)
            all_results[rtype] = [str(rdata) for rdata in answers]
        except Exception as e:
            all_results[rtype] = [f"Error: {str(e)}"]
    
    return all_results