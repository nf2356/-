import requests
from bs4 import BeautifulSoup
import pandas as pd

def html_table_to_df(table_rows):
    data = []
    for row in table_rows:
        cols = row.find_all(['th', 'td'])
        cols = [ele.text.strip() for ele in cols]
        data.append([ele for ele in cols if ele]) 
    df = pd.DataFrame(data[1:], columns=data[0])

    return df

def main():
    # 웹 페이지의 URL
    url = 'https://m.seibro.or.kr/cnts/company/selectDiv50.do'

    # 페이지의 HTML 가져오기
    response = requests.get(url)

    # 성공적인 응답을 받았는지 확인
    if response.status_code == 200:
        # HTML 파싱
        soup = BeautifulSoup(response.text, 'html.parser')

        # 테이블 데이터 찾기
        table = soup.find('table')

        # 모든 행 데이터 찾기
        rows = table.find_all('tr')

        # 판다스 데이터프레임으로 변환
        df = html_table_to_df(rows)

        # 상위 50행만 선택
        top20 = df.head(50)

        # 데이터를 엑셀 파일로 저장
        top20.to_excel('배당금순위.xlsx', index=False)

    else:
        print(f'Failed to retrieve page. Status code: {response.status_code}')

if __name__ == "__main__":
    main()