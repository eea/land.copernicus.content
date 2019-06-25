pipeline {
  agent any

  environment {
        GIT_NAME = "land.copernicus.content"
        SONARQUBE_TAGS = "insitu.copernicus.eu"
        FTEST_DIR = "land/copernicus/content/ftests"
        JSLINT_CUSTOM_FIND = "! -path */static/lib/* ! -path */static/fileslibraryitem/*"
        PYFLAKES_CUSTOM_FIND = "-name docs -prune -o"
        I18N_EXCLUDE = "template-overrides search-by-tags"
    }

  stages {

    stage('Cosmetics') {
      steps {
        parallel(

          "JS Hint": {
            node(label: 'docker') {
              script {
                try {
                  sh '''docker run -i --rm --name="$BUILD_TAG-jshint" -e GIT_SRC="https://github.com/eea/$GIT_NAME.git" -e GIT_NAME="$GIT_NAME" -e GIT_BRANCH="$BRANCH_NAME" -e GIT_CHANGE_ID="$CHANGE_ID" eeacms/jshint'''
                } catch (err) {
                  echo "Unstable: ${err}"
                }
              }
            }
          },

          "CSS Lint": {
            node(label: 'docker') {
              script {
                try {
                  sh '''docker run -i --rm --name="$BUILD_TAG-csslint" -e GIT_SRC="https://github.com/eea/$GIT_NAME.git" -e GIT_NAME="$GIT_NAME" -e GIT_BRANCH="$BRANCH_NAME" -e GIT_CHANGE_ID="$CHANGE_ID" eeacms/csslint'''
                } catch (err) {
                  echo "Unstable: ${err}"
                }
              }
            }
          },

          "PEP8": {
            node(label: 'docker') {
              script {
                try {
                  sh '''docker run -i --rm --name="$BUILD_TAG-pep8" -e GIT_SRC="https://github.com/eea/$GIT_NAME.git" -e GIT_NAME="$GIT_NAME" -e GIT_BRANCH="$BRANCH_NAME" -e GIT_CHANGE_ID="$CHANGE_ID" eeacms/pep8'''
                } catch (err) {
                  echo "Unstable: ${err}"
                }
              }
            }
          },

          "PyLint": {
            node(label: 'docker') {
              script {
                try {
                  sh '''docker run -i --rm --name="$BUILD_TAG-pylint" -e GIT_SRC="https://github.com/eea/$GIT_NAME.git" -e GIT_NAME="$GIT_NAME" -e GIT_BRANCH="$BRANCH_NAME" -e GIT_CHANGE_ID="$CHANGE_ID" eeacms/pylint'''
                } catch (err) {
                  echo "Unstable: ${err}"
                }
              }
            }
          }

        )
      }
    }

    stage('Code') {
      steps {
        parallel(

          "ZPT Lint": {
            node(label: 'docker') {
              sh '''docker run -i --rm --name="$BUILD_TAG-zptlint" -e GIT_BRANCH="$BRANCH_NAME" -e ADDONS="$GIT_NAME" -e DEVELOP="src/$GIT_NAME" -e GIT_CHANGE_ID="$CHANGE_ID" eeacms/plone-test:4 zptlint'''
            }
          },

          "JS Lint": {
            node(label: 'docker') {
              sh '''docker run -i --rm --name="$BUILD_TAG-jslint" -e CUSTOM_FIND="$JSLINT_CUSTOM_FIND" -e GIT_SRC="https://github.com/eea/$GIT_NAME.git" -e GIT_NAME="$GIT_NAME" -e GIT_BRANCH="$BRANCH_NAME" -e GIT_CHANGE_ID="$CHANGE_ID" eeacms/jslint4java'''
            }
          },

          "PyFlakes": {
            node(label: 'docker') {
              sh '''docker run -i --rm --name="$BUILD_TAG-pyflakes" -e CUSTOM_FIND="$PYFLAKES_CUSTOM_FIND" -e GIT_SRC="https://github.com/eea/$GIT_NAME.git" -e GIT_NAME="$GIT_NAME" -e GIT_BRANCH="$BRANCH_NAME" -e GIT_CHANGE_ID="$CHANGE_ID" eeacms/pyflakes'''
            }
          },

          "i18n": {
            node(label: 'docker') {
              sh '''docker run -i --rm --name=$BUILD_TAG-i18n -e EXCLUDE="$I18N_EXCLUDE" -e GIT_SRC="https://github.com/eea/$GIT_NAME.git" -e GIT_NAME="$GIT_NAME" -e GIT_BRANCH="$BRANCH_NAME" -e GIT_CHANGE_ID="$CHANGE_ID" eeacms/i18ndude'''
            }
          }
        )
      }
    }

    stage('Land') {
      when {
        not {
          branch 'insitu-redesign'
        }
      }
      steps {
        parallel(
          "Integration tests": {
            node(label: 'docker') {
              script {
                try {
                  sh '''docker run -i --name="$BUILD_TAG-land" -e GIT_NAME="$GIT_NAME" -e GIT_BRANCH="$BRANCH_NAME" -e GIT_CHANGE_ID="$CHANGE_ID" -e LAND_DOWNLOADS_SRC_PATH="/tmp" -e LAND_DOWNLOADS_DST_PATH="/tmp" eeacms/plone-copernicus-land:devel /debug.sh coverage'''
                  sh '''mkdir -p xunit-reports; docker cp $BUILD_TAG-land:/plone/instance/parts/xmltestreport/testreports/. xunit-reports/'''
                  stash name: "xunit-reports", includes: "xunit-reports/*.xml"
                  sh '''docker cp $BUILD_TAG-land:/plone/instance/src/$GIT_NAME/coverage.xml coverage.xml'''
                  stash name: "coverage.xml", includes: "coverage.xml"
                } finally {
                  sh '''docker rm -v $BUILD_TAG-land'''
                }
                junit 'xunit-reports/*.xml'
              }
            }
          },

          "Functional tests": {
            node(label: 'docker') {
              script {
                try {
                  checkout scm
                  sh '''mkdir -p xunit-functional'''
                  sh '''docker run -d -e ADDONS=$GIT_NAME -e DEVELOP=src/$GIT_NAME -e GIT_BRANCH="$BRANCH_NAME" -e GIT_CHANGE_ID="$CHANGE_ID" -e LAND_DOWNLOADS_SRC_PATH="/tmp" -e LAND_DOWNLOADS_DST_PATH="/tmp" --name=$BUILD_TAG-ft-land eeacms/plone-copernicus-land:devel /debug.sh bin/instance fg'''
                  sh '''timeout 600  wget --retry-connrefused --tries=60 --waitretry=10 -q http://$(docker inspect --format {{.NetworkSettings.IPAddress}} $BUILD_TAG-ft-land):8080/'''
                  sh '''casperjs test $FTEST_DIR/land/*.js --url=$(docker inspect --format {{.NetworkSettings.IPAddress}} $BUILD_TAG-ft-land):8080 --xunit=xunit-functional/ftestsreport.xml'''
                  stash name: "xunit-functional", includes: "xunit-functional/*.xml"
                } catch (err) {
                  sh '''docker logs --tail=100 $BUILD_TAG-ft-land'''
                  throw err
                } finally {
                  sh '''docker stop $BUILD_TAG-ft-land'''
                  sh '''docker rm -v $BUILD_TAG-ft-land'''
                }
                archiveArtifacts '*.png'
                junit 'xunit-functional/ftestsreport.xml'
              }
            }
          }
        )
      }
    }

    stage('InSitu') {
      when {
        allOf {
          branch 'insitu-redesign'
        }
      }
      steps {
        parallel(
          "Integration tests": {
            node(label: 'docker') {
              script {
                try {
                  sh '''docker run -i --name="$BUILD_TAG-insitu" -e GIT_NAME="$GIT_NAME" -e GIT_BRANCH="$BRANCH_NAME" -e GIT_CHANGE_ID="$CHANGE_ID" -e LAND_DOWNLOADS_SRC_PATH="/tmp" -e LAND_DOWNLOADS_DST_PATH="/tmp" eeacms/plone-copernicus-insitu:devel /debug.sh coverage'''
                  sh '''mkdir -p xunit-reports; docker cp $BUILD_TAG-insitu:/plone/instance/parts/xmltestreport/testreports/. xunit-reports/'''
                  stash name: "xunit-reports", includes: "xunit-reports/*.xml"
                  sh '''docker cp $BUILD_TAG-insitu:/plone/instance/src/$GIT_NAME/coverage.xml coverage.xml'''
                  stash name: "coverage.xml", includes: "coverage.xml"
                } finally {
                  sh '''docker rm -v $BUILD_TAG-insitu'''
                }
                junit 'xunit-reports/*.xml'
              }
            }
          },

          "Functional tests": {
            node(label: 'docker') {
              script {
                try {
                  checkout scm
                  sh '''mkdir -p xunit-functional'''
                  sh '''docker run -d -e ADDONS=$GIT_NAME -e DEVELOP=src/$GIT_NAME -e GIT_BRANCH="$BRANCH_NAME" -e GIT_CHANGE_ID="$CHANGE_ID" -e LAND_DOWNLOADS_SRC_PATH="/tmp" -e LAND_DOWNLOADS_DST_PATH="/tmp" --name=$BUILD_TAG-ft-insitu eeacms/plone-copernicus-insitu:devel /debug.sh bin/instance fg'''
                  sh '''timeout 600  wget --retry-connrefused --tries=60 --waitretry=10 -q http://$(docker inspect --format {{.NetworkSettings.IPAddress}} $BUILD_TAG-ft-insitu):8080/'''
                  sh '''casperjs test $FTEST_DIR/insitu/*.js --url=$(docker inspect --format {{.NetworkSettings.IPAddress}} $BUILD_TAG-ft-insitu):8080 --xunit=xunit-functional/ftestsreport.xml'''
                  stash name: "xunit-functional", includes: "xunit-functional/*.xml"
                } catch (err) {
                  sh '''docker logs --tail=100 $BUILD_TAG-ft-insitu'''
                  throw err
                } finally {
                  sh '''docker stop $BUILD_TAG-ft-insitu'''
                  sh '''docker rm -v $BUILD_TAG-ft-insitu'''
                }
                archiveArtifacts '*.png'
                junit 'xunit-functional/ftestsreport.xml'
              }
            }
          }
        )
      }
    }

    stage('Report to SonarQube') {
      when {
        allOf {
          environment name: 'CHANGE_ID', value: ''
        }
      }
      steps {
        node(label: 'swarm') {
          script{
            checkout scm
            dir("xunit-reports") {
              unstash "xunit-reports"
            }
            unstash "coverage.xml"
            dir('xunit-functional') {
              unstash "xunit-functional"
            }
            def scannerHome = tool 'SonarQubeScanner';
            def nodeJS = tool 'NodeJS11';
            withSonarQubeEnv('Sonarqube') {
                sh '''sed -i "s|/plone/instance/src/$GIT_NAME|$(pwd)|g" coverage.xml'''
                sh '''find xunit-functional -type f -exec mv {} xunit-reports/ ";"'''
                sh "export PATH=$PATH:${scannerHome}/bin:${nodeJS}/bin; sonar-scanner -Dsonar.python.xunit.skipDetails=true -Dsonar.python.xunit.reportPath=xunit-reports/*.xml -Dsonar.python.coverage.reportPath=coverage.xml -Dsonar.sources=./land -Dsonar.projectKey=$GIT_NAME-$BRANCH_NAME -Dsonar.projectVersion=$BRANCH_NAME-$BUILD_NUMBER"
                sh '''try=2; while [ \$try -gt 0 ]; do curl -s -XPOST -u "${SONAR_AUTH_TOKEN}:" "${SONAR_HOST_URL}api/project_tags/set?project=${GIT_NAME}-${BRANCH_NAME}&tags=${SONARQUBE_TAGS},${BRANCH_NAME}" > set_tags_result; if [ \$(grep -ic error set_tags_result ) -eq 0 ]; then try=0; else cat set_tags_result; echo "... Will retry"; sleep 60; try=\$(( \$try - 1 )); fi; done'''
            }
          }
        }
      }
    }

  }

  post {
    changed {
      script {
        def url = "${env.BUILD_URL}/display/redirect"
        def status = currentBuild.currentResult
        def subject = "${status}: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'"
        def summary = "${subject} (${url})"
        def details = """<h1>${env.JOB_NAME} - Build #${env.BUILD_NUMBER} - ${status}</h1>
                         <p>Check console output at <a href="${url}">${env.JOB_BASE_NAME} - #${env.BUILD_NUMBER}</a></p>
                      """

        def color = '#FFFF00'
        if (status == 'SUCCESS') {
          color = '#00FF00'
        } else if (status == 'FAILURE') {
          color = '#FF0000'
        }

        emailext (subject: '$DEFAULT_SUBJECT', to: '$DEFAULT_RECIPIENTS', body: details)
      }
    }
  }
}
