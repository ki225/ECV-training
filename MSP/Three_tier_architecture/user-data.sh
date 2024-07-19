#!/bin/bash
sudo yum update -y
sudo yum install -y httpd
sudo yum install -y httpd php
sudo systemctl start httpd
sudo systemctl enable httpd
sudo yum install -y mysql
sudo yum install amazon-cloudwatch-agent -y
sudo yum install aws-cli -y


HOST_IP1=$(ip addr show enX0 | grep 'inet ' | awk '{print $2}' | cut -d'/' -f1)
HOST_IP2=$(ip addr show eth0 | grep 'inet ' | awk '{print $2}' | cut -d'/' -f1)
echo -e "$HOST_IP1\n$HOST_IP2" > /var/www/html/index.html

sudo ln -s /etc/httpd/logs/access_log /var/log/access_log

cat << 'EOF' > /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json
{
  "agent": {
    "run_as_user": "root"
  },
  "metrics": {
    "metrics_collected": {
      "mem": {
        "measurement": [
          "mem_used_percent"
        ],
        "metrics_collection_interval": 60
      }
    }
  },
  "logs": {
    "logs_collected": {
      "files": {
        "collect_list": [
          {
            "file_path": "/var/log/access_log",
            "log_group_name": "kiki-log-group",
            "log_stream_name": "{instance_id}"
          }
        ]
      }
    }
  }
}
EOF

sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -s -c file:/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json