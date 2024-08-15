# variables.tf
# terraform apply -var="region=us-west-2" -var="stage_name=dev" -var="backend_url=https://your-backend-url.com"

variable "region" {
  description = "AWS region"
  default     = "us-east-1"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for the public subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for the private subnets"
  type        = list(string)
  default     = ["10.0.3.0/24", "10.0.4.0/24"]
}

variable "availability_zones" {
  description = "Availability zones"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

variable "ami_id" {
  description = "AMI ID for the EC2 instance"
  default     = "ami-03972092c42e8c0ca"  # Replace with your desired AMI
}

variable "instance_type" {
  description = "Instance type for the EC2 instance"
  default     = "t2.micro"
}

variable "stage_name" {
  description = "The name of the API Gateway stage"
  type        = string
  default     = "dev"
}

variable "flask_port" {
  description = "Port for the Flask server"
  type        = number
  default     = 5000
}

variable "key_pair_name" {
  description = "The name of the key pair to use for the EC2 instance"
  type        = string
}