#!/bin/sh
HERE=`pwd`
CONTROL=${HERE}/simulationcontrol
rm -r ${CONTROL}/nohup.out
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
docker exec -it -d $code bash -c "cd ../simulationcontrol; export PYTHONIOENCODING='utf-8';nohup python3 run.py"
echo "test2"
#echo `pwd`
#cd ..
#cd simulationcontrol
#python3 run.py
