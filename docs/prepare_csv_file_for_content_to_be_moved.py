""" Prepare csv file for @@aliases-controlpanel
    Make sure the results are as expected. It's just a sketch.

    To be added as useful script in ZMI: .maintenance folder.
"""
SITE_INSTANCE = "/copernicus"   # Example: /copernicus
FOLDER = "/in-situ"  # Where are the items now (before moving them)?
# Example: Use /old-folder for /copernicus/old-folder
NEW_FOLDER = "/imagery-in-situ"  # Where will be the items after moving them?
# Example: Use /some/path/new-folder for /copernicus/some/path/new-folder
INCLUDE_PARENT_FOLDER = True  # Add a rule for parent folder? False: only
# children

"""
Example result:
/old-folder,/some/path/new-folder                                  <<< optional
/old-folder/page1,/some/path/new-folder/page1
/old-folder/page2,/some/path/new-folder/page2
/old-folder/file1,/some/path/new-folder/file1
/old-folder/folder5/page7,/some/path/new-folder/folder5/page7
"""

catalog = context.portal_catalog


def relative_path(obj):
    """ Example result (site instance not included): /some/path/new-folder """
    return "/" + "/".join(obj.getPhysicalPath()[2:])


def exclude_old_parent(item):
    """ /old-folder/folder5/page7 -> /folder5/page7
    """
    return "/" + "/".join(item.split("/")[2:])


path = SITE_INSTANCE + FOLDER
items = [
    relative_path(b.getObject()) for b in catalog(path={"query": path})]

if INCLUDE_PARENT_FOLDER is False:
    items = [x for x in items if x != FOLDER]

result = []
for item in items:
    if item == FOLDER:
        result.append(item + "," + NEW_FOLDER)
    else:
        result.append(item + "," + NEW_FOLDER + exclude_old_parent(item))

for x in result:
    print x

return printed
