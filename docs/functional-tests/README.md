# EEA Land Copernicus test scenarios

### Test landfiles
Run as admin /test_all_landfiles

Status: "OK" or "Provided URL does not resolve to a file!"

### Add browser extension
The tests were run on chrome browser. For testing the functionality use according to your preffered browser:
- [selenium chrome extension](https://chrome.google.com/webstore/detail/selenium-ide/mooikfkahbdckldjjndioackbalphokd?hl=en)
- [selenium firefox add-on](https://addons.mozilla.org/en-US/firefox/addon/selenium-ide/)

### Download tests
Download from repository the tests configuration file: https://github.com/eea/land.copernicus.content/blob/master/docs/functional-tests/EEA-LAND-COPERNICUS.side

### Opening Selenium tests in extenstion/add-on

Open Selenium IDE (click on the icon on your toolbar
![](https://github.com/eea/land.copernicus.content/raw/master/docs/functional-tests/images/001-open-selenium.png)

Select open an existing project
![](https://github.com/eea/land.copernicus.content/raw/master/docs/functional-tests/images/002-open-project.png)

Change the values for REAL_USER_NAME and REAL_USER_PASSWORD to a valid account
![](https://github.com/eea/land.copernicus.content/raw/master/docs/functional-tests/images/004-change-real-username.png)

### Before running tests
1) Clear user password saved by default for the browser used in testing.
 - Chrome (https://support.google.com/chrome/answer/95606)
 - FireFox (https://support.mozilla.org/en-US/kb/password-manager-remember-delete-edit-logins)
 - Edge (https://support.microsoft.com/en-us/help/4028534/microsoft-edge-save-or-forget-passwords)
 - Safari (https://support.apple.com/guide/safari/passwords-sfri40599/mac)
2) Set the correct domain name.
3) Make sure you changed to set the REAL_USER_NAME and REAL_USER_PASSWORD case:
- 000_2 Lost password valid username
- 002 Login success
4) User used in test should have the personal settings completed in order to run the 'Download' functionality

### Running all tests

Before running all tests, ensure that you are not logged in the browser

### Individual tests
You can run the tests for partial testing. Review the test you wish to run to check if their are requirments

##### Lost Password
Check that you are not logged in. Will test with a fake and real username

##### Login failed
Testing this case you need to be sure that you are not logged in the browser. Will test also:
- Login With Empty Password Should Fail
- Login With Empty Username Should Fail
- Login With Empty Username And Password Should Fail
- Login With Invalid Username Should Fail
- Login With Invalid Password Should Fail
- Login With Invalid Username And Invalid Password Should Fail

By default it is populated with dummy data:  FAKE_USER_NAME and FAKE_USER_PASSWORD. In case you want to test for ex a expired/not validated or any case a user credential are not valid change the values
![](https://github.com/eea/land.copernicus.content/raw/master/docs/functional-tests/images/003-change-fake-username.png)

##### Login success
You should not be logged in for this test. The credential should be set for REAL_USER_NAME and REAL_USER_PASSWORD

##### Logout
We need a user to be logged in for a valid test.

##### Search
Will open search browser and assume that we have at least one category and a click on it will aspect search results to be visible

##### Download file
For this test we need a logged user. First we check the local menu, and click on first items and then Download. We order the results ascending by file size to ensure that the test will download a small one

##### Technical library
Will open technical library link and perform a search by default for "g"(we notice document title with "guide"). Using this search we should have results, but using "dummy_search_text" we should receive no results.

##### Map is loading
We repeat steps from download section, but we will not click Download button. If map is loading we check for a text inside of iframe

##### Global menu
This is a external website. Clicking on the global menu will load external file.
[git-repo-url]: <https://github.com/eea/land.copernicus.content>
