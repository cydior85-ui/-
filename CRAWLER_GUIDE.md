# 🤖 크롤러 실행 가이드

전북교육청 게시판에서 자동으로 서식을 수집하는 크롤러를 실행하는 방법입니다.

---

## ✅ 사전 준비

### 1단계: Python 설치 확인
```bash
python3 --version
# 또는
python --version
```

### 2단계: 필요한 라이브러리 설치
```bash
pip install requests beautifulsoup4
# 또는
pip3 install requests beautifulsoup4
```

---

## 🚀 크롤러 실행

### 기본 실행
```bash
python3 crawler.py
```

또는

```bash
python crawler.py
```

### 상세 로그와 함께 실행
```bash
python3 crawler.py 2>&1 | tee crawler.log
```

---

## 📊 실행 결과

성공적으로 실행되면 다음과 같은 출력이 나타납니다:

```
╔════════════════════════════════════════════════════════════╗
║  전북특별자치도교육청 서식 꾸러미 자동 수집 스크립트        ║
╚════════════════════════════════════════════════════════════╝

📥 서식 수집을 시작합니다...

📥 수집 시작: 중등 교무학사업무 길라잡이
  발견한 다운로드 링크: 47개
  ✓ 1. 교무학사 (hwp)
  ✓ 2. 학교생활기록부 관리 (hwp)
  ✓ 3. 결·보강 계획 (hwp)
  ...

📥 수집 시작: 초등 교무학사업무 길라잡이
  발견한 다운로드 링크: 53개
  ...

✓ 총 100개의 서식 수집 완료

==============================================================
📊 수집 결과 요약
==============================================================
총 서식 개수: 100개

분류별 개수:
  교무: 100개

파일형식별 개수:
  hwp: 75개
  xlsx: 20개
  pdf: 5개

==============================================================

✅ 완료! index.html을 열어 확인하세요.
```

---

## 📁 결과 파일

크롤러 실행 후 `forms.json` 파일이 업데이트됩니다.

### 파일 확인
```bash
# 파일이 생성되었는지 확인
ls -lh forms.json

# 내용 확인 (처음 50줄만)
head -50 forms.json

# 전체 항목 수 확인
grep '"id"' forms.json | wc -l
```

### 결과 확인
1. `forms.json` 파일이 업데이트되었으면 성공
2. `index.html`을 웹브라우저에서 열어 확인

---

## 🔧 크롤러 커스터마이징

### 더 많은 게시판 추가

`crawler.py` 에서 `sources` 리스트를 수정:

```python
sources = [
    {
        'name': '중등 교무학사업무 길라잡이',
        'url': 'https://www.jbe.go.kr/board/list.jbe?boardId=BBS_0000067&menuCd=DOM_000000105002003000',
        'category': '교무',
        'page': 1
    },
    # 새로운 게시판 추가
    {
        'name': '부서자료실',
        'url': 'https://www.jbe.go.kr/board/list.jbe?boardId=BBS_...',
        'category': '부서',
        'page': 1
    }
]
```

### 카테고리 수정

```python
'category': '교무'  # 이 부분을 변경
```

다음 카테고리 중 선택:
- `교무`
- `담임`
- `학사`
- `보건`
- `안전`
- `정보`
- `기타`

### 수집 속도 조절

`crawler.py`에서 이 줄을 찾아 수정:

```python
time.sleep(2)  # 2초 → 원하는 초 단위로 변경
```

- 느리게 (안전): `time.sleep(3)` 이상
- 보통: `time.sleep(2)`
- 빠르게: `time.sleep(1)` 이하 (권장하지 않음)

---

## ⚠️ 문제 해결

### 문제 1: "ModuleNotFoundError: No module named 'requests'"

**해결:**
```bash
pip install requests beautifulsoup4
```

### 문제 2: 다운로드 링크가 없음

**확인:**
1. 인터넷 연결 확인
2. 게시판 URL이 정확한지 확인
3. 게시판이 열려있는지 확인

### 문제 3: forms.json 파일이 비어있음

**확인:**
1. 크롤러 로그를 확인하세요
2. 게시판 구조가 변경되었을 수 있습니다
3. HTML 구조를 다시 분석해 crawler.py 수정 필요

---

## 🔄 자동화 (선택사항)

### Windows - 작업 스케줄러

1. **작업 스케줄러** 열기
2. **기본 작업 만들기**
3. **트리거** 설정: 주 1회 (일요일)
4. **작업**: `python3 crawler.py` 실행

### Mac/Linux - crontab

```bash
# crontab 열기
crontab -e

# 매주 일요일 오전 1시에 실행
0 1 * * 0 cd /경로/jbe-seosik && python3 crawler.py
```

---

## 📧 문제 보고

크롤러가 작동하지 않으면:

1. **로그 저장**:
   ```bash
   python3 crawler.py > crawler_error.log 2>&1
   ```

2. **파일 확인**:
   - `forms.json` 파일의 내용 확인
   - `crawler_error.log` 의 에러 메시지 확인

3. **HTML 구조 재분석**:
   - 게시판 방문
   - 개발자 도구(F12) > Elements 탭
   - 실제 HTML 구조 확인 후 `crawler.py` 수정

---

## 💡 팁

- 🔗 **게시판 URL 찾기**: `jbe.go.kr` 에서 원하는 메뉴로 이동 후 URL 복사
- 📄 **하나의 게시판만 테스트**: `sources` 리스트에 1개만 남겨두고 실행
- 🕐 **시간대 선택**: 교육청 서버가 한가한 시간에 실행 (새벽)
- ✏️ **메모**: 매번 수집 후 구글 시트나 엑셀에 정리

---

**질문이 있으면 README.md 와 DEPLOYMENT.md 를 확인하세요!**
