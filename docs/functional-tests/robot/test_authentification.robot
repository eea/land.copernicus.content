# ============================================================================
# EXAMPLE ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s plonetraining.testing -t test_authentification.robot --all
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
# $ bin/robot src/plonetraining/testing/tests/robot/test_authentification.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Variables ****************************************************************
${DOMAIN URL}      http://localhost:8080/copernicus
&{CREDENTIALS_REAL_USER}    username=YYYYYYYYYYY   password=XXXXXXXXX
@{CREDENTIALS_FAKE_USER}    fake user   fake password

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************


Scenario: Not being a member I will not authenticate to the website
  [Documentation]  Example of a BDD-style (Behavior-driven development) test.
  Given a login form
   When I enter invalid credentials
   Then login failed


Scenario: As a member I want to be able to log into the website
  [Documentation]  Example of a BDD-style (Behavior-driven development) test.
  Given a login form
   When I enter valid credentials
   Then I am logged in


Scenario: I will logout from website as a member
  [Documentation]  Example of a BDD-style (Behavior-driven development) test.
  Given a login form
    When I enter valid credentials
    Then I am logged in
    Then I will log out

*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a login form
  Go To  ${DOMAIN URL}/login
  Wait until page contains  Login Name
  Wait until page contains  Password


# --- WHEN -------------------------------------------------------------------

I enter invalid credentials
  Input Text  __ac_name  @{CREDENTIALS_FAKE_USER}[0]
  Input Text  __ac_password  @{CREDENTIALS_FAKE_USER}[1]
  Click Button  Log in


# --- THEN -------------------------------------------------------------------

Login failed
  Wait until page contains  Login failed
  Page should contain  Login failed


# --- WHEN -------------------------------------------------------------------

I enter valid credentials
  Input Text  __ac_name   &{CREDENTIALS_REAL_USER}[username]
  Input Text  __ac_password  &{CREDENTIALS_REAL_USER}[password]
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
