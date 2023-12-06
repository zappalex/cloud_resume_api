import json
import boto3
import logging
from CustomEncoder import CustomEncoder

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodbTableName = 'website_visitor_count'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodbTableName)

getMethod = 'GET'
putMethod = 'PUT'
healthPath = '/health'
visitorCountPath = '/visitorCount'


def lambda_handler(event, context):
    logger.info(event)
    httpMethod = event['httpMethod']
    path = event['path']

    if httpMethod == getMethod and path == healthPath:
        response = buildResponse(200)
    elif httpMethod == getMethod and path == visitorCountPath:
        response = getVisitorCount('alexashworthdev')
    elif httpMethod == putMethod and path == visitorCountPath:
        response = updateVisitorCount()

def getVisitorCount(siteName):
    try:
        response = table.get_item(
            Key={
                'site_name': siteName
            }
        )
        if 'Item' in response:
            return buildResponse(200, response['Item'])
        else:
            return buildResponse(404, {'Message': 'site_name: %s not found' % siteName})
    except:
        logger.exception('Custom Error Handling Here!')

def updateVisitorCount():
    pass
def buildResponse(statusCode, body):
    response = {
        'statusCode': statusCode,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    if body is not None:
        response['body'] = json.dumps(body, cls=CustomEncoder)

    return response