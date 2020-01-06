# ============================================================================
# EXAMPLE ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s plonetraining.testing -t test_download.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src
#     plonetraining.testing.testing.PLONETRAINING_TESTING_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_download.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Variables ****************************************************************
${DOMAIN URL}      http://copernicus.europa.eu

${number_of_items}  0
${number_of_items_search}   0

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************


Scenario: Technical library search check
  Given technical library
    When I perform a search
    Then number of results is changed

*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

technical library
  Go To  ${DOMAIN URL}/user-corner/technical-library

# --- WHEN -------------------------------------------------------------------

I perform a search
  Wait until page contains  Search:

#--- THEN --------------------------------------------------------------------

number of results is changed
  ${number_of_items} =    Get Text    xpath=//div[@class="dataTables_info"]
  Input Text  xpath=//input[@type="search"]   g

  Sleep   2
  ${number_of_items_search} =    Get Text    xpath=//div[@class="dataTables_info"]

  Log To Console    [${number_of_items}]
  Log To Console    [${number_of_items_search}]

  Should Not Be Equal As Strings    ${number_of_items}    ${number_of_items_search}
