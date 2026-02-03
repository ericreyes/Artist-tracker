# Artist Tracker Architecture

## Infrastructure Overview

### VPC Configuration
- Custom VPC with public/private subnets
- Multi-AZ deployment for high availability
- Internet Gateway for public access

### Terraform Modules
See `/terraform/modules/` for infrastructure code.

### State Management
Terraform state is stored in S3 with DynamoDB locking.
