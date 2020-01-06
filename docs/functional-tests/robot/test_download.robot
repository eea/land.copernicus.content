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
${LOCAL URL}      http://localhost:8080/copernicus/local
${REAL_USER_NAME}  XXXXXXXXXXX
${REAL_USER_PASS}  YYYYYYYYYYY

${ELEMENT_LINK_LOCAL} xpath=//li#portaltab-local/a
${ELEMENT_LINK_ALBUM} xpath=//div[@class="photoAlbumEntry"]

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************


Scenario: Download file as a member
  Given a login form
   When I enter valid credentials
   Then I am logged in
   Then I go to download section

*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a login form
  Go To  ${DOMAIN URL}/login
  Wait until page contains  Login Name
  Wait until page contains  Password

# --- WHEN -------------------------------------------------------------------

I enter valid credentials
  Input Text  __ac_name   ${REAL_USER_NAME}
  Input Text  __ac_password  ${REAL_USER_PASS}
  Click Button  Log in


# --- THEN -------------------------------------------------------------------

I am logged in
  Wait until page contains  Log out
  Page should contain  Log out


# --- THEN -------------------------------------------------------------------
Then I go to download section
  Click Element  xpath=//li[@id="portaltab-local"]/a
  Wait until page contains element  xpath=//div[@class="photoAlbumEntry"][2]/a
  Click Element   xpath=//div[@class="photoAlbumEntry"][2]/a
  Wait until page contains element  xpath=//div[@class="photoAlbumEntry"][1]/a
  Click Element   xpath=//div[@class="photoAlbumEntry"][1]/a
  Click Element  xpath=//a[normalize-space()="Download"]
  Wait until page contains element  xpath=//th[normalize-space()="Size"]
  Click ELEMENT   xpath=//th[normalize-space()="Size"]
  #Wait until page contains   xpath=//table[@id="data-table-download"]/tbody/tr[1]//input
  Click Element   xpath=//table[@id="data-table-download"]/tbody/tr[1]//input
  #Wait until page contains  contains xpath=//button[@id="button-download-selected"]
  Click Element   xpath=//button[@id="button-download-selected"]
  Wait until page contains    We're preparing your archive.
