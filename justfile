set dotenv-load := true

instance_type := env_var('AWS_INSTANCE_TYPE')
postgres_volume := env_var('POSTGRES_VOLUME')
swarm_n := env_var('AWS_SWARM_N')

# List all available recipes
default:
  just --list
  @echo "To execute a recipe: just [recipe-name]"

# Build AWS EC2 AMI with HCL Packer
aws-ami-build: aws-sso-login
  packer init {{justfile_directory()}}
  packer validate {{justfile_directory()}}
  -packer build {{justfile_directory()}}/aws-docker.pkr.hcl

# Provision an AWS security group
aws-security-group: aws-sso-login venv
  source {{justfile_directory()}}/.venv/bin/activate
  python {{justfile_directory()}}/scripts/create-security-group.py

# Launch a Docker Swarm on an AWS EC2 server
aws-swarm-launch: aws-ami-build aws-security-group aws-volume
  source {{justfile_directory()}}/.venv/bin/activate
  python {{justfile_directory()}}/scripts/deploy-swarm.py {{instance_type}} {{postgres_volume}} {{swarm_n}}

# Configure AWS SSO
aws-sso-configure:
  aws configure sso

# AWS SSO login
aws-sso-login profile="default":
  #!/usr/bin/env zsh
  SSO_ACCOUNT=$(aws sts get-caller-identity --query "Account" --profile {{profile}})
  #you can add a better check, but this is just an idea for quick check
  if [ ! ${#SSO_ACCOUNT} -eq 14 ];  then 
    aws sso login ;
  fi

# Provision an AWS EBS volume
aws-volume: aws-sso-login venv
  source {{justfile_directory()}}/.venv/bin/activate
  python {{justfile_directory()}}/scripts/create-volume.py

# Build and push the app and api Docker images
docker-build:
  docker login
  docker compose build -q
  docker compose push -q

# Activate virtual environment and install Python dependencies
venv:
  #!/usr/bin/env zsh
  if [ ! -d {{justfile_directory()}}/.venv ]; then
    echo "Creating {{justfile_directory()}}/.venv"
    python3 -m venv {{justfile_directory()}}/.venv
  fi
  source {{justfile_directory()}}/.venv/bin/activate
  pip install -q --upgrade pip
  pip install -q -r {{justfile_directory()}}/requirements.txt
