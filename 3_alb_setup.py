import boto3

alb = boto3.client('elbv2')

# Create a load balancer
response = alb.create_load_balancer(
    Name='aks-aws-alb',
    Subnets=['subnet-01874c4512136bd62','subnet-08fa616f96d54dfc2'],  
    SecurityGroups=['sg-0bc060d9865615fcb'],
    Scheme='internet-facing',
    Type='application'
)

alb_arn = response['LoadBalancers'][0]['LoadBalancerArn']

# Create a target group for the EC2 instance
target_group = alb.create_target_group(
    Name='akshay-tg-alb',
    Protocol='HTTP',
    Port=80,
    VpcId='vpc-09f02049d6176fe30'
)

# Register EC2 instance in the target group
instance_id = 'i-02db0472a739807d7'
alb.register_targets(
    TargetGroupArn=target_group['TargetGroups'][0]['TargetGroupArn'],
    Targets=[{'Id': instance_id}]
)

# Create a listener for the ALB to forward traffic to the target group
alb.create_listener(
    LoadBalancerArn=alb_arn,
    Protocol='HTTP',
    Port=80,
    DefaultActions=[{
        'Type': 'forward',
        'TargetGroupArn': target_group['TargetGroups'][0]['TargetGroupArn']
    }]
)