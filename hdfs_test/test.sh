#!/bin/bash
rm -rf testCand
hadoop fs -get /user/admin/testing/test ./testCand
python CheckHash.py testCand
