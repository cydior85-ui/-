# 🚀 GitHub Pages 배포 완벽 가이드

## 5분 안에 배포하기

### 📋 준비물
- GitHub 계정 (없으면 https://github.com/signup 에서 가입)
- 이 폴더의 4개 파일

---

## ✅ 1단계: GitHub 저장소 만들기

### Step 1-1: GitHub에서 New Repository 생성
1. https://github.com/new 방문
2. **Repository name** 입력: `jbe-seosik`
3. **Description** (선택사항): `전북특별자치도교육청 서식 꾸러미`
4. **Public** 선택 (중요!)
5. ✅ **Create repository** 클릭

### Step 1-2: 파일 업로드
**방법 A: 웹 인터페이스로 업로드 (가장 쉬움)**

1. 생성된 저장소 페이지에서 **"Add file" > "Upload files"** 클릭
2. 다음 4개 파일을 드래그앤드롭:
   - `index.html`
   - `forms.json`
   - `crawler.py`
   - `README.md`
3. **Commit changes** 클릭

**방법 B: Git CLI로 업로드 (터미널)**

```bash
# 1. 이 폴더로 이동
cd jbe-seosik

# 2. Git 초기화
git init

# 3. GitHub와 연결 (YOUR-USERNAME을 자신의 깃허브 아이디로 변경)
git remote add origin https://github.com/YOUR-USERNAME/jbe-seosik.git

# 4. 파일 추가 및 커밋
git add .
git commit -m "Initial commit: 전북교육청 서식 꾸러미"

# 5. 푸시
git branch -M main
git push -u origin main
```

---

## ✅ 2단계: GitHub Pages 활성화

1. GitHub 저장소 페이지에서 **Settings** 탭 클릭
2. 좌측 메뉴에서 **Pages** 선택
3. **Source** 설정:
   - Branch: **main** 선택
   - Folder: **/ (root)** 선택
4. **Save** 클릭
5. 페이지 새로고침하면 배포 링크 표시됨:
   ```
   ✅ Your site is live at https://YOUR-USERNAME.github.io/jbe-seosik
   ```

---

## 🎉 완료!

`https://YOUR-USERNAME.github.io/jbe-seosik` 에 접속하면 사이트가 보입니다.

**예시:**
- 계정명이 `kimji1416`이면: https://kimji1416.github.io/jbe-seosik

---

## 🔄 다음 단계: 데이터 채우기

현재는 샘플 데이터 10개만 있습니다. 실제 서식을 추가해보세요.

### 방법 1️⃣: 수동으로 추가 (가장 빠름)

1. **GitHub에서 forms.json 편집**
   - 저장소 > `forms.json` 클릭
   - ✏️ **Edit this file** 클릭
   - 샘플 형식을 참고하여 새 서식 추가
   - **Commit changes** 클릭

2. **JSON 형식:**
```json
{
  "id": "011",
  "title": "새로운 서식명",
  "category": "교무",        // 교무, 담임, 학사, 보건, 안전, 정보
  "subcategory": "계획",
  "date": "2026-07-26",
  "source": "전북특별자치도교육청",
  "download_url": "https://다운로드링크",
  "description": "간단한 설명",
  "file_type": "hwp"        // hwp, xlsx, pdf, docx 등
}
```

### 방법 2️⃣: 파이썬 크롤러로 자동 수집 (권장)

1. **본인 컴퓨터에서:**
   ```bash
   # 저장소 복제
   git clone https://github.com/YOUR-USERNAME/jbe-seosik.git
   cd jbe-seosik
   
   # 필요한 패키지 설치
   pip install requests beautifulsoup4
   
   # 크롤러 설정 후 실행
   python3 crawler.py
   ```

2. **crawler.py의 sources 설정** (중요!)
   
   `crawler.py`를 열어 수집할 게시판 URL을 입력:
   
   ```python
   sources = [
       {
           'name': '교무학사업무 길라잡이',
           'url': '수집할_게시판_URL',  # ← 여기 수정
           'category': '교무',
           'selector': 'table tr'       # ← 게시판 구조에 맞게 수정
       },
   ]
   ```

3. **수집 후 GitHub에 푸시:**
   ```bash
   git add forms.json
   git commit -m "Update: 크롤러로 수집한 서식 데이터"
   git push
   ```

---

## 🎨 커스터마이징 팁

### 색상 변경
`index.html` 에서 찾기(Ctrl+F): `#1a237e`
→ 16진수 색상코드 변경 (예: `#FF6B6B`)

### 제목/설명 수정
`index.html` 에서:
```html
<h1>🏫 전북특별자치도교육청 서식 꾸러미</h1>
<!-- ↑ 여기 수정 -->

<p>전북교육청 서식 및 자료를 한곳에서 검색하고 다운로드하세요</p>
<!-- ↑ 여기도 수정 가능 -->
```

### 카테고리 추가
`index.html`에서:
```html
<select id="categoryFilter">
    <option value="">전체</option>
    <option value="교무">교무</option>
    <option value="새카테고리">새카테고리</option>  <!-- 추가 -->
</select>
```

---

## 🔍 게시판 선택 가이드

좋은 수집 대상:
1. ✅ **전북특별자치도교육청 홈페이지** (jbe.go.kr)
   - 부서별 자료실
   - 공시 자료

2. ✅ **각 지원청 홈페이지**
   - 전주, 군산, 익산, 정읍, 남원, 김제, 완주, 진안, 무주, 장수, 임실, 순창, 고창, 부안
   - 학교업무지원센터

3. ✅ **jbwork.oopy.io**
   - 이미 정리된 공통양식들
   - 하지만 수집은 권리자 동의 필요 가능

---

## ⚠️ 주의사항

### 크롤러 설정 시
- 게시판마다 HTML 구조가 다릅니다
- 개발자 도구(F12) > Elements에서 구조 확인 후 `selector` 수정
- 과도한 요청으로 서버 부하 주지 않기 (1초 지연 유지)

### 다운로드 링크
- 핫링크 차단된 경우: 게시글 URL로 변경
- 상대 경로: 절대 경로로 변환 필요

### 저작권
- ⚠️ 공개된 공식 문서만 수집
- 저작권 명시 (README.md의 고지문 유지)

---

## 🆘 문제 해결

| 증상 | 해결법 |
|-----|-------|
| "404 Not Found" | GitHub Pages 설정 확인 (Settings > Pages) |
| "forms.json을 찾을 수 없음" | 파일이 main 브랜치의 루트에 있는지 확인 |
| 크롤러가 데이터를 찾지 못함 | selector가 실제 게시판 구조와 맞는지 확인 |
| 다운로드 링크가 작동 안 함 | URL이 올바른지, 핫링크가 차단되었는지 확인 |

---

## 💡 추천 다음 단계

1. **샘플 데이터로 테스트**: 현재 10개 샘플로 먼저 확인
2. **카테고리 확정**: 전북에 맞는 분류 정하기
3. **게시판 조사**: 수집할 주요 게시판 리스트 만들기
4. **크롤러 커스터마이징**: 각 게시판의 HTML 구조 분석 후 설정
5. **자동화 설정**: (선택) GitHub Actions로 주간 자동 갱신

---

## 📞 추가 지원

- **README.md** 읽기: 더 상세한 정보
- **index.html** 주석 읽기: HTML/JS 코드 이해
- **crawler.py** 주석 읽기: 크롤링 로직 이해

---

**축하합니다!** 🎉  
이제 전북판 경북 서식 꾸러미가 완성되었습니다!
