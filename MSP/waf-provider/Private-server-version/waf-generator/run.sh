sudo yum update -y

python3.8 -m venv myenv
source myenv/bin/activate
pip3 install pydantic
pip3 install requests
pip3 install boto3
pip3 install botocore
pip3 install uvicorn
pip3 install asgiref
pip3 install hypercorn
pip3 install aioboto3
pip3 install quart

sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/AmazonLinux/hashicorp.repo
sudo yum -y install terraform

cd /home/ec2-user ; mkdir customers
sudo lsof -ti:5000 | xargs kill -9
hypercorn server:server --workers 4 --worker-class asyncio --backlog 100 --bind 0.0.0.0:5000 --keep-alive 300 
hypercorn server:server --worker-class asyncio --backlog 100 --bind 0.0.0.0:5000 --keep-alive 300 
