from urllib.parse import urlencode

import scrapy


class IndeedVacanciesSpider(scrapy.Spider):
    name = "indeed_vacancies"

    def build_search_url(
        self, country: str, keyword: list, location: list, page: int = 0
    ) -> str:
        parameters = {"q": keyword, "l": location, "start": page}
        return f"https://{country}.indeed.com/jobs?" + urlencode(parameters)

    def start_requests(self):
        # This parameters will request from user
        country = "gb"
        keyword_list = ["data", "engineer"]
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
        print(response.meta)
