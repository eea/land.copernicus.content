# DISABLED
#from zExceptions import NotFound
#raise NotFound

geotags = context.portal_vocabularies.geotags
# geotags = context.portal_vocabularies.biotags
#geotags = context.portal_vocabularies.countries_mapping

for name, group in geotags.items():
  print '<element key="%s">' % name
  print '  <element key="title">%s</element>' % group.title_or_id()
  for cname, country in group.items():
    print '  <element key="%s">%s</element>' % (cname, country.title_or_id())
  print '</element>'

return printed
