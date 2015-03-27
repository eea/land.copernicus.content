from plone.app.users.browser.personalpreferences import UserDataPanelAdapter


class EnhancedUserDataPanelAdapter(UserDataPanelAdapter):
    """
    """
    def get_thematic_domain(self):
        value = []
        thematic_domains = self.context.getProperty('thematic_domain', '')
        if thematic_domains:
            value = thematic_domains.split(',')
        return value

    def set_thematic_domain(self, value):
        thematic_domains = ','.join(value)
        return self.context.setMemberProperties({'thematic_domain': thematic_domains})
    thematic_domain = property(get_thematic_domain, set_thematic_domain)

    def get_institutional_domain(self):
        value = []
        institutional_domains = self.context.getProperty('institutional_domain', '')
        if institutional_domains:
            value = institutional_domains.split(',')
        return value

    def set_institutional_domain(self, value):
        institutional_domains = ','.join(value)
        return self.context.setMemberProperties({'institutional_domain': institutional_domains})
    institutional_domain = property(get_institutional_domain, set_institutional_domain)

    def get_disclaimer(self):
        return self.context.getProperty('disclaimer', '')

    def set_disclaimer(self, value):
        return self.context.setMemberProperties({'disclaimer': value})
    disclaimer = property(get_disclaimer, set_disclaimer)
