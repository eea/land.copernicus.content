# ============================================================================
# EXAMPLE ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s plonetraining.testing -t test_search.robot --all
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
# $ bin/robot src/plonetraining/testing/tests/robot/test_search.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
#        Should Be Equal    ${MESSAGE}    Hello, world
# ============================================================================

*** Variables ****************************************************************
${DOMAIN URL}      http://localhost:8080/copernicus
${FAKE_USER_NAME}  fake user
${FAKE_USER_PASS}  fake pass
${REAL_USER_NAME}  XXXXXXXXX
${REAL_USER_PASS}  YYYYYYYYY

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************


Scenario: Search is performing
  Given the search form
   When I select a category
   Then results are updated

# --- Given ------------------------------------------------------------------

the search form
  Go To  ${DOMAIN URL}/@@search
  Wait until page contains  Login Name
  Wait until page contains  Password


# --- WHEN -------------------------------------------------------------------

I enter invalid credentials
  Input Text  __ac_name  ${FAKE_USER_NAME}
  Input Text  __ac_password  ${FAKE_USER_PASS}
  Click Button  Log in


# --- THEN -------------------------------------------------------------------

Login failed
  Wait until page contains  Login failed
  Page should contain  Login failed


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
Then I will log out
  Click Element  xpath=//a[normalize-space()="Log out"]
  Wait until page contains  Log in
  Page should contain  Log in
