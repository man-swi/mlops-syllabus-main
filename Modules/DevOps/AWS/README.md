# AWS CLI SETUP
### DOWNLOAD AWS CLI 
```
[Install aws cli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
```
### AWS cli setup
```
aws --version #check version
aws configure #And enter the Access Key and Secret Keys 
```
### AWS Calculator
```
[Aws Calculator](https://calculator.aws/#/)
```
# ECR Build &Push Image
### 1. Login To ECR
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <AWS_Account_id>.dkr.ecr.<Region>.amazonaws.com
```
### 2. Build Image
You can skip this step if your image has already been built
```bash
docker build -t dev-devops .
```

### 3. Tag According To ECR 
After the build is completed, tag your image so you can push the image to this repository
```bash
docker tag dev-devops:latest <AWS_Account_id>.dkr.ecr.<Region>.amazonaws.com/dev-devops:latest
```
### 4. Push To ECR
```bash
docker push <AWS_Account_id>.dkr.ecr.<Region>.amazonaws.com/dev-devops:latest
```

# Cloudformation- creating an EC2, iam roles & s3 bucket

```
aws cloudformation create-stack --stack-name MyStackName --template-body file://ec2-s3.yml --region us-east-1
```

