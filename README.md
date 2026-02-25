# BOJ Upload Helper

백준(BOJ)에서 풀었던 문제들을 **BaekjoonHub** 크롬 익스텐션을 통해 GitHub에 자동으로 업로드하는 헬퍼 프로그램입니다.

백준 프로필에서 "맞은 문제" 목록을 자동으로 가져와, 각 문제의 제출 페이지를 브라우저에서 순차적으로 열어줍니다.  
BaekjoonHub 익스텐션이 각 제출 페이지에서 자동으로 GitHub 커밋을 수행합니다.

### Reference
https://velog.io/@yoondgu/%ED%8C%8C%EC%9D%B4%EC%8D%AC%EC%9D%84-%EC%9D%B4%EC%9A%A9%ED%95%B4-%EA%B7%B8%EB%8F%99%EC%95%88-%EC%A0%9C%EC%B6%9C%ED%95%9C-%EB%AC%B8%EC%A0%9C-%EB%AA%A8%EB%91%90-%EB%B0%B1%EC%A4%80%ED%97%88%EB%B8%8C-%EC%97%85%EB%A1%9C%EB%93%9C%ED%95%98%EA%B8%B0

## 사전 준비

### 1. BaekjoonHub 크롬 익스텐션 설치 및 연동

1. [BaekjoonHub 크롬 익스텐션](https://chrome.google.com/webstore/detail/baekjoonhub/ccammcjdkpgjmcpijpahlehmapgmphmk)을 설치합니다.
2. GitHub 계정으로 로그인하고, 업로드할 Repository를 연동합니다.

### 2. 레포지토리 클론

```bash
git clone https://github.com/<your-username>/BOJ_Upload_Helper.git
cd BOJ_Upload_Helper
```

### 3. Python 환경 및 uv 설치

- Python 3.13 이상이 필요합니다.
- [uv](https://docs.astral.sh/uv/) 패키지 매니저를 설치합니다:

```bash
# macOS (Homebrew)
brew install uv

# 또는 공식 설치 스크립트
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 4. 의존성 설치

```bash
uv sync
```

## 사용법

```bash
uv run helper.py
```

실행하면 아래와 같은 흐름으로 동작합니다:

```
==================================================
  BOJ Upload Helper (BaekjoonHub 자동 업로드)
==================================================

[helper] username 입력 : ikjoon0812

[helper] 'ikjoon0812' 프로필에서 맞은 문제 목록을 가져오는 중...
[helper] 맞은 문제 272개를 찾았습니다.
[helper] 업로드 대상: 1000, 1001, 1003, ...

[helper] 업로드를 시작하시겠습니까? (y/n) : y

[helper] 총 272개 문제를 업로드합니다.
[helper] 문제당 5초 대기 (BaekjoonHub 업로드 대기)
[helper] 예상 소요 시간: 약 12분 34초

[helper] 업로드 진행: 100%|██████████████████████| 272/272 [03:30<00:00, 5.00s/문제]

[helper] 모든 문제의 제출 페이지를 열었습니다!
[helper] BaekjoonHub 업로드가 완료될 때까지 브라우저를 닫지 마세요.
```

## 업로드 재개 (Resume)

프로그램은 업로드가 완료된 문제를 `logs/uploaded_{username}.txt`에 자동으로 기록합니다.  
중간에 종료되거나 일부 문제가 누락된 경우, **그냥 다시 실행**하면 이미 완료된 문제는 자동으로 스킵하고 남은 문제만 이어서 업로드합니다.

```
[helper] 기존 업로드 완료: 220개 → 남은 문제: 52개
```

로그를 초기화하고 처음부터 다시 업로드하려면 아래 파일을 삭제하세요:

```bash
rm logs/uploaded_{username}.txt
```

## 주의사항

- **Chrome 브라우저**가 기본 브라우저로 설정되어 있어야 합니다.
- BaekjoonHub 익스텐션이 **활성화**된 상태여야 합니다.
- 업로드 중 브라우저를 닫지 마세요.
- **프로그램 실행 중에는 다른 작업을 하지 않는 것을 권장합니다.** 탭 전환이나 다른 앱 사용 시 브라우저가 백그라운드로 전환되어 BaekjoonHub가 페이지를 정상적으로 처리하지 못할 수 있습니다.
- 문제당 5초의 딜레이가 있으므로, 문제가 많을 경우 시간이 오래 걸릴 수 있습니다.

## 개발 도구

이 프로젝트는 **[GitHub Copilot CLI](https://githubnext.com/projects/copilot-cli/)** + **Claude Opus 4.6** 모델을 사용하여 설계 및 개발되었습니다.

초기 설계에 사용된 프롬프트는 [`plan_prompt.txt`](./plan_prompt.txt)에서 확인할 수 있습니다.