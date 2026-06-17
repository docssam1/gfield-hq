## PATCH 1 — 탭바에 유사문제 버튼 + view-similar 섹션 추가

FIND:
      <button class="tab-btn" id="btn-list" onclick="setView('list')">목록으로 보기</button>
    </div>
    <div id="view-quick"

REPLACE:
      <button class="tab-btn" id="btn-list" onclick="setView('list')">목록으로 보기</button>
      <button class="tab-btn" id="btn-similar" onclick="setView('similar')">유사문제</button>
    </div>
    <div id="view-similar" class="checklist-section"><div class="category-block"><div class="category-header"><div class="category-title">유사문제 훈련</div><div class="category-divider"></div></div><div id="similar-filter" style="display:flex;gap:8px;margin-bottom:16px;flex-wrap:wrap;"><button class="sim-diff-btn active" data-diff="easy" onclick="setSimilarDiff('easy')">🟢 쉬운 문제</button><button class="sim-diff-btn" data-diff="same" onclick="setSimilarDiff('same')">🟡 같은 난이도</button><button class="sim-diff-btn" data-diff="hard" onclick="setSimilarDiff('hard')">🔴 어려운 문제</button></div><div id="similar-list"></div></div></div>
    <div id="view-quick"

---

## PATCH 2 — setView 함수 확장 + 유사문제 렌더 함수 추가

FIND:
function setView(v){['quick','area','list'].forEach(n=>{document.getElementById(`view-${n}`).classList.toggle('active',v===n);document.getElementById(`btn-${n}`).classList.toggle('active',v===n)});}

REPLACE:
function setView(v){['quick','area','list','similar'].forEach(n=>{const vs=document.getElementById(`view-${n}`);const bs=document.getElementById(`btn-${n}`);if(vs)vs.classList.toggle('active',v===n);if(bs)bs.classList.toggle('active',v===n)});if(v==='similar')renderSimilarUI();}
let hfData=null;let currentSimilarDiff='easy';
function setSimilarDiff(diff){currentSimilarDiff=diff;document.querySelectorAll('.sim-diff-btn').forEach(b=>b.classList.toggle('active',b.dataset.diff===diff));renderSimilarList();}
async function renderSimilarUI(){if(!hfData){try{const res=await fetch('./data/hf_data.json');hfData=await res.json();}catch(e){document.getElementById('similar-list').innerHTML='<p style="color:red">데이터 로드 실패</p>';return;}}renderSimilarList();}
function renderSimilarList(){const wrongIds=selectedSet.size>0?Array.from(selectedSet):[];const container=document.getElementById('similar-list');if(wrongIds.length===0){container.innerHTML='<p style="text-align:center;color:#888;padding:24px">먼저 틀린 문제를 체크해 주세요.</p>';return;}if(!hfData){container.innerHTML='<p style="text-align:center;color:#888">데이터 로딩 중...</p>';return;}let html='';wrongIds.forEach(id=>{const item=hfData.find(d=>d.typeId===id);if(!item)return;const sims=item.fixedSimilars||[];const sim=sims.find(s=>s.difficulty===currentSimilarDiff)||sims[0];if(!sim)return;html+=`<div class="sim-card" style="border:1px solid #ddd;border-radius:10px;padding:16px;margin-bottom:12px;background:#fff;"><div style="font-size:.75rem;color:#888;margin-bottom:6px">유형 ${String(id).padStart(2,'0')} · ${item.title}</div><div style="font-weight:600;margin-bottom:10px;line-height:1.5">${sim.text}</div><details><summary style="cursor:pointer;color:var(--navy);font-weight:600">정답 및 풀이 보기</summary><div style="margin-top:10px;padding:12px;background:#f8f8f8;border-radius:8px"><div style="margin-bottom:6px"><strong>정답:</strong> ${sim.answer}</div><div style="line-height:1.6;color:#444">${sim.answerStory||''}</div></div></details></div>`;});container.innerHTML=html||'<p style="text-align:center;color:#888;padding:24px">해당 난이도 유사문제가 없습니다.</p>';}

---

## PATCH 3 — CSS 추가 (첫 번째 </style> 바로 앞)

FIND:
</style>

REPLACE (첫 번째만):
.sim-diff-btn{padding:7px 16px;border:1px solid #ddd;border-radius:20px;background:#fff;cursor:pointer;font-size:.82rem;font-weight:500;transition:all .2s}
.sim-diff-btn.active{background:var(--navy);color:#fff;border-color:var(--navy)}
</style>
