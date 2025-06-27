resource "aws_instance" "fastapi_ec2" {
  ami                         = "ami-0c803b171269e2d72" # Amazon Linux 2 2023
  instance_type               = var.instance_type
  key_name                    = var.key_name
  iam_instance_profile        = "aws_ec2_role"
  associate_public_ip_address = true

  vpc_security_group_ids = [aws_security_group.allow_web.id]

  user_data = <<-EOF
              #!/bin/bash
              set -e

              dnf update -y
              dnf install -y docker

              systemctl enable docker
              systemctl start docker

              usermod -aG docker ec2-user
              aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin ${var.ecr_image_url}
              docker pull ${var.ecr_image_url}
              docker run -d -p 80:8000 ${var.ecr_image_url}
              EOF



  tags = {
    Name = "FastAPI-Server-text-to-img"
  }
}
