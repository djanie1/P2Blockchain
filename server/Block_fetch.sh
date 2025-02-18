#!/bin/bash
#loop through till all blocks are retrieved
x=579
while [ $x -lt 584 ]
do
    docker exec -it peer3 peer channel fetch "$x" "/var/hyperledger/fabric/config/blocks_folder/block$x.block" -c dipperchannel --orderer 192.168.1.10:7050 --tls=true --cafile /var/hyperledger/fabric/config/root-tls/tls-ca-cert.pem
    ((x++))
done
#docker exec -it peer3 peer channel fetch newest /var/hyperledger/fabric/config/blocks_folder/block.block -c dipperchannel --orderer 192.168.1.10:7050 --tls=true --cafile /var/hyperledger/fabric/config/root-tls/tls-ca-cert.pem
#docker exec -it peer3 peer channel fetch <block_number> -c dipperchannel --orderer 192.168.1.10:7050 --tls=true --cafile /var/hyperledger/fabric/config/root-tls/tls-ca-cert.pem
