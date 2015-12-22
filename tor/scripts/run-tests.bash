#!/bin/bash -x

HERE=$(cd $(dirname "$0"); pwd)

$HERE/dev-teardown.bash
set -e

$HERE/dev-setup.bash

for test in $(ls $HERE/../tests/[0-9]*); do
	$test
done

