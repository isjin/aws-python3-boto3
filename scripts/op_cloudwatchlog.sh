#!/usr/bin/env bash
# install cloudwatch agent for amazon linux

# wxapi的文件名是OpWeiXinApiLog
# smapi的是OpSeminarApiLog
# identity的是OpIdentityApiLog
# docker log data path: /log/data/

awslogpath=/etc/awslogs

sudo yum install -y awslogs
sudo sed -i 's/us-east-1/cn-northwest-1/g' /etc/awslogs/awscli.conf
if [ ! -f /etc/awslogs/awslogs.conf.bak ];then 
sudo mv /etc/awslogs/awslogs.conf /etc/awslogs/awslogs.conf.bak
fi

cd $awslogpath
#wxapi
echo "[/logdata/op/wxapi]" |sudo tee awslogs.conf
echo "datetime_format = %b %d %H:%M:%S" | sudo tee -a sudo tee -a awslogs.conf
echo "file = /logdata/op/wxapi/*.txt" | sudo tee -a awslogs.conf
echo "buffer_duration = 5000" | sudo tee -a awslogs.conf
echo "log_stream_name = OpWeiXinApiLog" | sudo tee -a awslogs.conf
echo "initial_position = start_of_file" | sudo tee -a awslogs.conf
echo "log_group_name = OpWeiXinApi" | sudo tee -a awslogs.conf
echo "" | sudo tee -a awslogs.conf

#smapi
echo "[/logdata/op/smapi]" | sudo tee -a awslogs.conf
echo "datetime_format = %b %d %H:%M:%S" | sudo tee -a awslogs.conf
echo "file = /logdata/op/smapi/*.txt" | sudo tee -a awslogs.conf
echo "buffer_duration = 5000" | sudo tee -a awslogs.conf
echo "log_stream_name = OpSeminarApiLog" | sudo tee -a awslogs.conf
echo "initial_position = start_of_file" | sudo tee -a awslogs.conf
echo "log_group_name = OpSeminarApi" | sudo tee -a awslogs.conf
echo "" | sudo tee -a awslogs.conf

#identity
echo "[/logdata/op/identity]" | sudo tee -a awslogs.conf
echo "datetime_format = %b %d %H:%M:%S" | sudo tee -a awslogs.conf
echo "file = /logdata/op/identity/*.txt" | sudo tee -a awslogs.conf
echo "buffer_duration = 5000" | sudo tee -a awslogs.conf
echo "log_stream_name = OpIdentityApiLog" | sudo tee -a awslogs.conf
echo "initial_position = start_of_file" | sudo tee -a awslogs.conf
echo "log_group_name = OpIdentityApi" | sudo tee -a awslogs.conf
echo "" | sudo tee -a awslogs.conf



