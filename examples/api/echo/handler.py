'''
Simple echo endpoint for debugging my API Gateway configuration.
'''

import json

def handle(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps({
            'event': event
        }),
        'headers': {
            'Content-Type': 'application/json',
        }
    }
