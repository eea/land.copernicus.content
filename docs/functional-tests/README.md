# EEA Land Copernicus test scenarios

### Add browser extenstion
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
Edit the file and change the values for REAL_USER_NAME and REAL_USER_PASSWORD to a valid account
![](https://github.com/eea/land.copernicus.content/raw/master/docs/functional-tests/images/003-change-real-username.png)

### Running all tests

Before running all tests, ensure that you are not logged in the browser

### Individual tests
You can run the tests for partial testing. Review the test you wish to run to check if their are requirments

##### Login failed
Testing this case you need to be sure that you are not logged in the browser. Also we populated with dummy data:  FAKE_USER_NAME and FAKE_USER_PASSWORD. In case you want to test for ex a expired/not validated or any case a user credential are not valid change the values
![](https://github.com/eea/land.copernicus.content/raw/master/docs/functional-tests/images/003-change-fake-username.png)

##### Login success
You should not be logged in for this test. The credential should be set for REAL_USER_NAME and REAL_USER_PASSWORD

##### Logout
We need a user to be logged in for a valid test.



[git-repo-url]: <https://github.com/eea/land.copernicus.content>
