#!/usr/bin/env bash

for folder in $(ls ./images);do
	echo ">----------------------------<"
	echo "Build image: eagle-${folder}"
	docker build -t eagle-${folder} ./images/${folder}
done
