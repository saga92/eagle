#!/usr/bin/env bash

echo "------------------------------"
echo "Please Input the type of test:"
echo -e "Integratetest:--->1 \nUnit:------>2"
read type
case ${type} in
	1)
		echo "Test intergrate_test for eagle:"
		echo "------------------------------"
		cd ./integratetest && python -m unittest discover -v
		rm -rf *.log
		;;
	2)
		echo "Test unit_test for eagle"
		echo "------------------------------"
		cd ./unit && python -m unittest discover -v
		rm -rf *.log
		;;
	*)
		echo "Error: The input is wrong!!"
		;;
esac

