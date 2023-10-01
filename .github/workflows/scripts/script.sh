#!/usr/bin/env bash
# coding=utf-8

# WARNING: DO NOT EDIT!
#
# This file was generated by plugin_template, and is managed by it. Please use
# './plugin-template --github pulp_helm' to update this file.
#
# For more info visit https://github.com/pulp/plugin_template

set -mveuo pipefail

# make sure this script runs at the repo root
cd "$(dirname "$(realpath -e "$0")")"/../../..
REPO_ROOT="$PWD"

source .github/workflows/scripts/utils.sh

export POST_SCRIPT=$PWD/.github/workflows/scripts/post_script.sh
export POST_DOCS_TEST=$PWD/.github/workflows/scripts/post_docs_test.sh
export FUNC_TEST_SCRIPT=$PWD/.github/workflows/scripts/func_test_script.sh

# Needed for both starting the service and building the docs.
# Gets set in .github/settings.yml, but doesn't seem to inherited by
# this script.
export DJANGO_SETTINGS_MODULE=pulpcore.app.settings
export PULP_SETTINGS=$PWD/.ci/ansible/settings/settings.py

export PULP_URL="https://pulp"

if [[ "$TEST" = "docs" ]]; then
  if [[ "$GITHUB_WORKFLOW" == "Helm CI" ]]; then
    pip install towncrier==19.9.0
    towncrier --yes --version 4.0.0.ci
  fi
  cd docs
  make PULP_URL="$PULP_URL" diagrams html
  tar -cvf docs.tar ./_build
  cd ..

  if [ -f $POST_DOCS_TEST ]; then
    source $POST_DOCS_TEST
  fi
  exit
fi

REPORTED_STATUS="$(pulp status)"

if [[ "${RELEASE_WORKFLOW:-false}" == "true" ]]; then
  REPORTED_VERSION="$(echo $REPORTED_STATUS | jq --arg plugin helm --arg legacy_plugin pulp_helm -r '.versions[] | select(.component == $plugin or .component == $legacy_plugin) | .version')"
  response=$(curl --write-out %{http_code} --silent --output /dev/null https://pypi.org/project/pulp-helm/$REPORTED_VERSION/)
  if [ "$response" == "200" ];
  then
    echo "pulp_helm $REPORTED_VERSION has already been released. Skipping running tests."
    exit
  fi
fi

echo "machine pulp
login admin
password password
" | cmd_user_stdin_prefix bash -c "cat >> ~pulp/.netrc"
# Some commands like ansible-galaxy specifically require 600
cmd_user_stdin_prefix bash -c "chmod 600 ~pulp/.netrc"

cd ../pulp-openapi-generator
if [ "$(echo "$REPORTED_STATUS" | jq -r '.versions[0].package')" = "null" ]
then
  # We are on an old version of pulpcore without package in the status report
  for app_label in $(echo "$REPORTED_STATUS" | jq -r '.versions[].component')
  do
    if [ "$app_label" = "core" ]
    then
      item=pulpcore
    else
      item="pulp_${app_label}"
    fi
    ./generate.sh "${item}" python
    cmd_prefix pip3 install "/root/pulp-openapi-generator/${item}-client"
    sudo rm -rf "./${item}-client"
  done
else
  for item in $(echo "$REPORTED_STATUS" | jq -r '.versions[].package|sub("-"; "_")')
  do
    ./generate.sh "${item}" python
    cmd_prefix pip3 install "/root/pulp-openapi-generator/${item}-client"
    sudo rm -rf "./${item}-client"
  done
fi

cd $REPO_ROOT

cat unittest_requirements.txt | cmd_stdin_prefix bash -c "cat > /tmp/unittest_requirements.txt"
cat functest_requirements.txt | cmd_stdin_prefix bash -c "cat > /tmp/functest_requirements.txt"
cmd_prefix pip3 install -r /tmp/unittest_requirements.txt -r /tmp/functest_requirements.txt

CERTIFI=$(cmd_prefix python3 -c 'import certifi; print(certifi.where())')
cmd_prefix bash -c "cat /etc/pulp/certs/pulp_webserver.crt  | tee -a "$CERTIFI" > /dev/null"

# check for any uncommitted migrations
echo "Checking for uncommitted migrations..."
cmd_user_prefix bash -c "django-admin makemigrations helm --check --dry-run"

# Run unit tests.
cmd_user_prefix bash -c "PULP_DATABASES__default__USER=postgres pytest -v -r sx --color=yes -p no:pulpcore --pyargs pulp_helm.tests.unit"

# Run functional tests
if [[ "$TEST" == "performance" ]]; then
  if [[ -z ${PERFORMANCE_TEST+x} ]]; then
    cmd_user_prefix bash -c "pytest -vv -r sx --color=yes --pyargs --capture=no --durations=0 pulp_helm.tests.performance"
  else
    cmd_user_prefix bash -c "pytest -vv -r sx --color=yes --pyargs --capture=no --durations=0 pulp_helm.tests.performance.test_$PERFORMANCE_TEST"
  fi
  exit
fi

if [ -f $FUNC_TEST_SCRIPT ]; then
  source $FUNC_TEST_SCRIPT
else

    if [[ "$GITHUB_WORKFLOW" == "Helm Nightly CI/CD" ]] || [[ "${RELEASE_WORKFLOW:-false}" == "true" ]]; then
        cmd_user_prefix bash -c "pytest -v -r sx --color=yes --suppress-no-test-exit-code --pyargs pulp_helm.tests.functional -m parallel -n 8 --nightly"
        cmd_user_prefix bash -c "pytest -v -r sx --color=yes --pyargs pulp_helm.tests.functional -m 'not parallel' --nightly"

    
        cmd_user_prefix bash -c "pytest -v -r sx --color=yes --suppress-no-test-exit-code --pyargs pulpcore.tests.functional -m 'from_pulpcore_for_all_plugins and parallel' -n  8 --nightly"
        cmd_user_prefix bash -c "pytest -v -r sx --color=yes --suppress-no-test-exit-code --pyargs pulpcore.tests.functional -m 'from_pulpcore_for_all_plugins and not parallel'  --nightly"
    
    else
        cmd_user_prefix bash -c "pytest -v -r sx --color=yes --suppress-no-test-exit-code --pyargs pulp_helm.tests.functional -m parallel -n 8"
        cmd_user_prefix bash -c "pytest -v -r sx --color=yes --pyargs pulp_helm.tests.functional -m 'not parallel'"

    
        cmd_user_prefix bash -c "pytest -v -r sx --color=yes --suppress-no-test-exit-code --pyargs pulpcore.tests.functional -m 'from_pulpcore_for_all_plugins and parallel' -n  8"
        cmd_user_prefix bash -c "pytest -v -r sx --color=yes --suppress-no-test-exit-code --pyargs pulpcore.tests.functional -m 'from_pulpcore_for_all_plugins and not parallel'"
    
    fi

fi

if [ -f $POST_SCRIPT ]; then
  source $POST_SCRIPT
fi