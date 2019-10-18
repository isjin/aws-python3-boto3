#!/usr/bin/env bash
#reference url https://docs.aws.amazon.com/zh_cn/AWSEC2/latest/UserGuide/mon-scripts.html
# monitor disk memory usage
monitor_path=/monitor
sudo rm -rf $monitor_path
sudo mkdir -p $monitor_path
cd $monitor_path
sudo yum install -y perl-Switch perl-DateTime perl-Sys-Syslog perl-LWP-Protocol-https perl-Digest-SHA.x86_64 unzip
sudo curl https://aws-cloudwatch.s3.amazonaws.com/downloads/CloudWatchMonitoringScripts-1.2.2.zip -O
sudo unzip CloudWatchMonitoringScripts-1.2.2.zip && \sudo rm -rf CloudWatchMonitoringScripts-1.2.2.zip
cd aws-scripts-mon
sudo cp awscreds.template awscreds.conf
cd $monitor_path
echo "*/5 * * * * $monitor_path/aws-scripts-mon/mon-put-instance-data.pl --mem-used-incl-cache-buff --mem-util --disk-space-util --disk-path=/ --from-cron" |sudo tee aws_cloudwatch
sudo crontab aws_cloudwatch