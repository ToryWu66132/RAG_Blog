import os

import requests


def _parse_feishu_response(res):
    try:
        return res.json()
    except requests.exceptions.JSONDecodeError as exc:
        raise Exception(
            f"Feishu API returned non-JSON response: status={res.status_code}, body={res.text[:500]}"
        ) from exc


def get_tenant_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"

    res = requests.post(url, json={
        "app_id": os.getenv("FEISHU_APP_ID"),
        "app_secret": os.getenv("FEISHU_APP_SECRET")
    })

    data = _parse_feishu_response(res)

    if data.get("code") != 0:
        raise Exception(data)

    return data["tenant_access_token"]

def create_doc(token, title):
    url = "https://open.feishu.cn/open-apis/docx/v1/documents"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    res = requests.post(url, headers=headers, json={"title": title})
    data = _parse_feishu_response(res)

    if data.get("code") != 0:
        raise Exception(data)

    return data["data"]["document"]["document_id"]

def write_doc(token, doc_id, content):
    url = f"https://open.feishu.cn/open-apis/docx/v1/documents/{doc_id}/blocks/{doc_id}/children"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    paragraphs = content.split("\n")

    children = [
        {
            "block_type": 2,
            "text": {
                "elements": [
                    {
                        "text_run": {
                            "content": p
                        }
                    }
                ]
            }
        }
        for p in paragraphs if p.strip()
    ]

    res = requests.post(url, headers=headers, json={"children": children, "index": 0})
    data = _parse_feishu_response(res)

    if data.get("code") != 0:
        raise Exception(data)

    return f"https://feishu.cn/docx/{doc_id}"

def upload_to_feishu(title, content):
    token = get_tenant_token()
    doc_id = create_doc(token, title)
    return write_doc(token, doc_id, content)
