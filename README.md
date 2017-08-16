# aws-service-catalog-enforce-template-constraints
A Python script to freeze EC2 instance creation to t2.medium/small for Service Catalog portfolios

Go to Lambda Console -> Create-Function->Author From Scratch->Add Trigger->Select SNS -> Choose the correct SNS (the one you created for Budgets Alert) from the list->Check the Enable Trigger on the same page

![alt text](https://github.com/awslabs/aws-service-catalog-enforce-template-constraints/blob/ghoshtapo-patch-1/screenshots/Screen%20Shot%202017-08-16%20at%203.26.20%20PM.png)

![alt text](https://github.com/awslabs/aws-service-catalog-enforce-template-constraints/blob/ghoshtapo-patch-1/screenshots/Screen%20Shot%202017-08-16%20at%203.39.06%20PM.png)

Click Next -> Enter a name for the function-> In the Description, enter "Enforce Template Constraints for ServiceCatalog -> Choose Python2.7 as RunTime-> Paste the contents of enforce-template-constraints.py in the Lambda Function Code block -> Enter lambda_function.lambda_handler in the Handler-> Create a custom role. Name it service-catalog-lambda-<region>role->Enter the following policy 

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

On the Configure function page
![alt text](https://github.com/awslabs/aws-service-catalog-enforce-template-constraints/blob/master/screenshots/Screen%20Shot%202017-08-16%20at%204.03.06%20PM.png)

choose Next-> Review the configuration settings before choosing Create function



