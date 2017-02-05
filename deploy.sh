set -x

[ "$TRAVIS_BRANCH" = "master" ] || exit 1
[ "$TRAVIS_PULL_REQUEST" = "false" ] || exit 1
[ "$TRAVIS_PYTHON_VERSION" = "3.5" ] || exit 1

eval "$(ssh-agent -s)"

chmod 600 $TRAVIS_BUILD_DIR/deploy_key
ssh-add $TRAVIS_BUILD_DIR/deploy_key
fab publish:ci
