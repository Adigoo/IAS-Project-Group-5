#!/bin/bash




VM_NAMES=( "servicevm" "appvm" "modelvm" "kafkavm")
# VM_NAMES=( "VM_kafka" )
VM_PUBLIC_IPs=("20.204.11.236" "52.172.255.118" "20.204.176.114" "52.172.252.178")




# put the ips in database

res=$(python3 add_ips_to_db.py "${VM_NAMES[@]}" "${VM_PUBLIC_IPs[@]}");
echo $res

# END put the ips in database