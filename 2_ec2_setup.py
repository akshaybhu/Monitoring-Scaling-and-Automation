import boto3;

ec2 = boto3.resource('ec2')

#Launch EC2 instance
instance = ec2.create_instances(
    ImageId='ami-01816d07b1128cd2d',
    InstanceType='t2.micro',
    KeyName='akshay_aws_boto3',
    SubnetId='subnet-01874c4512136bd62',
    SecurityGroupIds=['sg-0bc060d9865615fcb'],
    MinCount=1,
    MaxCount=1,
    
    UserData="""#!/bin/bash
                sudo yum update -y
                sudo yum install git -y
                sudo yum install python3 -y
                sudo yum install python3-pip
                sudo yum install -y nginx
                sudo systemctl start nginx
                sudo systemctl enable nginx
                git clone https://github.com/akshaybhu/Monitoring-Scaling-and-Automation.git
                cd Monitoring-Scaling-and-Automation/
                sudo students.html index.html
                sudo cp -f index.html /usr/share/nginx/html/"""
)

#Wait for instance to be in running state
instance[0].wait_until_running()