#!/bin/sh
HERE=`pwd`
RESULT=${HERE}/docker
echo ${RESULT}
cd ${RESULT}
code=$(make run)
#echo "ls ${code}"
echo $code
echo "test1"
code=${code#*ubuntu:20.04-sniper-yixian} 
echo $code
echo "testtest"
docker exec -it $code bash -c "cd ../simulationcontrol; export PYTHONIOENCODING='utf-8';python3 run.py"
echo "test2"
#echo `pwd`
#cd ..
#cd simulationcontrol
#python3 run.py
