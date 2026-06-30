# TASK: 입장 화면에 마스터 코드(테스트용) 추가

## 무엇을 / 왜
원장님이 매번 승인번호·이름·연락처를 입력해야 해서 로드맵 화면을 빠르게 테스트하기 어렵습니다.
승인번호 칸에 특정 마스터 코드를 입력하면, 이름·연락처 입력 없이 바로 진단 화면으로 들어가고
시트 저장/조회를 건너뛰는(=학생 목록에 기록 안 남고 재작성 횟수 제한도 없는) 테스트 모드를 추가합니다.

## 대상 파일 (repo: docssam1/lete-on)
- `roadmap/index.html`

## 마스터 코드 값
```
docssam
```

## 수정 내용

`startStandardDiagnosis` 함수를 찾으세요 (대략 아래 형태):

```js
async function startStandardDiagnosis(){
  const code=document.getElementById('approvalCode').value.trim();
  const name=document.getElementById('approvalName').value.trim();
  const phone=document.getElementById('approvalPhone').value.trim();
  const error=document.getElementById('approvalError');
  if(!code||!name||!phone){error.textContent='승인번호, 학생 이름, 연락처를 모두 입력해 주세요.';return;}
  CURRENT_CODE = code;
  document.getElementById('studentName').value=name;

  // 저장 서버가 연결돼 있으면 기존 기록 조회
  if(storeEnabled()){
    error.textContent='확인 중…';
    SAVED_RECORD = await fetchSaved(code);
    error.textContent='';
    if(SAVED_RECORD && SAVED_RECORD.diag){
      // 기존 데이터 있음 → 새로/불러오기 분기
      document.getElementById('approvalGate').style.display='none';
      showReentryChoice(name);
      return;
    }
  }
  proceedToWelcome(name);
}
```

**함수 맨 위에 마스터 코드 분기를 추가**하세요 (함수 시작 부분, `const code=...` 줄 바로 다음):

```js
async function startStandardDiagnosis(){
  const code=document.getElementById('approvalCode').value.trim();

  // ===== 마스터 코드 (테스트용, 시트 저장/조회 건너뜀) =====
  const MASTER_CODE = 'docssam';
  if(code === MASTER_CODE){
    CURRENT_CODE = '';            // 저장 안 함 (storeEnabled 분기 자체를 안 타도록 빈 값)
    SAVED_RECORD = null;
    document.getElementById('studentName').value = '테스트';
    document.getElementById('approvalName').value = '테스트';
    document.getElementById('approvalPhone').value = '010-0000-0000';
    proceedToWelcome('테스트');
    return;
  }
  // ===== 마스터 코드 분기 끝 =====

  const name=document.getElementById('approvalName').value.trim();
  const phone=document.getElementById('approvalPhone').value.trim();
  const error=document.getElementById('approvalError');
  if(!code||!name||!phone){error.textContent='승인번호, 학생 이름, 연락처를 모두 입력해 주세요.';return;}
  CURRENT_CODE = code;
  document.getElementById('studentName').value=name;

  // 저장 서버가 연결돼 있으면 기존 기록 조회
  if(storeEnabled()){
    error.textContent='확인 중…';
    SAVED_RECORD = await fetchSaved(code);
    error.textContent='';
    if(SAVED_RECORD && SAVED_RECORD.diag){
      // 기존 데이터 있음 → 새로/불러오기 분기
      document.getElementById('approvalGate').style.display='none';
      showReentryChoice(name);
      return;
    }
  }
  proceedToWelcome(name);
}
```

## 동작 확인 포인트
- `CURRENT_CODE`가 빈 문자열(`''`)이면, 설문 제출 시 저장 로직(`if(storeEnabled() && CURRENT_CODE){...}`)의 `CURRENT_CODE` 조건이 false가 되어 **저장을 자동으로 건너뜀** (기존 코드 그대로 활용, 별도 수정 불필요).
- 마스터 코드 입력 시 이름·연락처 입력칸은 채워지지만, **사용자가 직접 입력칸을 거치지 않고 바로 환영 화면 → 진단 설문으로 진입**해야 함.
- 진단 설문(STEP 1)은 마스터 코드든 일반 승인번호든 동일하게 그대로 진행 (이름·나이·사고력·교과·연산 입력은 평소처럼 함).

## 작업 방법
1. GitHub에서 `roadmap/index.html` fetch
2. 위 old 블록(`startStandardDiagnosis` 함수 전체)을 new 블록으로 교체
3. JS 문법 확인
4. push (커밋: `feat(approval): 테스트용 마스터 코드(docssam) 추가`)

## 주의
- 마스터 코드는 승인번호 칸에만 입력하면 작동 (이름·연락처 칸은 비워둬도 됨, 자동으로 "테스트"/"010-0000-0000" 채워짐).
- 파일 전체를 다시 만들지 말 것. `startStandardDiagnosis` 함수만 정확히 교체.
- 교체 전 해당 함수가 파일에 정확히 1곳만 있는지 확인.
