## Script (Python) "at_download"
##title=Download a file keeping the original uploaded filename
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath

""" Start customization """
parents = context.aq_inner.aq_parent.absolute_url().split('/')[3:]
parents_paths = [
    '/' + '/'.join(parents[0:x+1]) + '/' for x in range(0, len(parents))]
find_workspace = [
    context.restrictedTraverse(x) for x in parents_paths if
    context.restrictedTraverse(x).portal_type == "eea.meeting.workspace"]

if len(find_workspace) > 0:
    workspace = find_workspace[0]
    has_access = workspace.restrictedTraverse("current_user_has_access")()
    # return has_access
""" End customization """

if traverse_subpath:
    field = context.getWrappedField(traverse_subpath[0])
else:
    field = context.getPrimaryField()
if not field.checkPermission('r', context):
    from zExceptions import Unauthorized
    raise Unauthorized('Field %s requires %s permission' % (field, field.read_permission))
if not hasattr(field, 'download'):
    from zExceptions import NotFound
    raise NotFound
return field.download(context)
