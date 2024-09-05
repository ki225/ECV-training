python3.8 -m venv myenv
source myenv/bin/activate
pip3 install flask
pip3 install pydantic
pip3 install requests
pip3 install gunicorn
pip3 install boto3

sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/AmazonLinux/hashicorp.repo
sudo yum -y install terraform

cd /home/ec2-user ; mkdir customers
gunicorn --config gunicorn_config.py server:server --log-level debug