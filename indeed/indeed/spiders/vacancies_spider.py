from urllib.parse import urlencode
import json

import scrapy
from bs4 import BeautifulSoup


class IndeedVacanciesSpider(scrapy.Spider):
    name = "indeed_vacancies"

    def build_search_url(
        self, country: str, keyword: list, location: list, page: int = 0
    ) -> str:
        parameters = {"q": keyword, "l": location, "start": page}
        return f"https://{country}.indeed.com/jobs?" + urlencode(parameters)

    def start_requests(self):
        # This parameters will request from user
        country = "uk"
        keyword_list = ["python data engineer"]
        location_list = ["london"]
        for keyword in keyword_list:
            for location in location_list:
                url = self.build_search_url(country, keyword, location)
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_search_results,
                    meta={
                        "country": country,
                        "keyword": keyword,
                        "location": location,
                    },
                )

    def parse_search_results(self, response):
        re_pattern = (
            r'window.mosaic.providerData\["mosaic-provider-jobcards"\]=(\{.+?\});'
        )
        xpath_pattern = '//script[@id="mosaic-data"]/text()'

        country = response.meta["country"]
        keyword = response.meta["keyword"]
        location = response.meta["location"]
        script = response.xpath(xpath_pattern).re(re_pattern)
        json_search_result = json.loads(script[0])
        jobs = json_search_result["metaData"]["mosaicProviderJobCardsModel"]["results"]

        for job in jobs:
            job_key = job["jobkey"]
            job_url = f"https://{country}.indeed.com/viewjob?jk=" + job_key

            print(job_key, job_url)
