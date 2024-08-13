# VPC
data "aws_vpc" "kg_vpc" {
  filter {
    name   = "tag:Name"
    values = ["kg-vpc"]  
  }
}

data "aws_subnet" "pub_subnet_1a" {
  filter {
    name   = "tag:Name"
    values = ["kg-subnet-public1-us-east-1a"] 
  }
}

data "aws_subnet" "pub_subnet_1b" {
  filter {
    name   = "tag:Name"
    values = ["kg-subnet-public1-us-east-1b"] 
  }
}


data "aws_subnet" "pri_subnet_1a" {
  filter {
    name   = "tag:Name"
    values = ["kg-subnet-private1-us-east-1a"] 
  }
}


data "aws_subnet" "pri_subnet_1b" {
  filter {
    name   = "tag:Name"
    values = ["kg-subnet-private-us-east-1b"] 
  }
}

# data "aws_internet_gateway" "kg_igw" {
#   filter {
#     name   = "attachment.vpc-id"
#     values = [data.aws_vpc.kg-vpc.id]
#   }
# }

# data "aws_nat_gateway" "kg_nat" {
#   filter {
#     name   = "vpc-id"
#     values = [data.aws_vpc.kg-vpc.id]
#   }
# }
