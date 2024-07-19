# Create a Private Subnet
resource "aws_subnet" "private1" {
    vpc_id = aws_vpc.main.id
    cidr_block = "10.0.1.0/24"
    availability_zone = "ap-northeast-1a"

    tags = {
        Name = "private-subnet1"
    }
}

resource "aws_subnet" "private2" {
    vpc_id = aws_vpc.main.id
    cidr_block = "10.0.2.0/24"
    availability_zone = "ap-northeast-1c"

    tags = {
        Name = "private-subnet2"
    }
}
