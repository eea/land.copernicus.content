from plone.app.users.browser.personalpreferences import UserDataPanelAdapter


class EnhancedUserDataPanelAdapter(UserDataPanelAdapter):
    """
    """
    def get_first_name(self):
        first_name = self.context.getProperty('first_name', '')
        return first_name

    def set_first_name(self, value):
        first_name = value
        return self.context.setMemberProperties({'first_name': first_name})
    first_name = property(get_first_name, set_first_name)

    def get_last_name(self):
        last_name = self.context.getProperty('last_name', '')
        return last_name

    def set_last_name(self, value):
        last_name = value
        return self.context.setMemberProperties({'last_name': last_name})
    last_name = property(get_last_name, set_last_name)

    def get_thematic_domain(self):
        value = []
        thematic_domains = self.context.getProperty('thematic_domain', '')
        if thematic_domains:
            value = thematic_domains.split(',')
        return value

    def set_thematic_domain(self, value):
        thematic_domains = ','.join(value)
        return self.context.setMemberProperties(
            {'thematic_domain': thematic_domains})
    thematic_domain = property(get_thematic_domain, set_thematic_domain)

    def get_institutional_domain(self):
        value = []
        institutional_domains = self.context.getProperty(
            'institutional_domain', '')
        if institutional_domains:
            value = institutional_domains.split(',')
        return value

    def set_institutional_domain(self, value):
        institutional_domains = ','.join(value)
        return self.context.setMemberProperties(
            {'institutional_domain': institutional_domains})
    institutional_domain = property(
        get_institutional_domain, set_institutional_domain)

    def get_reason(self):
        return self.context.getProperty('reason', '')

    def set_reason(self, value):
        return self.context.setMemberProperties({'reason': value})
    reason = property(get_reason, set_reason)

    def get_job_title(self):
        return self.context.getProperty('job_title', '')

    def set_job_title(self, value):
        return self.context.setMemberProperties({'job_title': value})
    job_title = property(get_job_title, set_job_title)

    def get_postal_address(self):
        return self.context.getProperty('postal_address', '')

    def set_postal_address(self, value):
        return self.context.setMemberProperties({'postal_address': value})
    postal_address = property(get_postal_address, set_postal_address)

    def get_telephone(self):
        return self.context.getProperty('telephone', '')

    def set_telephone(self, value):
        return self.context.setMemberProperties({'telephone': value})
    telephone = property(get_telephone, set_telephone)

    def get_mobile(self):
        return self.context.getProperty('mobile', '')

    def set_mobile(self, value):
        return self.context.setMemberProperties({'mobile': value})
    mobile = property(get_mobile, set_mobile)

    def get_fax(self):
        return self.context.getProperty('fax', '')

    def set_fax(self, value):
        return self.context.setMemberProperties({'fax': value})
    fax = property(get_fax, set_fax)

    def get_organisation(self):
        return self.context.getProperty('organisation', '')

    def set_organisation(self, value):
        return self.context.setMemberProperties({'organisation': value})
    organisation = property(get_organisation, set_organisation)

    def get_disclaimer(self):
        return self.context.getProperty('disclaimer', '')

    def set_disclaimer(self, value):
        return self.context.setMemberProperties({'disclaimer': value})
    disclaimer = property(get_disclaimer, set_disclaimer)
