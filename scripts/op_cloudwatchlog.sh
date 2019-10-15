#!/usr/bin/env bash
# install cloudwatch agent for amazon linux

# wxapi的文件名是OpWeiXinApiLog
# smapi的是OpSeminarApiLog
# identity的是OpIdentityApiLog

sudo yum install -y awslogs
sudo sed -i 's/us-east-1/cn-northwest-1/g' /etc/awslogs/awscli.conf
sudo mv /etc/awslogs/awslogs.conf /etc/awslogs/awslogs.conf.bak

#wxapi
echo -e "[/logdata/op/wxapi]" >> awslogs.conf
echo -e "datetime_format = %b %d %H:%M:%S" >> awslogs.conf
echo -e "file = /logdata/op/wxapi/*.txt" >> awslogs.conf
echo -e "buffer_duration = 5000" >> awslogs.conf
echo -e "log_stream_name = OpWeiXinApiLog" >> awslogs.conf
echo -e "initial_position = start_of_file" >> awslogs.conf
echo -e "log_group_name = OpWeiXinApi" >> awslogs.conf

#smapi
echo -e "[/logdata/op/smapi]" >> awslogs.conf
echo -e "datetime_format = %b %d %H:%M:%S" >> awslogs.conf
echo -e "file = /logdata/op/smapi/*.txt" >> awslogs.conf
echo -e "buffer_duration = 5000" >> awslogs.conf
echo -e "log_stream_name = OpSeminarApiLog" >> awslogs.conf
echo -e "initial_position = start_of_file" >> awslogs.conf
echo -e "log_group_name = OpSeminarApi" >> awslogs.conf

#identity
echo -e "[/logdata/op/identity]" >> awslogs.conf
echo -e "datetime_format = %b %d %H:%M:%S" >> awslogs.conf
echo -e "file = /logdata/op/identity/*.txt" >> awslogs.conf
echo -e "buffer_duration = 5000" >> awslogs.conf
echo -e "log_stream_name = OpIdentityApiLog" >> awslogs.conf
echo -e "initial_position = start_of_file" >> awslogs.conf
echo -e "log_group_name = OpIdentityApi" >> awslogs.conf

