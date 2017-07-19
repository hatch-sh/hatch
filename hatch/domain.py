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
    def parse(domainStr):

        if domainStr is None:
            return None

        parts = domainStr.split(".")
        main_parts = parts[-2:]
        sub_parts = parts[0:-2]

        return Domain(
            ".".join(sub_parts) if len(sub_parts) is not 0 else None,
            ".".join(main_parts)
        )
