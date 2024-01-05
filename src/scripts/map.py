import aiohttp
from bs4 import BeautifulSoup


async def fetch_campus() -> list[dict]:
    async with aiohttp.ClientSession() as session:
        async with session.get("https://m.blog.naver.com/hyerica4473/222530157495") as response:
            response_text = await response.text()
            soup = BeautifulSoup(response_text, "html.parser")
            buildings = soup.select("div > div > div > table > tbody > tr > td")
            raw_data = []
            for building in buildings:
                data = building.text.strip()
                if data and data != "\u200b":
                    raw_data.append(data)
    building_list = []
    for index in range(0, len(raw_data) - 1, 2):
        if raw_data[index].isdigit():
            name = raw_data[index + 1]\
                .replace("Lion's Hall", "라이언스홀")\
                .replace("창의관", "창의인재관")\
                .replace("창의인재 교육관", "교육관")\
                .replace("학술정보관(커리어개발센터)", "학술정보관")\
                .replace("실용음악관(Muse Hall)", "뮤즈홀(실용음악관)")\
                .replace("한양맞춤의약연구원", "맞춤의약연구원(HY-IPT)")
            building_list.append({"id": raw_data[index], "name": name})
    return building_list
