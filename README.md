# 전북특별자치도교육청 서식 꾸러미

전북교육청의 서식을 한곳에서 검색하고 다운로드할 수 있는 정적 웹사이트입니다.

> 💡 **참고**: 이 프로젝트는 경북교육청의 ["경상북도교육청 서식 꾸러미"](https://kimju1416.github.io/gbe-seosik/)에서 영감을 받았습니다.

---

## 🚀 빠른 시작

### 1단계: GitHub 저장소 만들기

1. GitHub에 로그인하고 새 저장소를 만듭니다.
   - 저장소명: `jbe-seosik` (또는 원하는 이름)
   - Public 선택
   - README 미생성 (이 파일을 사용)

2. 이 폴더의 모든 파일을 저장소에 업로드합니다:
   ```
   jbe-seosik/
   ├── index.html
   ├── forms.json
   ├── crawler.py
   ├── README.md
   └── .github/
       └── workflows/
           └── update.yml (선택사항)
   ```

### 2단계: 데이터 수집하기

#### 옵션 A: 수동으로 forms.json 작성
`forms.json`의 샘플 데이터를 참고하여 직접 서식을 입력합니다.

#### 옵션 B: Python 크롤러 사용 (권장)

1. **크롤러 설정**
   
   `crawler.py`의 `crawl_forms()` 함수에서 수집 대상을 설정합니다:
   
   ```python
   sources = [
       {
           'name': '교무학사업무 길라잡이',
           'url': 'https://수집대상URL',  # ← 실제 게시판 URL 입력
           'category': '교무',
           'selector': 'table tr'  # ← 게시판 구조에 맞게 수정
       },
       # 추가 게시판...
   ]
   ```

2. **수집 대상 찾기**
   
   전북교육청 공식 서식 자료실:
   - 도교육청 홈페이지: https://www.jbe.go.kr/
   - 각 지원청 학교업무지원센터
   - jbwork.oopy.io (이미 정리된 공통양식들)

3. **크롤러 실행**
   
   ```bash
   python3 crawler.py
   ```
   
   또는
   
   ```bash
   python crawler.py
   ```

4. **결과 확인**
   
   `forms.json`이 새로 생성되고 `index.html`에서 확인할 수 있습니다.

### 3단계: GitHub Pages에 배포

1. 저장소 Settings > Pages로 이동
2. **Source** 설정:
   - Branch: `main`
   - Folder: `/ (root)`
3. **Save** 클릭

4. 배포 완료 대기 (보통 1-2분)

5. `https://[YOUR-USERNAME].github.io/jbe-seosik` 에서 사이트 확인

---

## 📚 파일 구조 설명

```
jbe-seosik/
├── index.html          # 메인 웹페이지 (검색, 필터, 미리보기)
├── forms.json          # 서식 데이터 (JSON 형식)
├── crawler.py          # 자동 수집 스크립트
├── README.md           # 이 파일
└── .github/
    └── workflows/
        └── update.yml  # GitHub Actions 자동화 (선택)
```

### forms.json 형식

```json
[
  {
    "id": "001",
    "title": "서식명",
    "category": "교무",           // 주분류
    "subcategory": "계획·보고",   // 소분류
    "date": "2026-07-22",
    "source": "전북특별자치도교육청",
    "download_url": "https://...",
    "description": "서식 설명",
    "file_type": "hwp"            // hwp, xlsx, pdf, docx, etc
  }
]
```

---

## 🎨 커스터마이징

### 색상 변경

`index.html`의 CSS에서 `#1a237e` (네이비 파란색)을 원하는 색상 코드로 변경:

```css
header h1 {
    color: #FF6B6B;  /* 빨간색 예시 */
}
```

### 카테고리 추가/삭제

1. `index.html`의 필터 선택지 추가:
```html
<select id="categoryFilter">
    <option value="">전체</option>
    <option value="교무">교무</option>
    <option value="새카테고리">새카테고리</option>  <!-- 추가 -->
</select>
```

2. `forms.json`에서 해당 category 값 사용

### 로고/헤더 변경

```html
<!-- 현재 -->
<h1>🏫 전북특별자치도교육청 서식 꾸러미</h1>

<!-- 변경 예시 -->
<h1>📋 전북 교육 서식 모음</h1>
```

---

## 🤖 자동 갱신 설정 (GitHub Actions)

매주 자동으로 크롤러를 실행하여 서식을 갱신할 수 있습니다.

`.github/workflows/update.yml` 생성:

```yaml
name: Weekly Forms Update

on:
  schedule:
    - cron: '0 0 * * 0'  # 매주 일요일 자정 (UTC)

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: pip install requests beautifulsoup4
      
      - name: Run crawler
        run: python3 crawler.py
      
      - name: Commit changes
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add -A
          git commit -m "Auto: Update forms database ($(date +'%Y-%m-%d %H:%M:%S'))" || true
          git push
```

---

## ⚠️ 중요 사항

### 데이터 수집 시 주의사항

1. **게시판 HTML 구조 파악**
   - 크롤러가 작동하려면 실제 게시판 HTML 구조를 파악해야 합니다.
   - 각 게시판마다 구조가 다르므로 `crawler.py`의 선택자(selector)를 맞춰야 합니다.
   - 개발자 도구(F12) > Elements 탭에서 확인

2. **핫링크(hotlinking) 확인**
   - 일부 게시판은 외부 사이트에서의 직접 다운로드를 차단할 수 있습니다.
   - 이 경우 `download_url`을 게시글 링크로 변경해야 합니다.

3. **로봇 배제(robots.txt) 존중**
   - 게시판의 robots.txt를 확인하고 존중합니다.
   - 필요시 `User-Agent` 지연을 늘립니다. (crawler.py의 `time.sleep(1)`)

### 법적/윤리적 사항

- ✅ 공개된 공식 문서만 수집합니다.
- ✅ 교육청의 저작권을 명시합니다.
- ❌ 내부 문서나 개인정보는 수집하지 않습니다.
- ❌ 과도한 트래픽으로 서버에 부하를 주지 않습니다.

---

## 🔧 문제 해결

### Q: "forms.json을 불러올 수 없습니다" 오류

**A:** 
1. `forms.json` 파일이 저장소에 있는지 확인
2. 경로가 `index.html`과 같은 폴더인지 확인
3. GitHub Pages가 활성화되었는지 확인 (Settings > Pages)

### Q: 크롤러가 서식을 수집하지 못함

**A:**
1. `crawler.py`의 URL이 정확한지 확인
2. 선택자(selector)를 실제 게시판 구조에 맞게 수정
3. 콘솔 출력(로그)를 확인하여 오류 메시지 확인

```bash
python3 crawler.py  # 상세한 로그 출력
```

### Q: 파일이 다운로드되지 않음

**A:**
1. `download_url`이 올바른지 확인
2. 핫링크가 차단되었는지 확인
3. 대신 게시글 링크(view 페이지)로 변경

---

## 📊 통계

현재 포함된 서식:
- 총 서식 개수: (자동 계산)
- 주분류: 교무, 담임, 학사, 보건, 안전, 정보 등
- 파일형식: HWP, XLSX, PDF 등

---

## 📧 피드백 및 기여

### 서식 추가 요청
1. 이슈(Issue) 작성: "추가 요청: [서식명]"
2. 또는 직접 `forms.json`에 추가 후 PR 생성

### 개선 사항 제안
- 검색 기능 개선
- UI/UX 개선
- 자동화 스크립트 최적화

---

## 📜 라이선스 및 저작권

> ⚠️ **중요**: 이 사이트는 **전북특별자치도교육청의 공식 사이트가 아닙니다**. 
> 모든 서식의 저작권은 전북특별자치도교육청에 있습니다.

이 저장소는 공개된 교육청 서식에 대한 접근성을 높이기 위한 비영리 프로젝트입니다.

---

## 🙏 감사의 말

- [경상북도교육청 서식 꾸러미](https://kimju1416.github.io/gbe-seosik/)에서 영감
- jbwork.oopy.io의 전북 공통양식 자료

---

**마지막 업데이트:** 2026-07-26  
**유지보수:** 전북 교육 커뮤니티
