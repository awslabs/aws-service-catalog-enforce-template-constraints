#Copyright 2017 Amazon.com, Inc. and its affiliates. All Rights Reserved.
#SPDX-License-Identifier: MIT-0

# This sample, non-production-ready script can clamp down the instancetype constraint for all Service Catalog portfolio/product to t2.medium or small. and the associated products (c) 2017 Amazon Web Services, Inc. or its affiliates. All Rights Reserved. This AWS Content is provided subject to the terms of the AWS Customer Agreement available at http://aws.amazon.com/agreement or other written agreement between Customer and Amazon Web Services, Inc.

from __future__ import print_function
import json
import boto3
import traceback
from boto3.session import Session
import zipfile
import botocore
import uuid


client = boto3.client('servicecatalog')

""" Main method controlling the sequence of actions as follows
        1. List all portfolios
        2. List products associated with each portfolip
        3. For each portfolio list constraint and filter by TEMPLATE and then by InstanceType constraint
        4. Delete all the constraints matching above condition
        5. Recreate constraints for each one deleted with new small InstanceType only
    :param event: Input json from SNS
    :param context: Not used, but required for Lambda function
    :return: None
    :exception: Any exception
"""

def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    message = event['Records'][0]['Sns']['Message']
    print("From SNS: " + message)
    constraint_metadata=[]
    constraintIDs=[]
    portIds=list_portfolios()
    rule="""{
     "Rules": {
     "Rule1": {
       "Assertions": [
         {
           "Assert": {
             "Fn::Contains": [
               [
                 "t1.micro",
                 "t2.medium"
               ],
               {
                 "Ref": "InstanceType"
               }
             ]
           },
           "AssertDescription": "Instance type should be either t1.micro or t2.medium"
         }
       ]
     }
   }
  }"""
    try:
       for index in range(len(portIds)):
        print (portIds[index])
        prodIds=list_products_for_portfolio(portIds[index])
        for index2 in range(len(prodIds)):
            #Iterate over all products to check constraints
            print ("Listing constraints.........")
            constraintIDs=list_constraint_for_portfolio(portIds[index])
            for constraintID in constraintIDs:
                print ("deleting existing constraint with InstanceTypes....\n")
                if delete_constraint(constraintID) is True:
                   print ("Creating constraint with small instance type....\n")
                   result=create_constraint(portIds[index],str(prodIds[index2]['ProductId']),rule)
    except Exception as e:
        print('Function failed due to exception.')
        print(e)


def list_constraint_for_portfolio(id):
    constraintIDs=[]
    response = client.list_constraints_for_portfolio(
    AcceptLanguage='en',
    PortfolioId=id
)
    #Product can have multiple TEMPLATE constraints, so returning a list
    for index in range(len(response['ConstraintDetails'])):
        if response['ConstraintDetails'][index]['Type'] == 'TEMPLATE':
           if "InstanceType" in str(describe_constraint(response['ConstraintDetails'][index]['ConstraintId'])):
              constraintIDs.append(response['ConstraintDetails'][index]['ConstraintId'])
    return constraintIDs

def list_portfolios():
    """
    :return:  List of Portfolios in the account
    """
    nextmarker = None
    done = False
    lst_portfolio = []
    portIds=[]

    while not done:
        if nextmarker:
                portfolio_response = client.list_portfolios(PageToken=nextmarker,PageSize=20)
        else:
            portfolio_response = client.list_portfolios()

        for portfolio in portfolio_response['PortfolioDetails']:
            lst_portfolio.append(portfolio)

        if 'NextPageToken' in portfolio_response:
            nextmarker = portfolio_response['NextPageToken']
        else:
            break
    for i in range(len(lst_portfolio)):
        portId = lst_portfolio[i]['Id']
        portIds.append(portId)
    return portIds


def list_products_for_portfolio(id):
    """
    :param id: portfolio id
    :return: List of products associated with the portfolio
    """
    nextmarker = None
    done = False
    lst_products = []

    while not done:
        if nextmarker:
            product_response = client.search_products_as_admin(nextmarker=nextmarker, PortfolioId=id)
        else:
            product_response = client.search_products_as_admin(PortfolioId=id)

        for product in product_response['ProductViewDetails']:
            lst_products.append(product['ProductViewSummary'])

        if 'NextPageToken' in product_response:
            nextmarker = product_response['NextPageToken']
        else:
            break
    return lst_products

def delete_constraint(constraintId):
    response = client.delete_constraint(
    AcceptLanguage='en',
    Id=constraintId
)
    if (str(response['ResponseMetadata']['HTTPStatusCode']) == '200'):
       print ("Deleted")
       return True
    else:
       return False

def describe_constraint(constraintId):
    response = client.describe_constraint(
    AcceptLanguage='en',
    Id=constraintId
)
    obj=eval(str(response))

    return obj

def create_constraint(portId,prodId,rule):
    response = client.create_constraint(
    AcceptLanguage='en',
    PortfolioId=portId,
    ProductId=prodId,
    Parameters=rule,
    Type='TEMPLATE',
    Description='t2 medium or small only',
    IdempotencyToken=str(uuid.uuid4()))
    if response['Status'] != 'CREATING':
       return False
    else:
       return True
