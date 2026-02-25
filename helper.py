import sys
import time
import webbrowser
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

PROFILE_URL = "https://www.acmicpc.net/user/{username}"
SUBMIT_URL = "https://www.acmicpc.net/status?from_mine=1&problem_id={problem_id}&user_id={username}"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    )
}
DELAY_SECONDS = 5
LOG_DIR = Path(__file__).parent / "logs"


def fetch_solved_problems(username: str) -> list[str]:
    url = PROFILE_URL.format(username=username)
    response = requests.get(url, headers=HEADERS, timeout=10)

    if response.status_code != 200:
        print(f"\n[error] 프로필 페이지 접근 실패 (HTTP {response.status_code})")
        print(f"[error] URL: {url}")
        sys.exit(1)

    soup = BeautifulSoup(response.text, "html.parser")
    problem_divs = soup.select("div.problem-list")

    if not problem_divs:
        print("\n[error] 맞은 문제를 찾을 수 없습니다.")
        print("[error] username을 확인하거나, 프로필 공개 설정을 확인해주세요.")
        sys.exit(1)

    problem_list = problem_divs[0].select("a")
    if not problem_list:
        print("\n[error] 맞은 문제를 찾을 수 없습니다.")
        sys.exit(1)

    return [a.text.strip() for a in problem_list]


def get_log_path(username: str) -> Path:
    return LOG_DIR / f"uploaded_{username}.txt"


def load_uploaded(username: str) -> set[str]:
    log_path = get_log_path(username)
    if not log_path.exists():
        return set()
    return set(log_path.read_text().strip().splitlines())


def save_uploaded(username: str, problem_id: str) -> None:
    LOG_DIR.mkdir(exist_ok=True)
    log_path = get_log_path(username)
    with open(log_path, "a") as f:
        f.write(problem_id + "\n")


def open_submission_pages(username: str, problems: list[str]) -> None:
    print(f"\n[helper] 총 {len(problems)}개 문제를 업로드합니다.")
    print(f"[helper] 문제당 {DELAY_SECONDS}초 대기 (BaekjoonHub 업로드 대기)")
    print(f"[helper] 예상 소요 시간: 약 {len(problems) * DELAY_SECONDS // 60}분 {len(problems) * DELAY_SECONDS % 60}초")
    print()

    for problem_id in tqdm(problems, desc="[helper] 업로드 진행", unit="문제"):
        url = SUBMIT_URL.format(problem_id=problem_id, username=username)
        webbrowser.open_new_tab(url)
        save_uploaded(username, problem_id)
        time.sleep(DELAY_SECONDS)

    print("\n[helper] 모든 문제의 제출 페이지를 열었습니다!")
    print("[helper] BaekjoonHub 업로드가 완료될 때까지 브라우저를 닫지 마세요.")


def main() -> None:
    print("=" * 50)
    print("  BOJ Upload Helper (BaekjoonHub 자동 업로드)")
    print("=" * 50)
    print()

    username = input("[helper] username 입력 : ").strip()

    if not username:
        print("[error] username을 입력해주세요.")
        sys.exit(1)

    print(f"\n[helper] '{username}' 프로필에서 맞은 문제 목록을 가져오는 중...")
    all_problems = fetch_solved_problems(username)
    print(f"[helper] 맞은 문제 {len(all_problems)}개를 찾았습니다.")

    uploaded = load_uploaded(username)
    problems = [p for p in all_problems if p not in uploaded]

    if not problems:
        print(f"[helper] 모든 문제가 이미 업로드 완료되었습니다! (로그: {get_log_path(username)})")
        sys.exit(0)

    if uploaded:
        print(f"[helper] 기존 업로드 완료: {len(uploaded)}개 → 남은 문제: {len(problems)}개")
    print(f"[helper] 업로드 대상: {', '.join(problems[:10])}{'...' if len(problems) > 10 else ''}")

    print()
    confirm = input("[helper] 업로드를 시작하시겠습니까? (y/n) : ").strip().lower()
    if confirm != "y":
        print("[helper] 업로드를 취소합니다.")
        sys.exit(0)

    open_submission_pages(username, problems)


if __name__ == "__main__":
    main()
