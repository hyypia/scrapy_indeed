from pprint import pprint
import requests


res = requests.get(
    "https://www.glassdoor.com/Job/berlin-germany-data-engineer-jobs-SRCH_IL.0,14_IC2622109_KO15,28.htm",
    headers={
        "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0"
    },
)
pprint(res.status_code)
