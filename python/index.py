import json
import logging
import os
import botocore.vendored.requests as requests
import urllib.request

HOOK_URL = os.environ['WebhookUrl']


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def format_message(data):
    payload = {
        'username': f"WAF {data['Type']}",
        'icon_emoji': ':managedrule:',
        'text': f"{data['Subject']}",
        'attachments': [
            {
                'fallback': "Detailed information on {data['Type']}.",
                'color': 'green',
                'title': data['Subject'],
                'text': data['Message'],
                'fields': [
                    {
                        'title': 'Managed Rule Group',
                        'value': data['MessageAttributes']['managed_rule_group']['Value'],
                        'short': True
                    },
                    {
                        'title': 'Version',
                        'value': data['MessageAttributes']['major_version']['Value'],
                        'short': True
                    }
                ]
            }
        ]
    }
    return payload


def notify_slack(url, payload):
    data = json.dumps(payload).encode('utf-8')
    method = 'POST'
    headers = {'Content-Type': 'application/json'}

    request = urllib.request.Request(url, data = data, method = method, headers = headers)
    with urllib.request.urlopen(request) as response:
        return response.read().decode('utf-8')

def lambda_handler(event, context):
    logger.info("Message: " + str(event))
    payload = format_message(event['Records'][0]['Sns'])
    response = notify_slack(HOOK_URL, payload)
    return response