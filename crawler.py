#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
전북특별자치도교육청 서식 꾸러미 자동 수집 스크립트
- 지정된 게시판의 서식 목록을 자동으로 수집합니다.
- forms.json 파일로 저장됩니다.

사용방법:
1. 대상 게시판 URL을 설정합니다.
2. python3 crawler.py 를 실행합니다.
"""

import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FormCrawler:
    def __init__(self):
        self.forms = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def crawl_forms(self):
        """
        전북교육청 게시판에서 서식을 수집합니다.
        
        주요 수집 대상:
        - 도교육청 부서별 자료실
        - 각 지원청 학교업무지원센터
        """
        
        # 📝 수집 대상 설정
        # 실제로는 각 게시판의 URL을 여기에 입력합니다.
        sources = [
            {
                'name': '도교육청 교무학사업무 길라잡이',
                'url': 'https://www.jbe.go.kr/',  # 예시
                'category': '교무',
                'selector': 'article'  # 게시글 선택자
            },
            # 추가 게시판들...
        ]
        
        for source in sources:
            logger.info(f"수집 시작: {source['name']}")
            self.crawl_board(source)
            time.sleep(1)  # 서버 부하 방지
        
        logger.info(f"총 {len(self.forms)}개의 서식 수집 완료")
    
    def crawl_board(self, source):
        """특정 게시판에서 서식을 수집합니다."""
        try:
            response = self.session.get(source['url'], timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code != 200:
                logger.warning(f"접근 실패 ({response.status_code}): {source['url']}")
                return
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # ⚠️ 주의: 아래는 예시입니다. 실제 게시판 구조에 맞게 수정해야 합니다.
            # 게시판마다 HTML 구조가 다르므로, 개발자 도구를 열어 선택자를 확인하세요.
            
            # 예시: 표 형식 게시판
            rows = soup.find_all('tr')[1:]  # 헤더 제외
            
            for row in rows[:20]:  # 최근 20개만
                cols = row.find_all('td')
                if len(cols) < 3:
                    continue
                
                title = cols[0].get_text(strip=True)
                date_str = cols[-1].get_text(strip=True)
                link = cols[0].find('a')
                
                if not link:
                    continue
                
                form_url = link.get('href', '')
                
                # 상대 경로를 절대 경로로 변환
                if not form_url.startswith('http'):
                    form_url = source['url'].split('/index')[0] + form_url
                
                form = self.create_form_object(
                    title=title,
                    category=source['category'],
                    url=form_url,
                    date=date_str
                )
                
                if form:
                    self.forms.append(form)
                    logger.debug(f"  추가: {title}")
        
        except Exception as e:
            logger.error(f"크롤링 오류 ({source['url']}): {str(e)}")
    
    def create_form_object(self, title, category, url, date):
        """서식 객체를 생성합니다."""
        if not title or not url:
            return None
        
        # 파일 형식 자동 감지
        file_type = self.detect_file_type(url)
        
        # 소분류 결정 (제목에서 추론)
        subcategory = self.infer_subcategory(title, category)
        
        # 중복 확인
        if any(f['title'] == title and f['category'] == category for f in self.forms):
            return None
        
        return {
            'id': f"{len(self.forms)+1:03d}",
            'title': title,
            'category': category,
            'subcategory': subcategory,
            'date': self.normalize_date(date),
            'source': '전북특별자치도교육청',
            'download_url': url,
            'description': f"{category} 업무에 활용할 수 있는 서식입니다.",
            'file_type': file_type
        }
    
    def detect_file_type(self, url):
        """URL에서 파일 형식을 감지합니다."""
        url_lower = url.lower()
        if url_lower.endswith('.hwp') or '.hwp' in url_lower:
            return 'hwp'
        elif url_lower.endswith('.xlsx') or url_lower.endswith('.xls') or '.xlsx' in url_lower:
            return 'xlsx'
        elif url_lower.endswith('.pdf') or '.pdf' in url_lower:
            return 'pdf'
        elif url_lower.endswith('.docx') or '.docx' in url_lower:
            return 'docx'
        else:
            return 'etc'
    
    def infer_subcategory(self, title, category):
        """제목에서 소분류를 추론합니다."""
        title_lower = title.lower()
        
        subcategories = {
            '계획': ['계획', '안내', '길라잡이'],
            '양식': ['양식', '서식', '서식지'],
            '보고': ['보고', '보고서', '현황'],
            '학생관리': ['학생', '명부', '명단'],
            '상담': ['상담', '의뢰'],
            '건강관리': ['건강', '검사'],
            '생활지도': ['폭력', '지도', '약물'],
            '교육과정': ['교육과정', '평가'],
            '소통': ['가정통신', '알림'],
        }
        
        for sub, keywords in subcategories.items():
            if any(kw in title_lower for kw in keywords):
                return sub
        
        return category
    
    def normalize_date(self, date_str):
        """날짜 형식을 표준화합니다."""
        # 예: "2026-07-22" 또는 "26.07.22"
        if not date_str:
            return datetime.now().strftime('%Y-%m-%d')
        
        # 다양한 날짜 형식 처리
        formats = ['%Y-%m-%d', '%y.%m.%d', '%Y.%m.%d', '%d-%m-%Y']
        for fmt in formats:
            try:
                date_obj = datetime.strptime(date_str.strip(), fmt)
                return date_obj.strftime('%Y-%m-%d')
            except:
                continue
        
        return datetime.now().strftime('%Y-%m-%d')
    
    def save_to_json(self, filename='forms.json'):
        """수집한 서식을 JSON으로 저장합니다."""
        try:
            # ID 재정의
            for i, form in enumerate(self.forms, 1):
                form['id'] = f"{i:03d}"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.forms, f, ensure_ascii=False, indent=2)
            
            logger.info(f"✓ {filename}에 {len(self.forms)}개 항목 저장 완료")
            return True
        
        except Exception as e:
            logger.error(f"JSON 저장 오류: {str(e)}")
            return False
    
    def print_summary(self):
        """수집 결과 요약을 출력합니다."""
        print("\n" + "="*60)
        print("📊 수집 결과 요약")
        print("="*60)
        print(f"총 서식 개수: {len(self.forms)}개\n")
        
        # 분류별 통계
        categories = {}
        for form in self.forms:
            cat = form['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        print("분류별 개수:")
        for cat, count in sorted(categories.items()):
            print(f"  {cat}: {count}개")
        
        # 파일형식별 통계
        print("\n파일형식별 개수:")
        file_types = {}
        for form in self.forms:
            ft = form['file_type']
            file_types[ft] = file_types.get(ft, 0) + 1
        
        for ft, count in sorted(file_types.items()):
            print(f"  {ft}: {count}개")
        
        print("\n" + "="*60)

def main():
    print("""
╔════════════════════════════════════════════════════════════╗
║  전북특별자치도교육청 서식 꾸러미 자동 수집 스크립트        ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    crawler = FormCrawler()
    
    # 🚀 수집 시작
    print("📥 서식 수집을 시작합니다...\n")
    crawler.crawl_forms()
    
    # 💾 저장
    if crawler.save_to_json():
        crawler.print_summary()
        print("\n✅ 완료! index.html을 열어 확인하세요.")
    else:
        print("\n❌ 저장 중 오류가 발생했습니다.")

if __name__ == '__main__':
    main()
