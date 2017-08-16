# aws-service-catalog-enforce-template-constraints
A Python script to freeze EC2 instance creation to t2.medium/small for Service Catalog portfolios

Go to Lambda Console -> Create-Function->Author From Scratch->Add Trigger->Select Lambda -> Choose the correct lambda from listing->Check the Enable Trigger on the same page->Click Next -> Enter a name for the function-> Enter "Enforce Template Constraints for ServiceCatalog in the Description -> Choose Python2.7 as RunTime-> Paste the contents of enforce-template-constraints.py in the Lambda Function Code block -> Enter lambda_function.lambda_handler in the Handler-> Create a custom role. Name it service-catalog-lambda-role->Enter the following policy 

```

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "servicecatalog:*",
                "s3:*",
                "cloudformation:ValidateTemplate",
                "iam:GetRole"
            ],
            "Resource": [
                "*"
            ],
            "Effect": "Allow"
        },
        {
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*",
            "Effect": "Allow"
        }
    ]
}

```

On the Configure function page, choose Next-> Review the configuration settings before choosing Create function



