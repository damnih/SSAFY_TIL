from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from .models import StockData

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--blink-settings=imagesEnabled=false")  # D
chrome_options.add_argument("--window-size=800,600")

service = Service(
    ChromeDriverManager().install()
)  # ChromeDriver 자동 다운로드


client = OpenAI(api_key=settings.OPENAI_API_KEY)


def ask_comment(prompt, model="gpt-4o-mini"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"오류 발생: {e}"


def get_stock_code_and_name(driver, company_name):
    """Selenium을 사용하여 Toss Invest 사이트에서 종목 코드와 이름을 가져옵니다."""
    try:
        # Toss Invest 메인 페이지 열기
        driver.get('https://tossinvest.com/')

        # 검색 버튼 클릭
        search_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'u09klc0'))
        )
        ActionChains(driver).click(search_button).perform()

        # 검색 입력
        search_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, '_1x1gpvi6'))
        )
        search_input.clear()
        search_input.send_keys(company_name)
        search_input.send_keys(Keys.RETURN)

        # 검색 결과 대기 후 클릭
        first_result = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'u09klc0'))
        )
        ActionChains(driver).click(first_result).perform()

        # 종목 코드 및 이름 가져오기
        stock_name_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    '//*[@id="__next"]/div[1]/div[1]/main/div/div/div/div[3]/div/div[3]/div[1]/span[1]',
                )
            )
        )
        stock_code = driver.current_url.split('/order')[0][-6:]
        name = stock_name_element.text.strip()

        return stock_code, name
    except Exception as e:
        raise e


def scrape_comments(driver):
    """Selenium을 사용하여 Toss Invest 커뮤니티에서 댓글을 스크래핑."""
    try:
        driver.get(driver.current_url.split('/order')[0] + '/community')

        comment_container = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, 'article > div > a > span')
            )
        )
        filtered_comments = []
        exclude_phrases = ["더보기", "더 보기", "더 보 기"]

        for comment in comment_container:
            comment_text = comment.text.strip()
            normalized_text = comment_text.replace(" ", "")

            if normalized_text and all(
                exclude not in normalized_text for exclude in exclude_phrases
            ):
                filtered_comments.append(comment_text)

        return filtered_comments
    except Exception as e:
        raise e


def scrape_company_data(driver):
    """Selenium을 사용하여 Toss Invest에서 종목 코드, 이름, 댓글을 가져옵니다."""
    try:
        # Chrome WebDriver 초기화
        # driver = webdriver.Chrome(service=service, )

        # 종목 코드 및 이름 가져오기
        # stock_code, stock_name = get_stock_code_and_name(company_name)

        # 댓글 스크래핑
        comments = scrape_comments(driver)

        # WebDriver 종료
        driver.quit()

        return comments
    except Exception as e:
        if 'driver' in locals():
            driver.quit()
        raise e


def analyze_comments(comments, company_name):
    """
    댓글을 분석하여 ChatGPT 응답 반환
    """
    if comments:
        combined_comments = "\n".join(comments)
        prompt = f"다음은 {company_name}에 대한 댓글들입니다. 종합적인 분석을 한글로 작성하고, 마지막 줄에는 여론을 긍정적, 부정적, 중립으로 판단해 주세요:\n{combined_comments}"
        return ask_comment(prompt)
    return "댓글을 찾을 수 없습니다."


def stock_finder(request):
    driver = None  # WebDriver 초기화
    if request.method == "POST":
        # 사용자 입력 받기
        company_name = request.POST.get('company_name', '').strip().lower()
        loading_step = request.POST.get('loading_step', '')

        if not company_name:
            return render(
                request,
                'contentfetch/stock_finder.html',
                {'error_message': "회사 이름을 입력하세요."},
            )

        try:
            # 1. DB에서 `company_name`으로 부분 검색 (부분 일치 허용)
            existing_data = StockData.objects.filter(
                company_name__icontains=company_name
            ).first()
            if existing_data:
                print(f"DB에서 기존 데이터 찾음: {existing_data.company_name}")
                return render(
                    request,
                    'contentfetch/stock_finder.html',
                    {
                        'company_name': existing_data.company_name,
                        'stock_code': existing_data.stock_code,
                        'comments': existing_data.comments.split("\n"),
                        'chatgpt_response': existing_data.analysis,
                        'is_existing_data': True,
                        'is_loading': False,
                    },
                )

            # 2. DB에 없을 경우 Selenium 작업
            if not loading_step:  # 첫 번째 단계
                print("첫 번째 단계: Selenium 로딩 화면 표시")
                return render(
                    request,
                    'contentfetch/stock_finder.html',
                    {
                        'is_loading': True,
                        'loading_step': 'selenium',
                        'company_name': company_name,
                        'form_data': {
                            'company_name': company_name,
                            'loading_step': 'selenium',
                        },
                    },
                )

            # 3. Selenium으로 종목 코드 및 데이터 가져오기
            driver = webdriver.Chrome(service=service, options=chrome_options)
            stock_code, company_name = get_stock_code_and_name(
                driver, company_name
            )
            comments = scrape_company_data(driver)
            print(f"스크래핑 완료: {len(comments)}개 댓글 수집")

            print("ChatGPT 분석 시작")
            chatgpt_response = analyze_comments(comments, company_name)
            print("ChatGPT 분석 완료")

            # 6. DB에 저장
            print("DB 저장 시작")
            stock_data = StockData(
                company_name=company_name,
                stock_code=stock_code,
                comments="\n".join(comments),
                analysis=chatgpt_response,
            )
            stock_data.save()
            print("DB 저장 완료")

            # 7. 최종 결과 반환
            print("최종 결과 반환")
            return render(
                request,
                'contentfetch/stock_finder.html',
                {
                    'company_name': company_name,
                    'stock_code': stock_code,
                    'comments': comments,
                    'chatgpt_response': chatgpt_response,
                    'is_existing_data': False,
                    'is_loading': False,
                },
            )

        except Exception as e:
            print(f"오류 발생: {e}")
            return render(
                request,
                'contentfetch/stock_finder.html',
                {
                    'error_message': f"스크래핑 중 오류 발생: {e}",
                    'is_loading': False,
                },
            )
        finally:
            if driver:
                driver.quit()

    # GET 요청 또는 초기 로드
    return render(
        request, 'contentfetch/stock_finder.html', {'is_loading': False}
    )


@csrf_exempt
def delete_comment(request):
    if request.method == "POST":
        stock_code = request.POST.get('stock_code')
        comment_index = request.POST.get('comment_index')

        if stock_code and comment_index is not None:
            try:
                comment_index = int(comment_index)
                stock_data = StockData.objects.get(stock_code=stock_code)

                if stock_data:
                    comments = stock_data.comments.split("\n")
                    if 0 <= comment_index < len(comments):
                        # 댓글 삭제
                        del comments[comment_index]
                        stock_data.comments = "\n".join(comments)

                        # ChatGPT 응답 재분석
                        chatgpt_response = analyze_comments(
                            comments, stock_data.company_name
                        )
                        stock_data.analysis = chatgpt_response
                        stock_data.save()

                        # 삭제 후 페이지 새로고침
                        return render(
                            request,
                            'contentfetch/stock_finder.html',
                            {
                                'company_name': stock_data.company_name,
                                'stock_code': stock_data.stock_code,
                                'comments': comments,
                                'chatgpt_response': chatgpt_response,
                            },
                        )
            except ValueError:
                pass

        return render(
            request,
            'contentfetch/stock_finder.html',
            {
                'error_message': "댓글 삭제 중 오류가 발생했습니다.",
                'is_loading': False,
            },
        )

    return render(
        request,
        'contentfetch/stock_finder.html',
        {
            'is_loading': False,
        },
    )
