#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GFIELD HF — Gemini Vision SVG 유사문제 생성 스크립트
프로젝트: solve (gen-lang-client-0329093850)

준비:
  gcloud config set project gen-lang-client-0329093850

사용법:
  ~/gfield-hq/venv/bin/python3 ~/hf_svg_gen.py 1   # 배치 1 (typeId 01~05)
  ~/gfield-hq/venv/bin/python3 ~/hf_svg_gen.py 2   # 배치 2 (typeId 06~10)
  ...배치 11까지

각 배치 실행 후 ~/hf_batch_NN.json 검토 → 다음 배치 진행.
"""

import sys, json, base64, urllib.request, urllib.parse, os, subprocess

PROJECT_ID = "gen-lang-client-0329093850"  # solve 프로젝트 (크레딧 있음)
LOCATION = "us-central1"
MODEL = "gemini-2.0-flash"

IMG_REPO = "docssam1/Hyper-Focus-answer-Key"
IMG_PATH = "premier-hyper-focus/assets/problems"

FILES = {
    1: "1 특정 모양과 똑같이 만들기 위해 추가로 필요한 쌓기나무의 개수 구하기.png",
    2: "2 정육면체를 완성하기 위해 채우기 위해 필요한 쌓기 나무의 개수 구하기.png",
    3: "3 흑백이 교차로 쌓인 쌓기나무에서 특정 색상의 개수 구하기.png",
    4: "4 덩어리에 구멍을 뚫었을 때, 구멍이 뚫리지 않은 온전한 쌓기나무의 개수 구하기.png",
    5: "5 보이지 않는 쌓기 나무의 개수 구하기 .png",
    6: "6. 보는 방향에 따른 모양.png",
    7: "7 주어진 전개도로 만들 수 있거나,없는 정육면체 모양 찾기.png",
    8: "8 주사위를 규칙에 따라 굴리거나 이동시켰을 때 윗면에 나오는 수 구하기.png",
    9: "9 바탕그림에서의 쌓기나무의 개수.png",
    10: "10 색종이 2~4장을 겹쳤을 때, 겹쳐진 부분의 수 구하기.png",
    11: "11 앞뒤에 같은 수가 적힌 직사각형 색종이를 접었을 때 윗면에 나오는 수 구하기.png",
    12: "12 색종이를 여러 번 접고 펼친 후의 구멍 개수 구하기.png",
    13: "13 여러 가지 모양의 펜토미노 조각으로 직사각형 빈틈없이 채우기.png",
    14: "14 특정 도형을 다양한 크기의 정사각형들로 나눌 때 필요한 최소 개수 구하기.png",
    15: "15 조건에 맞게 주어진 평면도형 나누기.png",
    16: "16 복잡한 도형 안에서 크고 작은 사각형,삼각형의 총 개수 세기.png",
    17: "17 대각선이 있는 도형 안에서 크고 작은 사각형,삼각형의 총 개수 세기.png",
    18: "18 쌓기나무 4개를 붙여 나올 수 있는 가짓수.png",
    19: "19 지오보드에서의 도형의 개수.png",
    20: "20 길이가 다른 여러 선분을 조합하여 만들 수 있는 새로운 선분 길이의 가짓수 구하기.png",
    21: "21 조건에 알맞은 수.png",
    22: "22 두 자리 수 덧셈 등식에서 숫자 2개의 위치를 바꿔 올바른 식 만들기.png",
    23: "23 숫자들 사이에 덧셈(+) 또는 뺄셈(-) 기호를 넣어 특정 값이 나오는 가짓수 구하기.png",
    24: "24 숫자들 사이에 덧셈(+) 또는 뺄셈(-) 기호를 지워 특정 값이 나오는 가짓수 구하기.png",
    25: "25. 크기를 만족하는 공통의 수 .png",
    26: "26 성냥개비를 옮겨 올바른 연산식 만들기 (또는 도형 만들기).png",
    27: "27 벌집 모양의 수 배열에서 규칙을 찾아 연산 완성하기.png",
    28: "28. 가로로 배열되거나 3개가 겹친 벤다이어그램 영역 안의 수의 합이 같도록 수 배치하기.png",
    29: "29. 아래,오른쪽으로 일정하게  커지는 수 배열표에서 특정 위치의 수 구하기.png",
    30: "30. 과녁에 화살을 쏘아 만들수 있는 점수.png",
    31: "31. 기호나 도형이 나타내는 숨겨진 수 구하기.png",
    32: "32. 거울에 비친 디지털 수의 원래 합.png",
    33: "33. 가위,바위,보 하여 계단 오르거나 내려가기.png",
    34: "34. 숫자 카드로  수를 만들어 특정 연산의 최댓값 또는 최솟값 구하기.png",
    35: "35. 주어진 단서들을 바탕으로 줄을 세우고 등수(순위) 정확히 추론하기.png",
    36: "36. 줄 세우기에서 특정인들 사이에 있는 사람 수의 최댓값 및 최솟값 구하기.png",
    37: "37. 원 모양에서의 위치.png",
    38: "38. 원 모양에서 마주보는 사람의 순서 정하기.png",
    39: "39. 논리표(Matrix)를 이용하여 조건에 맞는 항목(좋아하는 음식, 과일 등) 올바르게 짝짓기.png",
    40: "40. 주어진 수 규칙을 이용해 암호 풀기유형.png",
    41: "41. 주어진 패턴 규칙을 이용해 암호 풀기유형.png",
    42: "42. 5칸의 빈 공간을 1칸짜리와 2칸짜리 막대로 채우는 모든 가짓수 구하기.png",
    43: "43. 4가지 색 중 3개를 골라  트리미노를 칠하는 가짓수 구하기.png",
    44: "44. 주어진 숫자 카드를 사용하여 조건에 맞는 세 자리 수의 개수 구하기.png",
    45: "45. 조건이 주어진 길 찾기에서 최단 거리로 이동하는 가짓수 구하기.png",
    46: "46. 식이나 문장 조건을 보고 결과를 거꾸로 계산하여 처음 수 구하기.png",
    47: "47. 표의 변화 과정을 거꾸로 추적하여 문제 해결하기.png",
    48: "48. 일의 양과 시간 계산.png",
    49: "49. 비례식 활용.png",
    50: "50. 서로 다른 단위 길이를 이용한 길이 문제.png",
    51: "51. 시간 범위 내에서 시간대에 따라 시계탑의 종이 울린 총 횟수 구하기.png",
    52: "52. 3~4개의 양팔저울 결과를 보고 동물이나 과일의 무게 비교하기.png",
    53: "53 서로 다른 단위길이를 이용한 활용 문제.png",
    54: "54. 피보나치 수열 등 특정 수열에서 홀수(또는 짝수)가 나오는 개수 구하기.png",
}

PROMPT_TEMPLATE = """너는 GFIELD 프리미어 하이퍼 포커스의 유사문항 생성 전문가다.
첨부된 원본 문제 이미지(typeId {tid}, 제목: {title})를 직접 보고 분석해라.

규칙:
1. 원본 이미지의 핵심 도형/구조를 파악한다.
2. 숫자/조건만 바꾼 유사문항 2개를 SVG로 만든다.
3. 그림 문제는 반드시 그림(SVG)으로 표현한다. 텍스트로 바꾸지 마라.
4. viewBox는 "0 0 400 300", stroke 기반 path 위주.
5. 색상: 기본 #0d1b2a, 강조 #e9c176.
6. 금지어: 교차점, 단면화, 단면, 교차 (유아어 대체: 교차점->만나는 곳, 단면->잘린 면).
7. 7세 유아 대상 따뜻한 말투.
8. 정답을 직접 풀어서 검산한 뒤에만 verified:true.

아래 JSON만 출력해라. 다른 텍스트 없이:
{{
  "typeId": "{tid_pad}",
  "title": "이미지에서 읽은 정확한 제목",
  "legacyGroup": "A 또는 B",
  "functionalGroup": "공간/기하 또는 평면/논리 또는 연산/규칙 또는 가중치/활용",
  "originalSummary": "원본 문제 구조 요약",
  "originalAnswer": "원본 정답",
  "fixedSimilars": [
    {{
      "id": "{tid_pad}_1",
      "difficulty": "same",
      "svg": "<svg viewBox=\\"0 0 400 300\\" xmlns=\\"http://www.w3.org/2000/svg\\">...전체 SVG...</svg>",
      "answer": "정답",
      "solution": "풀이(유아어)",
      "hint": "힌트(유아어)",
      "verified": true
    }},
    {{
      "id": "{tid_pad}_2",
      "difficulty": "same",
      "svg": "<svg viewBox=\\"0 0 400 300\\" xmlns=\\"http://www.w3.org/2000/svg\\">...전체 SVG...</svg>",
      "answer": "정답",
      "solution": "풀이(유아어)",
      "hint": "힌트(유아어)",
      "verified": true
    }}
  ]
}}
"""

def get_image_b64(filename):
    # GitHub Contents API로 받기 (한글 파일명 인코딩 문제 회피)
    api = f"https://api.github.com/repos/{IMG_REPO}/contents/{IMG_PATH}/{urllib.parse.quote(filename)}?ref=main"
    req = urllib.request.Request(api, headers={"Accept": "application/vnd.github.v3+json"})
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        req.add_header("Authorization", f"token {tok}")
    with urllib.request.urlopen(req) as r:
        info = json.loads(r.read())
    if info.get("content"):
        return info["content"].replace("\n", "")
    # 대용량이면 download_url 사용
    durl = info["download_url"]
    with urllib.request.urlopen(durl) as r:
        return base64.b64encode(r.read()).decode()

def get_access_token():
    return subprocess.check_output(["gcloud","auth","print-access-token"]).decode().strip()

def call_gemini(img_b64, prompt):
    token = get_access_token()
    url = f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/{MODEL}:generateContent"
    payload = {
        "contents": [{
            "role": "user",
            "parts": [
                {"inlineData": {"mimeType": "image/png", "data": img_b64}},
                {"text": prompt}
            ]
        }],
        "generationConfig": {"temperature": 0.4, "maxOutputTokens": 8192}
    }
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req) as r:
        res = json.loads(r.read())
    return res["candidates"][0]["content"]["parts"][0]["text"]

def main():
    if len(sys.argv) < 2:
        print("사용법: python3 hf_svg_gen.py <배치번호 1~11>")
        return
    batch = int(sys.argv[1])
    start = (batch - 1) * 5 + 1
    end = min(start + 4, 54)
    print(f"=== 배치 {batch}: typeId {start:02d}~{end:02d} ===\n")

    results = []
    for tid in range(start, end + 1):
        title = FILES[tid].rsplit(".png", 1)[0]
        print(f"[typeId {tid:02d}] {title[:30]}... 처리중")
        try:
            img_b64 = get_image_b64(FILES[tid])
            prompt = PROMPT_TEMPLATE.format(tid=tid, tid_pad=f"{tid:02d}", title=title)
            raw = call_gemini(img_b64, prompt).strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            data = json.loads(raw.strip())
            results.append(data)
            a1 = data['fixedSimilars'][0].get('answer','?')
            a2 = data['fixedSimilars'][1].get('answer','?')
            print(f"  OK — 정답: {a1}, {a2}")
        except Exception as e:
            print(f"  ERROR: {e}")

    outpath = os.path.expanduser(f"~/hf_batch_{batch:02d}.json")
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n저장: {outpath}  ({len(results)}개)")
    print(f"검토 후 업로드: python3 ~/hf_svg_push.py {batch}")

if __name__ == "__main__":
    main()
