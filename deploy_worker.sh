#!/bin/bash

export nodes=${nodes:-"root@172.17.0.4 root@172.17.0.5"}

for node in ${nodes}; do
    host=$(echo ${node} | awk -F'@' '{print $2}')
    sed -i "s/DEPLOY_HOSTNAME = '.*'/DEPLOY_HOSTNAME = '${host}'/g" worker/worker_cfg.py
    scp -pr ./ ${node}:/opt/eagle/
    ssh ${node} 'source /opt/eagle/env.sh && 
        nohup python /opt/eagle/worker/worker.py > /opt/eagle/nohup.log 2>&1 &'
done
