#!/bin/bash

export SSH_ASKPASS=$4
export DISPLAY=:0
PASSWORD=$1 setsid ssh-copy-id -o StrictHostKeyChecking=no $2@$3