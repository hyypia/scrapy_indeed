from urllib.parse import urlencode
import json
from pprint import pprint

import scrapy
from bs4 import BeautifulSoup


class IndeedVacanciesSpider(scrapy.Spider):
    name = "indeed_vacancies"

    def build_search_url(
        self, country: str, keyword: list, location: list, offset: int = 0
    ) -> str:
        parameters = {"q": keyword, "l": location, "start": offset}
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
                        "offset": 0,
                    },
                )

    def parse_search_results(self, response):
        xpath_script_pattern = '//script[@id="mosaic-data"]/text()'
        re_script_pattern = (
            r'window.mosaic.providerData\["mosaic-provider-jobcards"\]=(\{.+?\});'
        )
        xpath_jobs_count_pattern = '//div[@class="jobsearch-JobCountAndSortPane-jobCount css-1af0d6o eu4oa1w0"]/span/text()'

        jobs_total_count = int(response.xpath(xpath_jobs_count_pattern).re(r"\d+")[0])

        country = response.meta["country"]
        keyword = response.meta["keyword"]
        location = response.meta["location"]
        offset = response.meta["offset"]

        script = response.xpath(xpath_script_pattern).re(re_script_pattern)
        json_search_result = json.loads(script[0])
        jobs = json_search_result["metaData"]["mosaicProviderJobCardsModel"]["results"]

        # for job in jobs:
        #     job_key = job["jobkey"]
        #     job_url = f"https://{country}.indeed.com/viewjob?jk=" + job_key
        #     yield scrapy.Request(
        #         url=job_url,
        #         callback=self.parse_job,
        #         meta={
        #             "country": country,
        #             "keyword": keyword,
        #             "location": location,
        #         },
        #     )

        if offset == 0:
            pages_count = round(jobs_total_count / 15) * 10

            for offset in range(10, pages_count + 10, 10):
                url = self.build_search_url(country, keyword, location, offset)
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_search_results,
                    meta={
                        "country": country,
                        "keyword": keyword,
                        "location": location,
                        "offset": offset,
                    },
                )

    def parse_job(self, response):
        pass
