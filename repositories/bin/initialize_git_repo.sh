#!/bin/bash
# Pass the full uri of the repo, typically file:///path/to/repo
if [ $1 -eq 0 ]  # Must have command-line args to demo script.
then
  echo "Please invoke this script with a repository uri."
  exit $E_NO_ARGS
fi  

mkdir /tmp/temprepo
cd /tmp/temprepo
git init
touch README.txt
git add .
git commit -a -m 'Initial commit'
git remote add origin $1
git push origin master
cd /tmp
rm -Rf temprepo
