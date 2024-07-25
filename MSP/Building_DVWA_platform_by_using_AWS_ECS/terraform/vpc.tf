
resource "aws_vpc" "kiki-VPC" {
  cidr_block = "10.0.0.0/16"
  
  tags = {
    Name = "kiki-VPC"
  }
}

resource "aws_internet_gateway" "kiki-igw" {
  vpc_id = aws_vpc.kiki-VPC.id

  tags = {
    Name = "kiki-igw"
  }
}

resource "aws_subnet" "subnet_1" {
  vpc_id            = aws_vpc.kiki-VPC.id
  cidr_block        = "10.0.1.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "Subnet 1"
  }
}

resource "aws_subnet" "subnet_2" {
  vpc_id            = aws_vpc.kiki-VPC.id
  cidr_block        = "10.0.2.0/24"
  availability_zone = "us-east-1b"

  tags = {
    Name = "Subnet 2"
  }
}