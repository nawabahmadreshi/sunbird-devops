#!/bin/sh
# Build script
# set -o errexit

ansible-playbook --version

ansible-playbook -i ansible/inventory/${ENV} ansible/deploy.yml --tags "stack-logger" --vault-password-file  /run/secrets/vault-pass
