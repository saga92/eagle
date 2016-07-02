#!/usr/bin/env bash

echo "------------------------------"
echo "Please Input the type of test:"
echo -e "Tempest:--->1 \nUnit:------>2"
read type
case ${type} in
	1)
		cd ./tempest && python -m unittest discover -v
		rm -rf *.log
		;;
	2)
		cd unit && python -m unittest discover -v
		rm -rf *.log
		;;
	*)
		echo "Error: The input is wrong!!"
		;;
esac

