import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
TABLE_NAME = 'rozelle-stream-state'

CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type,X-Api-Key',
    'Access-Control-Allow-Methods': 'GET,PUT,OPTIONS',
    'Content-Type': 'application/json'
}

DEFAULT_STATE = {
    'id': 'current',
    'currentSegment': 'Beat Making Session',
    'currentStatus': 'ON NOW',
    'comingUp': 'Stand-Up Comedy Set',
    'latestProject': 'New EP — Coming Soon',
    'latestProjectMeta': 'Feb 2026'
}

def lambda_handler(event, context):
    method = event.get('httpMethod', 'GET')
    if method == 'OPTIONS':
        return {'statusCode': 200, 'headers': CORS_HEADERS, 'body': ''}
    table = dynamodb.Table(TABLE_NAME)
    if method == 'GET':
        try:
            response = table.get_item(Key={'id': 'current'})
            item = response.get('Item', DEFAULT_STATE)
            item.pop('id', None)
            return {'statusCode': 200, 'headers': CORS_HEADERS, 'body': json.dumps(item)}
        except Exception as e:
            return {'statusCode': 500, 'headers': CORS_HEADERS, 'body': json.dumps({'error': str(e)})}
    if method == 'PUT':
        try:
            body = json.loads(event.get('body', '{}'))
            allowed = ['currentSegment', 'currentStatus', 'comingUp', 'latestProject', 'latestProjectMeta']
            update_expr_parts = []
            expr_values = {}
            expr_names = {}
            for field in allowed:
                if field in body:
                    safe_key = f'#f_{field}'
                    val_key  = f':v_{field}'
                    expr_names[safe_key] = field
                    expr_values[val_key]  = body[field]
                    update_expr_parts.append(f'{safe_key} = {val_key}')
            if not update_expr_parts:
                return {'statusCode': 400, 'headers': CORS_HEADERS, 'body': json.dumps({'error': 'No valid fields provided'})}
            table.update_item(
                Key={'id': 'current'},
                UpdateExpression='SET ' + ', '.join(update_expr_parts),
                ExpressionAttributeNames=expr_names,
                ExpressionAttributeValues=expr_values
            )
            return {'statusCode': 200, 'headers': CORS_HEADERS, 'body': json.dumps({'success': True, 'updated': list(body.keys())})}
        except json.JSONDecodeError:
            return {'statusCode': 400, 'headers': CORS_HEADERS, 'body': json.dumps({'error': 'Invalid JSON body'})}
        except Exception as e:
            return {'statusCode': 500, 'headers': CORS_HEADERS, 'body': json.dumps({'error': str(e)})}
    return {'statusCode': 405, 'headers': CORS_HEADERS, 'body': json.dumps({'error': 'Method not allowed'})}
