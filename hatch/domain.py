import tldextract

class Domain(object):

    def __init__(self, subdomain, main_domain):
        self.subdomain = subdomain
        self.main_domain = main_domain

    @property
    def full_domain(self):
        if self.subdomain:
            return "{}.{}".format(self.subdomain, self.main_domain)
        return self.main_domain

    @staticmethod
    def parse(domain_str):

        if domain_str is None:
            return None

        parsed = tldextract.extract(domain_str)

        return Domain(
            parsed.subdomain,
            "{}.{}".format(parsed.domain, parsed.suffix)
        )
