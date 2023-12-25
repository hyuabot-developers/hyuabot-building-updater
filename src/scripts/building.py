import asyncio

import aiohttp

BASE_URL = "https://m.blog.naver.com/api/blogs/hyerica4473/search/post"
search_keyword = "%EA%B1%B4%EB%AC%BC%20%EB%82%B4%EB%B6%80%20%EA%B5%AC%EC%A1%B0%EB%8F%84"


async def fetch_building_list() -> list[dict]:
    pages = [1, 2, 3, 4]
    urls = [f"{BASE_URL}?query={search_keyword}&page={page}" for page in pages]
    header = {"Referer": "https://m.blog.naver.com/PostSearchList.naver?blogId=hyerica4473&orderType=sim&searchText="}
    async with aiohttp.ClientSession(headers=header) as session:
        tasks = []
        for url in urls:
            tasks.append(asyncio.create_task(fetch_building_page(session, url)))
        values = await asyncio.gather(*tasks)
    building_list = []
    for value in values:
        building_list.extend(filter(lambda x: "건물 내부 구조도" in x.get("title"), value))

    results = []
    for building in building_list:
        title = str(building.get("title"))\
            .replace("[자료실] ", "")\
            .replace('<em class="highlight">건물 내부 구조도</em>', "").strip()
        post_no = building.get("logNo")
        results.append({"title": title, "link": f"https://m.blog.naver.com/hyerica4473/{post_no}"})
    return results


async def fetch_building_page(session, url) -> list[dict]:
    async with session.get(url) as response:
        response_json = await response.json()
        return response_json.get("result").get("list")
