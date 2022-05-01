#!/bin/bash

az login

SUB_ID=$(az account show --query 'id' -o json)

printf "\n\n"
echo "###### Provisioning VMs ########"
printf "\n\n"

printf "\n"
echo "Enter the resource group name"
read RESOURCE_GROUP_NAME

az group create --name $RESOURCE_GROUP_NAME --location centralindia

VM_NAMES=( "vm1" "vm2" )
# VM_NAMES=( "VM_kafka" )
VM_PUBLIC_IPs=()

printf "\n\n"
echo "## Provisioning ${#VM_NAMES[@]} VMs ##"
printf "\n"

for vm_name in "${VM_NAMES[@]}"
do
PUBLIC_IP_ADDRESS=$(az vm create --resource-group $RESOURCE_GROUP_NAME \
  --name $vm_name \
  --image UbuntuLTS \
  --output json \
  --verbose \
  --authentication-type all\
  --generate-ssh-keys\
  --admin-username ias_user\
  --admin-password Abc@12345xyz\
  --query 'publicIpAddress' -o json)

VM_PUBLIC_IPs+=($PUBLIC_IP_ADDRESS)
az vm open-port --port 22 --resource-group $RESOURCE_GROUP_NAME --name $vm_name --priority 400
az vm open-port --port 80 --resource-group $RESOURCE_GROUP_NAME --name $vm_name --priority 600
az vm open-port --port 5000 --resource-group $RESOURCE_GROUP_NAME --name $vm_name --priority 700
az vm open-port --port 5001 --resource-group $RESOURCE_GROUP_NAME --name $vm_name --priority 701
az vm open-port --port 5002 --resource-group $RESOURCE_GROUP_NAME --name $vm_name --priority 702
az vm open-port --port 5003 --resource-group $RESOURCE_GROUP_NAME --name $vm_name --priority 703
az vm open-port --port 5004 --resource-group $RESOURCE_GROUP_NAME --name $vm_name --priority 704
az vm open-port --port 5005 --resource-group $RESOURCE_GROUP_NAME --name $vm_name --priority 705
az vm open-port --port 5006 --resource-group $RESOURCE_GROUP_NAME --name $vm_name --priority 706
az vm open-port --port 5007 --resource-group $RESOURCE_GROUP_NAME --name $vm_name --priority 707
az vm open-port --port 5008--resource-group $RESOURCE_GROUP_NAME --name $vm_name --priority 708
az vm open-port --port 5009 --resource-group $RESOURCE_GROUP_NAME --name $vm_name --priority 709
az vm open-port --port 5010 --resource-group $RESOURCE_GROUP_NAME --name $vm_name --priority 710
az vm open-port --port 2376 --resource-group $RESOURCE_GROUP_NAME --name $vm_name --priority 711
az vm open-port --port 9092 --resource-group $RESOURCE_GROUP_NAME --name $vm_name --priority 800
az vm open-port --port 8004 --resource-group $RESOURCE_GROUP_NAME --name $vm_name --priority 1200
az vm open-port --port 10000 --resource-group $RESOURCE_GROUP_NAME --name $vm_name --priority 1100
az vm open-port --port 50000 --resource-group $RESOURCE_GROUP_NAME --name $vm_name --priority 1300
done

printf "\n\n"
echo "VMs have been provisioned at following IP addresses"
OUTPUT_FILENAME=vms_history.txt
VM_ADMIN_USERNAME=$(az vm show --resource-group $RESOURCE_GROUP_NAME --name ${VM_NAMES[0]} --query 'osProfile.adminUsername' -o json)
VM_ADMIN_USERNAME=$(echo "$VM_ADMIN_USERNAME" | tr '"' "'")

for ip in "${VM_PUBLIC_IPs[@]}"
do
  echo "Installing dependencies"
  IP_NEW="${ip%\"}"
  IP_NEW="${IP_NEW#\"}"
  UN_NEW="${VM_ADMIN_USERNAME%\'}"
  UN_NEW="${UN_NEW#\'}"
  echo $IP_NEW
  echo $UN_NEW
  sshpass -f pass ssh -o StrictHostKeyChecking=no $UN_NEW@$IP_NEW "sudo apt install curl; curl -fsSL https://get.docker.com -o get-docker.sh; sudo sh get-docker.sh; sudo apt-get install sshpass; sudo apt install -y python3-pip;sudo -H pip3 install --upgrade pip; pip3 install kafka-python;pip3 install azure-storage-file-share;pip3 install Flask;"
  sudo chmod 777 /var/run/docker.sock
  # sshpass -f pass scp -o StrictHostKeyChecking=no -r node $UN_NEW@$IP_NEW:node
  # sshpass -f pass ssh -o StrictHostKeyChecking=no $UN_NEW@$IP_NEW "cd node && python3 node2.py" &
done

INDEX=0
for ip in "${VM_PUBLIC_IPs[@]}"
do
  echo "* $ip"
  ip=$(echo "$ip" | tr '"' "'")
  echo "$ip '${VM_NAMES[$INDEX]}' $VM_ADMIN_USERNAME" >> $OUTPUT_FILENAME
 INDEX=$((INDEX+1))
done
