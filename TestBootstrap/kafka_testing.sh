
az login

SUB_ID=$(az account show --query 'id' -o json)

printf "\n\n"
echo "###### Provisioning VMs ########"
printf "\n\n"

printf "\n"
echo "Enter the resource group name"
read RESOURCE_GROUP_NAME

az group create --name $RESOURCE_GROUP_NAME --location centralindia

VM_NAMES=( "servicevm" "appvm" "modelvm" "kafkavm")
# VM_NAMES=( "VM_kafka" )
VM_PUBLIC_IPs=()

# "20.219.13.244" "20.207.197.64" "20.219.31.64" "20.207.198.176"

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
  --admin-password Ias@12345678\
  --query 'publicIpAddress' -o json)
VM_PUBLIC_IPs+=($PUBLIC_IP_ADDRESS)
az vm open-port --port 22 --resource-group $RESOURCE_GROUP_NAME --name $vm_name --priority 400
az vm open-port --port 80 --resource-group $RESOURCE_GROUP_NAME --name $vm_name --priority 600
az vm open-port --port 5000 --resource-group $RESOURCE_GROUP_NAME --name $vm_name --priority 700
az vm open-port --port 5001 --resource-group $RESOURCE_GROUP_NAME --name $vm_name --priority 701
az vm open-port --port 5002 --resource-group $RESOURCE_GROUP_NAME --name $vm_name --priority 702
az vm open-port --port 5003 --resource-group $RESOURCE_GROUP_NAME --name $vm_name --priority 703
az vm open-port --port 5004 --resource-group $RESOURCE_GROUP_NAME --name $vm_na0me --priority 704
az vm open-port --port 5005 --resource-group $RESOURCE_GROUP_NAME --name $vm_name --priority 705
az vm open-port --port 5006 --resource-group $RESOURCE_GROUP_NAME --name $vm_name --priority 706
az vm open-port --port 5007 --resource-group $RESOURCE_GROUP_NAME --name $vm_name --priority 707
az vm open-port --port 5008 --resource-group $RESOURCE_GROUP_NAME --name $vm_name --priority 708
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


counter=0
for ip in "${VM_PUBLIC_IPs[@]}"
do
  IP_NEW="${ip%\"}"
  IP_NEW="${IP_NEW#\"}"
  UN_NEW="${VM_ADMIN_USERNAME%\'}"
  UN_NEW="${UN_NEW#\'}"
  echo $IP_NEW
  echo $UN_NEW
  sshpass -f pass ssh -o StrictHostKeyChecking=no $UN_NEW@$IP_NEW "sudo apt install curl; curl -fsSL https://get.docker.com -o get-docker.sh; sudo sh get-docker.sh; sudo apt-get install sshpass; sudo apt install -y python3-pip;sudo -H pip3 install --upgrade pip; pip3 install kafka-python;pip3 install azure-storage-file-share;pip install Flask; sudo chmod 777 /var/run/docker.sock; git clone https://github.com/Adigoo/IAS-Project-Group-5.git;"
  # sshpass -f pass scp -o StrictHostKeyChecking=no -r node $UN_NEW@$IP_NEW:node
  # sshpass -f pass ssh -o StrictHostKeyChecking=no $UN_NEW@$IP_NEW "cd node && python3 node2.py" &

  if [[ $counter == 3 ]]; then
    echo "inside"
    sshpass -f pass ssh -o StrictHostKeyChecking=no $UN_NEW@$IP_NEW "\
        sudo apt install -y default-jre; \
        wget https://dlcdn.apache.org/kafka/3.1.0/kafka_2.13-3.1.0.tgz; \
        
        tar -xzvf kafka_2.13-3.1.0.tgz; \
        rm -rf kafka_2.13-3.1.0.tgz*;\
        rm -rf IAS-Project-Group-5;\
        git clone https://github.com/Adigoo/IAS-Project-Group-5.git;\
        cp IAS-Project-Group-5/TestBootstrap/update_advertized_listener_kafka.py .;\
        python3 ./update_advertized_listener_kafka.py $IP_ADDR; \
        cd kafka_2.13-3.1.0; \
        bin/zookeeper-server-start.sh -daemon config/zookeeper.properties; \
        sleep 10s; \
        JMX_PORT=8004 bin/kafka-server-start.sh -daemon config/server.properties; \
        sleep 10s;
    "

  fi

  counter=$(($counter + 1));
done




INDEX=0
for ip in "${VM_PUBLIC_IPs[@]}"
do
  echo "* $ip"
  ip=$(echo "$ip" | tr '"' "'")
  echo "$ip '${VM_NAMES[$INDEX]}' $VM_ADMIN_USERNAME" >> $OUTPUT_FILENAME
 INDEX=$((INDEX+1))
done


# put the ips in database
echo "Will this execute?"
res=$(python3 add_ips_to_db.py "${VM_NAMES[@]}" "${VM_PUBLIC_IPs[@]}");
echo $res

# END put the ips in database