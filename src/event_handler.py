import boto3
import json
import logging
import os

from base64 import b64decode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# KMS-encrypted ciphertext. Note that the ciphertext has been base64-encoded, in order for the
# ciphertext to be represented as string (KMS CLI does this automatically when specifying output
# as text). It will, therefore, need to be decoded first before decrypting (like done below).
ENCRYPTED_HOOK_URL = os.environ['ENCRYPTED_SLACK_WEBHOOK_URL']
SLACK_CHANNEL = os.environ['SLACK_CHANNEL']

decrypted_hook_url = boto3.client('kms').decrypt(CiphertextBlob=b64decode(ENCRYPTED_HOOK_URL))
HOOK_URL = "https://" + decrypted_hook_url['Plaintext'].decode('utf-8')

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def build_slack_message(message):
    alarm_name = message['AlarmName']
    old_state = message['OldStateValue']
    new_state = message['NewStateValue']
    reason = message['NewStateReason']

    return f"CloudWatch Alarm state changed for `{alarm_name}`" \
        f" from `{old_state}` to `{new_state}`" \
        f" because of the following reason:\n```{reason}```"


def notify_slack(event, context):
    logger.info(f"Event: {str(event)}")
    message = json.loads(event['Records'][0]['Sns']['Message'])
    logger.info(f"Message: {str(message)}")

    slack_data = {'channel': SLACK_CHANNEL, 'text': build_slack_message(message)}

    req = Request(HOOK_URL, json.dumps(slack_data).encode('utf-8'))
    try:
        response = urlopen(req)
        response.read()
        logger.info(f"Message posted to {slack_data['channel']}")
    except HTTPError as e:
        logger.error(f"Request failed: {e.code} {e.reason}")
    except URLError as e:
        logger.error(f"Server connection failed: {e.reason}")
