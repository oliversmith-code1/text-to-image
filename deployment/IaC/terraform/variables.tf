variable "aws_region" {
  default = "us-east-2"
}

variable "instance_type" {
  default = "t2.micro"
}

variable "ecr_image_url" {
  description = "The full ECR image URL"
  default     = "381781745738.dkr.ecr.us-east-2.amazonaws.com/text-to-img"
  type        = string
}

variable "key_name" {
  description = "Name of the EC2 key pair"
  default     = "textToImg"
  type        = string
}