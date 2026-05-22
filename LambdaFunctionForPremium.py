
import json
import boto3
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('SkyFallCustomers')

def lambda_handler(event, context):
    try:
        
        caller_id = event['Details']['ContactData']['CustomerEndpoint']['Address']
        
        clean_phone = int(caller_id.replace('+', ''))

        response = table.scan( 
            FilterExpression=Attr('PhoneNumber').eq(clean_phone)
        )

        items = response.get('Items', [])

        if len(items) > 0:
            customer = items[0]
            account_tier = customer.get('AccountNumber', 'Standard')
            
            if account_tier == "" or account_tier == "<empty>":
                account_tier = "Standard"
            
            return {
                "AccountNumber": account_tier
            }
            
        else:
            return {
                "AccountNumber": "Standard"
            }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "AccountNumber": "Standard"
        }