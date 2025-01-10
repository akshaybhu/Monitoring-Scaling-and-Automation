import boto3

ec2_client = boto3.client('ec2')

# Create an AMI from the EC2 instance
image = ec2_client.create_image(InstanceId='i-02db0472a739807d7', Name='akshay_aws_boto3')

# Create launch template using the AMI ID
launch_template = ec2_client.create_launch_template(
    LaunchTemplateName='akshay-aws-boto3-template',
    VersionDescription='v1',
    LaunchTemplateData={
        'ImageId': image['ImageId'],
        'InstanceType': 't2.micro',
        'SecurityGroupIds': ['sg-0bc060d9865615fcb'],
        'KeyName': 'aks-boto3'
    }
)

autoscaling = boto3.client('autoscaling')

#Create Auto Scaling Group (ASG)
response = autoscaling.create_auto_scaling_group(
    AutoScalingGroupName='aks-asg-grp',
    LaunchTemplate={'LaunchTemplateName':'akshay-aws-boto3-template','Version':'1'},
    MinSize=2,
    MaxSize=3,
    DesiredCapacity=2,
    VPCZoneIdentifier='subnet-01874c4512136bd62',
    TargetGroupARNs=['arn:aws:elasticloadbalancing:us-east-1:975050024946:loadbalancer/app/aks-aws-alb/7f610a3ca1218e44']
)

# Create scaling policy based on CPU utilization
autoscaling.put_scaling_policy(
    AutoScalingGroupName='aks-asg-grp',
    PolicyName='scale-out-policy',
    ScalingAdjustment=1,
    AdjustmentType='ChangeInCapacity',
    Cooldown=500,
    MetricAggregationType='Average',
    EstimatedInstanceWarmup=500,
    StepAdjustments=[{
        'MetricIntervalLowerBound': 0,
        'ScalingAdjustment': 1
    }]
)    