# from Products.CMFCore.utils import getToolByName
#
# site = self.context.portal_url.getPortalObject()
#
# mt = getToolByName(site, 'portal_membership')
# md = getToolByName(site, 'portal_memberdata')
# ut = getToolByName(self, 'acl_users')
#
# all_members = [x for x in md._members.keys()]
# local_members = mt.listMemberIds()
# eionet_members = [x for x in all_members if x not in local_members]
#
# user = mt.getAuthenticatedMember()
# user.bobobase_modification_time()
#
# mt.getMemberById('gonchvic').bobobase_modification_time()
#
# (Pdb) md.getMemberDataContents()
# [{'orphan_count': 669, 'member_count': 14386}]
# members = md._members

# DateTime('2015/05/12 10:54:7.022828 GMT+3')
# user
# <MemberData at /copernicus/portal_memberdata/ghitab ...
# user.getUser()
# <PloneUser 'ghitab'>

# userid = "someid"
# site.acl_users.get("ldap-plugin").acl_users.searchUsers(uid=userid)[0]
# {
#   'dn': 'uid=someid,ou=Users,o=EIONET,l=Europe',
#   'mail': 'someid@eaudeweb.ro', 'uid': 'someid',
#   'sn': 'Someid', 'cn': 'Some Name'
# }
# mt.getMemberById('someid').getProperty('thematic_domain', '')
# 'Agriculture'

# user.getUser().getOrderedPropertySheets()[0])
# user.getUser().getOrderedPropertySheets()[0].propertyItems()
# [('email', u'ghita.bizau@eaudeweb.ro'), ('fullname', u'Ghita Bizau')]
# user.getUser().getOrderedPropertySheets()[1].propertyItems()
# [('email', 'ghita_bizau@yahoo.com'), ('portal_skin', ''), ('listed', True),
#  ('login_time', DateTime('2017/12/05 15:40:40.806253 GMT+2')),
#  ('last_login_time', DateTime('2017/11/20 14:04:8.161584 GMT+2')),
#  ('fullname', ''), ('error_log_update', 0.0), ('home_page', ''),
#  ('location', ''), ('description', ''), ('language', ''),
#  ('ext_editor', False), ('wysiwyg_editor', ''), ('visible_ids', False),
#  ('first_name', u'Ghita'), ('last_name', u'Bizau'),
#  ('thematic_domain', 'Agriculture'), ('institutional_domain', 'Education'),
#  ('reason', ''), ('job_title', ''),
#  ('postal_address', u'Fundatia Life Cuza Voda \nlanga Biserica cu Luna'),
#  ('telephone', ''), ('mobile', ''), ('fax', ''), ('organisation', '')]

# len(membership_tool.listMemberIds())
# 13718

# user = mt.getMemberById('ghitab')
# user.getUser().getPropertysheet(
#     'mutable_properties').getProperty('last_login_time')
# DateTime('2017/12/05 15:40:40.806253 GMT+2')
