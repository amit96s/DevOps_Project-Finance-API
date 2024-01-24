provider "aws" {}
resource "aws_instance" "web3" {
  ami           = "ami-0005e0cfe09cc9050"
  instance_type = "t3.small"
  user_data = <<-EOF
             #!/bin/bash
              exec > /var/log/user-data.log 2>&1
              set -e
              sudo yum update -y
              sudo yum install docker -y
              sudo service docker start
              sudo docker run -d -p 80:5000 amit1shemesh/finaanceapiv1:latest
              sudo docker run -d --network="host" amit1shemesh/finance_api_daily_tests:latest
              sudo wget -O /etc/yum.repos.d/jenkins.repo \
                  https://pkg.jenkins.io/redhat-stable/jenkins.repo
              sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key
              sudo yum upgrade
              sudo yum install java-17-amazon-corretto -y
              sudo yum install jenkins -y
              sudo usermod -aG docker jenkins
              sudo systemctl start jenkins

            EOF
}

resource "aws_security_group" "api-port" {
  name = "amit-api-group"
  description = "allow access to ssh and port 80"

  ingress {
    from_port = 22
    protocol = "tcp"
    to_port = 22
    cidr_blocks = [
      "0.0.0.0/0"]
  }

  ingress {
    from_port = 80
    protocol = "tcp"
    to_port = 5000
    cidr_blocks = [
      "0.0.0.0/0"]
  }

  ingress {
    from_port = 0
    protocol = "-1"
    to_port = 0
    cidr_blocks = [
      "0.0.0.0/0"]
  }

  ingress {
    from_port = 8080
    protocol = "tcp"
    to_port = 8080
    cidr_blocks = [
      "0.0.0.0/0"]
  }
}