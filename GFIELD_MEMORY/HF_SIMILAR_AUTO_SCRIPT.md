# 프리미어 HF 유사문제 자동 생성 스크립트

> 작성: Claude (관호 지시하에) / 2026.06.15  
> 실행: Cloud Shell / Codex / 텔레봇 어디서든 가능

---

## 사전 준비

```bash
# 환경변수 세팅
export GOOGLE_APPLICATION_CREDENTIALS=~/gfield-drive-worker.json
export GITHUB_TOKEN=your_github_token
export GITHUB_REPO=docssam1/Hyper-Focus-answer-Key

# 패키지 설치
pip install google-cloud-aiplatform google-auth requests pillow --break-system-packages
```

---

## 스크립트 — hf_similar_auto.py

```python
"""
GFIELD 프리미어 하이퍼 포커스 유사문제 자동 생성

흐름:
1. Drive API → 원본 이미지 다운로드
2. Vertex AI Gemini Vision → 이미지 분석 + 유사문제 생성
3. GitHub API → assets/similar/ 이미지 업로드
4. sq-a/b/c.js → imgUrl 필드 patch
"""

import os
import base64
import json
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
import vertexai
from vertexai.generative_models import GenerativeModel, Part

# ── 설정 ──────────────────────────────────────────
CREDENTIALS_PATH = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', '~/gfield-drive-worker.json')
GITHUB_TOKEN = os.environ['GITHUB_TOKEN']
GITHUB_REPO = os.environ.get('GITHUB_REPO', 'docssam1/Hyper-Focus-answer-Key')
GCP_PROJECT = 'project-56629b95-34aa-49fc-8cf'  # 확인 필요
GCP_LOCATION = 'asia-northeast3'

# Drive 폴더 ID (프리미어 시험유형)
DRIVE_FOLDER_ID = '1jMg0m9l7BTSkjgeAo0OJDVH02fi5qpnn'

# typeId별 Drive 파일 ID 매핑
DRIVE_FILE_MAP = {
    1:  '1URE_YndY7-9hANd96BH4QNORrjU202kT',
    2:  '1izACmtZNjecfi1P8xCkp2pcrBEMT98bb',
    3:  '1LUujCTkOWdHHFfONHDfyRi4KorzBmO6x',
    4:  '1rLXIiAjUQ-XiMTDL1Jpk90lPCGngV6h0',
    5:  '17l8AbFtGhRM0zsDvZKANAvv0lHSCJ7T_',
    6:  '1OwhUDu-DFYd-K08ixW3A_CvPVUUvjvaH',
    7:  '1QgdTacsWHuvzpU31nlAMmIr7sB8Qcm5S',
    8:  '1YVvBgEAwW6Lzg2bEMG7ORgnhGz7KEAtF',
    9:  '1-gChjOlE8hcVuw7yqBiTmYmB2WvzwCWa',
    10: '1peOvsjCTsA-BeiJMeLuYbg9ACZIobHK7',
    11: '1oX5OJf4h5oMwKvstXLIga3b080AVAYDo',
    12: '1Q2NbQDr6_mNfpobg5a0z2wzu25JLztO1',
    13: '1IKh1_EgM8KpFBGD6vTqFHkvGShF1GAzt',
    14: '1Vc-moAlNqGi6A88MfYsSKkpY4ExSCCGi',
    15: '1ucWa86phfmL_iFR-UwQinq9Mj8XCtDxq',
    16: '1sjD8nFuOTdA51nijGKejyXuhF_uli16D',
    17: '1ZQWPmVi6sLRseGiviS4liNuOqJS81Xbx',
    18: '14NkAN7rwVRd36BzFwI87KQvaLZOi4SR7',
    19: '15emsZRX6FTuJHAjYDb8xMLgoRZSk_Vz3',
    20: '1qeMtG4vYKM_8-S0nqfUzpl24rfXrPLYy',
    22: '1obF_swj4tuePROxUqxvhezDhaejn9AZL',
    23: '1R2pGMMaopmE-ir_cJdB-5sqKQQIAtdmW',
    24: '1OzNZYQk2AwotJHmRZuSBkeiDHnLI19_I',
    25: '1Mav_S_Evba4OfjzopsxbTZ9HUkxndY-t',
    26: '1zLx1CeWma8i4ThrFP-lbVcfKlc809Dyb',
    27: '1onYEDehOA040OUrxjkhd88wuWOymja_p',
    28: '14DTP93BfWlzhzTZqp0sfyJw2z5cf-BP2',
    29: '1-cCfOhtEaOSGAID4j3ujtlzc-u0T-teQ',
    30: '1pr6OQlEtTEdfT3AhzOMIni2lgmUJPI8B',
    31: '1QHDLFBHxJ3ZMpG8av7kTrrEVuuPiQXG2',
    32: '1HJ1BXbJt441jW_kgfruEW81qISajwZiA',
    33: '1oybK_PW7wzwERmRLkJxKusSuJX3JNvyH',
    35: '1GxblME6K2H6QVizDzF20WQu6OoEfr5Tv',
    36: '10a9qma7ecq-RTfOiuxfvtkkfA74pJLNQ',
    37: '1wxe-sMOmsqmRaVmt7knssJ5Vul6Bzq-V',
    38: '1fp6tmM8pJE-AIHDQx2jMjbTaJ6AdTWet',
    39: '1l6LFbQgaFVZ0PZd8b2ZGUccLdWJ72DkB',
    40: '1jyq6cV-FDaLAWpWMlwfVT8oiKWpqaXjE',
    41: '1rc3XkdZIufL6xUIhqjFCE9GGxU-GiEUt',
    42: '1ro7065of9eZPg2u6UF3AFkDTFXj9rDh2',
    43: '10emBJXn5FSndzFFyIIcZpCy2Dcil_RpX',
    45: '1_T4-D1vkMIgLhlig08vr6lvGFZ_MyGcp',
    49: '1ay481B1zpKQI0tMpbUUn8R9QOWeqOgtA',
    52: '1lCDo4qMt0EoIV3sd1Zkye67oG81X333W',
    54: '1UnRZqp0vS1ZRZPW1hxQV_SHAXCgnYPgC',
}

# sq.js 파일 매핑
SQ_FILE_MAP = {
    **{i: 'premier-hyper-focus/data/sq-a.js' for i in range(1, 18)},
    **{i: 'premier-hyper-focus/data/sq-b.js' for i in range(18, 35)},
    **{i: 'premier-hyper-focus/data/sq-c.js' for i in range(35, 55)},
}


# ── Drive 이미지 다운로드 ──────────────────────────
def download_drive_image(file_id):
    creds = service_account.Credentials.from_service_account_file(
        os.path.expanduser(CREDENTIALS_PATH),
        scopes=['https://www.googleapis.com/auth/drive.readonly']
    )
    service = build('drive', 'v3', credentials=creds)
    content = service.files().get_media(fileId=file_id).execute()
    return content  # bytes


# ── Vertex AI Gemini Vision으로 유사문제 생성 ───────
def generate_similar_problems(image_bytes, type_id):
    vertexai.init(project=GCP_PROJECT, location=GCP_LOCATION)
    model = GenerativeModel('gemini-1.5-pro-vision')

    image_part = Part.from_data(image_bytes, mime_type='image/png')

    prompt = f"""
이 이미지는 초등학교 사고력 수학 문제(typeId: {type_id})입니다.

이 문제를 참고해서 숫자/조건만 다른 유사문제 2개를 만들어주세요.

규칙:
- 문제 유형과 풀이 방법은 동일하게
- 숫자/조건/이름만 다르게
- 한국어로
- JSON 형식으로만 출력 (다른 텍스트 없이)

출력 형식:
{{
  "q1": {{
    "question": "문제 텍스트",
    "answer": "정답",
    "solution": "풀이",
    "hint": "힌트"
  }},
  "q2": {{
    "question": "문제 텍스트",
    "answer": "정답",
    "solution": "풀이",
    "hint": "힌트"
  }}
}}
"""

    response = model.generate_content([image_part, prompt])
    text = response.text.strip()
    # JSON 파싱
    if '```' in text:
        text = text.split('```')[1].replace('json', '').strip()
    return json.loads(text)


# ── GitHub 이미지 업로드 ───────────────────────────
def upload_to_github(image_bytes, path, commit_msg):
    b64 = base64.b64encode(image_bytes).decode('utf-8')
    url = f'https://api.github.com/repos/{GITHUB_REPO}/contents/{path}'
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Content-Type': 'application/json'
    }
    # 기존 파일 SHA 확인
    r = requests.get(url, headers=headers)
    sha = r.json().get('sha') if r.status_code == 200 else None

    data = {'message': commit_msg, 'content': b64}
    if sha:
        data['sha'] = sha

    r = requests.put(url, headers=headers, json=data)
    if r.status_code in [200, 201]:
        print(f'  ✅ 업로드 완료: {path}')
    else:
        print(f'  ❌ 업로드 실패: {r.status_code} {r.text[:200]}')


# ── sq.js imgUrl patch ────────────────────────────
def patch_sq_js(type_id):
    sq_file = SQ_FILE_MAP.get(type_id)
    if not sq_file:
        return

    url = f'https://api.github.com/repos/{GITHUB_REPO}/contents/{sq_file}'
    headers = {'Authorization': f'token {GITHUB_TOKEN}'}
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        print(f'  ❌ sq.js 읽기 실패')
        return

    data = r.json()
    content = base64.b64decode(data['content']).decode('utf-8')
    sha = data['sha']

    # A, B 각각 imgUrl 추가
    for idx, letter in enumerate(['A', 'B'], 1):
        old = f'id: "{type_id}-{letter}",'
        new = f'id: "{type_id}-{letter}",\n        imgUrl: "./assets/similar/sq-{type_id:02d}-{idx}.jpg",'
        if old in content and 'imgUrl' not in content.split(old)[1][:50]:
            content = content.replace(old, new, 1)
            print(f'  ✅ {type_id}-{letter} imgUrl 추가')
        else:
            print(f'  ⚠️  {type_id}-{letter} 이미 있거나 못 찾음')

    # GitHub 업로드
    b64_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
    r = requests.put(url, headers=headers, json={
        'message': f'patch: typeId {type_id} imgUrl 추가',
        'content': b64_content,
        'sha': sha
    })
    if r.status_code in [200, 201]:
        print(f'  ✅ sq.js 패치 완료')
    else:
        print(f'  ❌ sq.js 패치 실패: {r.status_code}')


# ── 메인 실행 ─────────────────────────────────────
def run(type_ids):
    for type_id in type_ids:
        print(f'\n[typeId {type_id}] 시작...')

        file_id = DRIVE_FILE_MAP.get(type_id)
        if not file_id:
            print(f'  ⚠️  Drive 파일 ID 없음, 건너뜀')
            continue

        # 1. 이미지 다운로드
        print(f'  1. Drive 이미지 다운로드...')
        image_bytes = download_drive_image(file_id)

        # 2. GitHub 이미지 업로드 (원본 그대로 2개)
        print(f'  2. GitHub 이미지 업로드...')
        for idx in [1, 2]:
            path = f'premier-hyper-focus/assets/similar/sq-{type_id:02d}-{idx}.jpg'
            upload_to_github(image_bytes, path, f'add: typeId {type_id} 유사문제 이미지 {idx}')

        # 3. sq.js imgUrl 패치
        print(f'  3. sq.js imgUrl 패치...')
        patch_sq_js(type_id)

        print(f'[typeId {type_id}] 완료 ✅')


if __name__ == '__main__':
    import sys
    # 실행 예시: python hf_similar_auto.py 4
    # 또는: python hf_similar_auto.py 1 2 3 4 5
    if len(sys.argv) > 1:
        ids = [int(x) for x in sys.argv[1:]]
    else:
        # 기본: 전체 실행
        ids = list(DRIVE_FILE_MAP.keys())

    run(ids)
```

---

## 실행 방법

```bash
# typeId 4번만
python hf_similar_auto.py 4

# 여러 개
python hf_similar_auto.py 1 2 3 4 5

# 전체
python hf_similar_auto.py
```

---

## 주의

- `GCP_PROJECT` 확인 필요 (현재 `project-56629b95-34aa-49fc-8cf`)
- Vertex AI Gemini Vision API 활성화 필요
- GITHUB_TOKEN 환경변수 세팅 필요
- 이미지는 원본 그대로 2개 올림 (크롭/변형은 Gemini Vision이 별도 처리)
