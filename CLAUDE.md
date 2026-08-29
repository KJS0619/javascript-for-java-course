# JavaScript for Java Course - 프로젝트 가이드

## 프로젝트 개요
자바 개발자를 위한 JavaScript 입문서 (부크크 POD 출판용)

## 대상 독자
- Java/Spring 백엔드 개발자
- JavaScript를 처음 배우거나 체계적으로 정리하고 싶은 분
- React/Vue/Node.js를 배우기 전 기초를 다지고 싶은 분

## 디렉토리 구조
```
javascript-for-java-course/
├── book/
│   ├── chapter0.html ~ chapter9.html  # 챕터별 HTML
│   ├── index.html                      # 목차 페이지
│   ├── cover/                          # 표지
│   │   ├── cover.html
│   │   └── fonts/
│   ├── pdf-src/                        # PDF 생성
│   │   ├── build.py
│   │   └── fonts/
│   └── javascript-book.pdf
├── CLAUDE.md
└── README.md
```

## 부크크 규격
- **판형**: 46배판 (188mm × 263mm)
- **도련**: 3mm
- **풀커버**: (191 + 책등 + 191) × 269mm

## 책등 두께 계산
```
책등(mm) = 페이지 수 × 0.0534 (80g 용지 기준)
```

## 목차 구조

### 0장. 오리엔테이션
- 이 책의 대상과 목표
- Java 개발자가 JavaScript를 배울 때 유의점
- 학습 환경 설정

### 1장. JavaScript 첫걸음
- JavaScript란?
- Java와의 근본적 차이
- 브라우저 콘솔에서 실행해보기
- Node.js 환경 소개

### 2장. 변수와 타입
- var, let, const의 차이
- 동적 타입 vs 정적 타입
- 원시 타입과 참조 타입
- typeof와 타입 확인
- Java 개발자가 주의할 점

### 3장. 함수의 모든 것
- 함수 선언 vs 함수 표현식
- 화살표 함수 (Arrow Function)
- 함수는 일급 객체
- 클로저 (Closure) 이해
- Java의 메서드 vs JavaScript의 함수

### 4장. 객체와 배열
- 객체 리터럴
- 프로토타입과 상속
- 배열과 고차 함수 (map, filter, reduce)
- 구조 분해 할당
- 스프레드 연산자

### 5장. 클래스와 모듈
- ES6 클래스 문법
- 상속과 super
- 모듈 시스템 (import/export)
- Java 클래스와의 비교

### 6장. 비동기 프로그래밍
- 콜백과 콜백 지옥
- Promise 이해와 활용
- async/await 패턴
- 에러 처리
- Java의 CompletableFuture와 비교

### 7장. DOM과 이벤트
- DOM 구조 이해
- 요소 선택과 조작
- 이벤트 리스너
- 이벤트 버블링과 캡처링
- 실습: 간단한 TODO 앱

### 8장. 모던 JavaScript 생태계
- npm과 패키지 관리
- 번들러 (Webpack, Vite)
- 트랜스파일러 (Babel)
- TypeScript 소개
- 프론트엔드 프레임워크 로드맵

### 9장. 실전 프로젝트
- Spring Boot API와 연동
- Fetch API로 HTTP 요청
- CORS 이해
- 간단한 SPA 구현
- 다음 학습 로드맵

## 스타일 가이드

### 코드 비교 형식
```html
<div class="compare">
  <div class="java">
    <h4>Java</h4>
    <pre>// Java 코드</pre>
  </div>
  <div class="js">
    <h4>JavaScript</h4>
    <pre>// JavaScript 코드</pre>
  </div>
</div>
```

### 핵심 포인트 박스
```html
<aside class="keypoint">
  <strong>Java 개발자 포인트</strong>
  <p>설명...</p>
</aside>
```

### 색상 테마
- 배경: #EEF0EA (paper)
- 글자: #201F1B (ink)
- 강조: #D4A017 (JavaScript 노란색)
- 코드 배경: #1C2229

## 작업 이력

### 2026-08-29 프로젝트 생성
- 디렉토리 구조 생성
- CLAUDE.md 작성
- 목차 설계
