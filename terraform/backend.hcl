# Terraform backend configuration
bucket         = "artist-tracker-terraform-state"
key            = "artist-tracker/terraform.tfstate"
region         = "us-west-2"
encrypt        = true
dynamodb_table = "terraform-state-lock"
