import logging
from typing import ClassVar
from urllib.parse import quote, urlencode

from seleniumwire.request import Request, Response

from haystack.search.models import Search, SearchSource
from haystack.search.parsers.base import BaseParser

logger = logging.getLogger(__name__)


class LinkedInParser(BaseParser):
    """Search LinkedIn for jobs."""

    JOBS_PER_PAGE = 10

    MAX_JOB_COUNT = 1000

    blocklist: ClassVar[list[str]] = []

    name = 'linkedin'

    def intercept_request(self, request: Request) -> None:
        """Abort authwall requests."""
        super().intercept_request(request)
        if request.host == 'www.linkedin.com' and request.path.strip('/') in ['', 'authwall', 'favicon.ico']:
            request.abort(error_code=404)

    def process_response(self, requests: list[Request]) -> Response | None:
        """Return most recent request to access jobs url."""
        for request in reversed(requests):
            if request.url.startswith('https://www.linkedin.com/jobs') and (response := request.response) is not None:
                return response
        return None

    def get_linkedin_url(self, endpoint: str, search: Search, page: int = 1) -> str:
        """Return LinkedIn search url."""
        params = {
            'keywords': quote(search.keywords),
            'geo_id': search.geo_id,
        }

        if search.easy_apply:
            params['f_AL'] = 'true'

        wt = [
            str(code)
            for value, code in [
                (search.is_onsite, 1),
                (search.is_remote, 2),
                (search.is_hybrid, 3),
            ]
            if value
        ]
        if wt:
            params['f_WT'] = quote(','.join(wt))

        if page > 1:
            params['start'] = self.JOBS_PER_PAGE * (page - 1)

        return f'https://linkedin.com{endpoint}search?{urlencode(params)}'

    def get_job_count(self, search: Search) -> int:
        """Return number of jobs found."""
        url = self.get_linkedin_url('/jobs/', search)
        response = self.firefox.get_with_retry(url)
        if response is None:
            logger.error('Unable to retrieve job count')
            return 0

        soup = self.firefox.soupify()
        try:
            tag = soup.find('span', {'class': 'results-context-header__job-count'})
            if tag is None:
                logger.error('`results-context-header__job-count` not found')
                return 0
            count = tag.get_text(strip=True)
            return min(int(''.join(filter(str.isdigit, count))), self.MAX_JOB_COUNT)
        except Exception:
            logger.exception('Error parsing job count')
            return 0

    def get_page_count(self, search: Search) -> int:
        """Return number of pages to search."""
        count = self.get_job_count(search)
        if count == 0:
            logger.info('Setting page count to 1')
            return 1
        return (count // self.JOBS_PER_PAGE) + 1

    def parse(self, search_source: SearchSource) -> str:
        """Parse jobs."""
        return self.get_linkedin_url('/jobs-guest/jobs/api/seeMoreJobPostings/', search_source.search)
