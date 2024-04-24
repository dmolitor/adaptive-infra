packer {
  required_plugins {
    amazon = {
      version = ">= 1.2.8"
      source  = "github.com/hashicorp/amazon"
    }
  }
}

source "amazon-ebs" "docker" {
  ami_name        = "aws-docker-adaptive"
  ami_description = "An image based on Ubuntu Jammy with Docker installed"
  instance_type   = "t2.micro"
  region          = "us-east-1"
  source_ami_filter {
    filters = {
      name                = "ubuntu/images/*ubuntu-jammy-22.04-amd64-server-*"
      root-device-type    = "ebs"
      virtualization-type = "hvm"
    }
    most_recent = true
    owners      = ["099720109477"]
  }
  ssh_username    = "ubuntu"
}

build {
  sources = [
    "source.amazon-ebs.docker"
  ]
  provisioner "shell" {
    script = "scripts/install-docker.sh"
  }
}