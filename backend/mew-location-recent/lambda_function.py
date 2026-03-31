import json
import boto3
from boto3.dynamodb.conditions import Attr
from botocore.config import Config
import requests
from datetime import datetime
from zoneinfo import ZoneInfo

from backend.shared.config import load_config
from backend.shared.http import cors_headers, error_response, get_header

cfg = load_config()
config = Config(region_name=cfg.aws_region)
config.endpoint_discovery_enabled = True
timestream_query_client = boto3.client('timestream-query', config=config)


def lambda_handler(event, context):
    
    cfg_local = load_config()
    origin = get_header(event, "origin")

    try:
        access_token = event["access_token"]
    except Exception:
        return error_response(
            status_code=400,
            message="Bad Request: access_token is required",
            origin=origin,
            allowed_origins=cfg_local.allowed_origins,
        )
    valid_result = validate_access_token(access_token)
    if valid_result == True:
        user_id = get_user_id(access_token)
        
        dynamoDB = boto3.resource('dynamodb')
        table = dynamoDB.Table('mew-line-device')
        scan_res = table_scan(table,user_id)

        if not scan_res["Items"]:
            msg_notlink = "アカウント連携が完了していません。アカウント連携を実施して再実行して下さい。"
            send_message(user_id,msg_notlink)
            
        else:
            device_id = scan_res["Items"][0].get("DeviceID")

        try:
            msg_succes = "ログインが成功しました"
            loc_res = scan_reccent_location(device_id)
            send_message(user_id,msg_succes)
        except Exception:
            msg_notgnss = "位置情報がありません。解決しない場合は問い合わせフォームよりお問合せ下さい。"
            send_message(user_id,msg_notgnss)
            return error_response(
                status_code=404,
                message="Location not found",
                origin=origin,
                allowed_origins=cfg_local.allowed_origins,
            )
    else:
        return error_response(
            status_code=401,
            message="Access token validation failed",
            origin=origin,
            allowed_origins=cfg_local.allowed_origins,
        )
        
    return {
        "statusCode": 200,
        "headers": cors_headers(origin, cfg_local.allowed_origins),
        "body": json.dumps(loc_res, ensure_ascii=False),
    }
    

def validate_access_token(access_token):
    
    params = {
        'access_token': access_token
    }
    
    response_vali = requests.get('https://api.line.me/oauth2/v2.1/verify', params=params)
    res_client_id = response_vali.json()["client_id"]
    
    valid_result = False 
    
    cfg_local = load_config()
    if res_client_id == cfg_local.line_channel_id:
        valid_result = True
    else:
        valid_result = False
    

    return valid_result

def get_user_id(access_token):
    
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    
    response_userid = requests.get('https://api.line.me/v2/profile', headers=headers)
    
    return response_userid.json()["userId"]


def table_scan(dynamo_table,serch_user_id):
    
     options = {
        'FilterExpression': Attr('LINEID').eq(serch_user_id)
     }
     res = dynamo_table.scan(**options)
     return res



def scan_reccent_location(device_id):
    
    QUERY = """SELECT * FROM "mew_db"."mew_gnss_tables" \
            WHERE device = '%s' \
            ORDER BY time DESC LIMIT 3"""%device_id

    result = timestream_query_client.query(
        QueryString=QUERY
    )
    
    device_id = result['Rows'][0]["Data"][0]["ScalarValue"]
    

    data = {}
    for i in range(len(result['Rows'])):
        data['No%s' %(i+1)] = {}
        data['No%s' %(i+1)]['time_stamp'] = trans_timezone(result['Rows'][i]["Data"][2]["ScalarValue"])
        data['No%s' %(i+1)]['gnss'] = trans_gnss(result['Rows'][i]["Data"][4]["ScalarValue"])


    return {
        'device_id': device_id,
        'Data': [
            data
        ]
    }


def trans_timezone(time_stamp):
    
    time_jst = datetime.strptime(time_stamp[:-10], '%Y-%m-%d %H:%M:%S')
    time_jst = time_jst.astimezone(ZoneInfo("UTC"))
    time_jst = time_jst.astimezone(ZoneInfo("Asia/Tokyo"))
    time_jst = time_jst.strftime('%Y/%m/%d %H:%M')
    
    return time_jst


def trans_gnss(gnss):
    
    gnss_re = gnss.replace("[","")
    gnss_re = gnss_re.replace("]","")

    return gnss_re


def send_message(put_LINEID,msg):
    
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + load_config().line_channel_access_token,
    }

    json_data = {
        'to': put_LINEID,
        'messages': [
            {
                'type': 'text',
                'text': msg,
            },
        ],
    }
    
    response = requests.post('https://api.line.me/v2/bot/message/push', headers=headers, json=json_data)
    return 0

 
