# lambda-rabbitmq-message-reader

AWS lambda service can be used to read and process RabbitMQ messages. 

## Python Pika Package

This lambda script requires python pika package, which is the [python implementation of RabbbitMQ](https://pypi.org/project/pika/). You can download pika package following [this AWS article](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html).You can also follow the below steps to download the package using Virtual environment.

1) Install virtualenv using pip
```
pip install virtualenv
```

2) Create a virtual environment using the below command
```
virtualenv v-env
```
3) Activate the envronment
```
source v-env/bin/activate
```
4) Install pika in the virtual environment using pip
```
pip install pika
```
5) Deactivate the virtual environment
```
deactivate
```
6) Navigate to the site-packages folder to get the downloaded packages
```
cd v-env/lib/python3.8/site-packages
```

## Mandatory Environment variables
|Variable | Purpose |
|--------------|-------------------|
| RABBIT_HOST | 	RabbitMQ Host |
| RABBIT_USER | RabbitMQ user name to access the service |
| RABBIT_PWD | RabbitMQ password to access the service. If KMS_REGION variable is suppied, this field expects encrypted password |
| RABBIT_QUEUE | RabbitMQ queue name from which messages whould be read. |

## Optional Environment variables
|Variable | Purpose |
|--------------|-------------------|
| KMS_REGION | 	If RABBIT_PWD is a kms encrypted password, this variable is required specify the KMS region to decrypt the password  |
| RABBIT_PORT | if RabbitMQ is using any other port instead of the default port 5672 |

## IAM Policy for Lambda
The place holders [REGION], [ACCOUNT_ID] and [KEY] should be updated with the relavent values. Alternatives the wildcard * can be also used any of them to expand the access.
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "Logs",
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogStream",
                "logs:CreateLogGroup",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        },
        {
            "Sid": "KMS",
            "Effect": "Allow",
            "Action": [
                "kms:Decrypt"
            ],
            "Resource": [
              "arn:aws:kms:[REGION]:[ACCOUNT_ID]:key/[KEY]"
            ]
        }
    ]
}
```
