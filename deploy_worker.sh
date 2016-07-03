#!/bin/bash

export nodes=${nodes:-"root@172.17.0.4 root@172.17.0.5"}

for node in ${nodes}; do
    scp -pr ./ ${node}:/opt/eagle/
    ssh ${node} 'source /opt/eagle/env.sh && 
        nohup python /opt/eagle/worker/worker.py > /opt/eagle/nohup.log 2>&1 &'
done
