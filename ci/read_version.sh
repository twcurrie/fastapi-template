#!/bin/sh

git log -1 --pretty=format:'{"link": "http://github.com/hinge-health/eligibility-service/commit/%H",%n"hash":"%h",%n"author":"%an",%n"date":"%ad",%n"email":"%aE",%n"message":"%s",%n"commitDate":"%ai",%n"age":"%cr"}' | cat
