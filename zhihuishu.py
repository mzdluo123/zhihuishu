import requests
import data_encoder
import json
from typing import Tuple


def login(account: str, password: str) -> str:
    # 登录

    raw_data = {"password": password, "areaCode": "86", "appVersion": "4.3.8", "clientType": "1",
                "imei": "+0a386f8f9154844b2b32c6", "account": account, "verification": False}

    encoded = data_encoder.encode(json.dumps(raw_data))
    rep = requests.post('https://appstudent.zhihuishu.com/appstudent/newuser/userLoginByAccount',
                        data={'paramJsonStr': encoded, 'timeNote': 1515340800})

    data = rep.json()
    if data['status'] != '200':
        raise Exception("登录失败")
    return data['rt']['userUUID']


def class_list(uuid: str) -> list:
    # 课程列表
    rep = requests.post('https://appstudent2c.zhihuishu.com/app_2c/studyv2/queryStudingList',
                        data={'page': 1, 'pageSize': 20, 'uuid': uuid})
    result = []
    print(rep.text)
    for i in rep.json()['rt']:
        print(i['name'])
    return result


def group_list(uuid: str) -> list:
    # 群列表
    rep = requests.post('https://ctapp.zhihuishu.com/app-commonserv-classroomtools/commonChat/group/chatGroupList',
                        data={'uuid': uuid})
    result = []
    for i in rep.json()['rt']['groups']:
        result.append((i['groupName'], i['groupId']))
    return result


def sign_list(uuid: str, groupId: str) -> dict:
    # 签到列表
    rep = requests.post(
        'https://ctapp.zhihuishu.com/app-commonserv-classroomtools/commonChat/sign/chatCheckStudentHistory',
        data={'groupId': groupId, 'uuid': uuid, "sUuid": uuid, 'isAddMeetingCourseSign': 1})
    # print(rep.text)
    return rep.json()['rt']


def sign(checkId: str, uuid: str, gesture: str) -> Tuple[bool, str]:
    # 签到
    rep = requests.post("https://ctapp.zhihuishu.com/app-commonserv-classroomtools/commonChat/sign/chatStudentCheck",
                        data={'checkGesture': gesture, 'checkId': checkId, 'checkType': 2, 'latitude': '',
                              'longitude': '', 'uuid': uuid})
    data = rep.json()['rt']
    if data['resultStatus'] == 1:
        return True, data['resultMessage']
    else:
        return True, data['resultMessage']


def sign_info(checkId: str, uuid: str) -> dict:
    # 签到信息
    """
    checkStatus
        0  签到被删除
        1  未签到
        2  已签到
        3  未签到，签到已结束
        4  你不在群
    """
    rep = requests.post("https://ctapp.zhihuishu.com/app-commonserv-classroomtools/commonChat/sign/chatCheckInfo",
                        data={'checkId': checkId, 'uuid': uuid})
    data = rep.json()['rt']
    return data


def group_user_info(uuid: str, role: str = "1", groupId: str = "1"):
    rep = requests.post("https://ctapp.zhihuishu.com/app-commonserv-classroomtools/commonChat/group/groupUserInfo",
                        data={'groupId': groupId, "role": 1, 'uuid': uuid})
    data = rep.json()['rt']
    return data
