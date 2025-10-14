import logging
from typing import ClassVar
from urllib.parse import quote, urlencode

from django.utils import timezone
from seleniumwire.request import Request, Response

from haystack.jobs.models import Job
from haystack.search.models import Search, SearchSource, Status
from haystack.search.parsers.base import BaseParser
from haystack.search.utils import NullableTag, remove_query

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

    def get_linkedin_url(self, endpoint: str, search: Search, page: int = 1, period: int | None = None) -> str:
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

        if period is not None:
            params['f_TPR'] = f'r{period}'

        # set distance parameter to 25 if location contains a comma with
        # the assumption that names with commas represent cities in states
        if ',' in getattr(search.location, 'name', ''):
            params['distance'] = 25

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

    def parse_job(self, div: NullableTag) -> dict | None:
        """Parse job div."""
        error: str | None = None
        job = {}

        try:
            company_link = div.find('h4', {'class': 'base-search-card__subtitle'}).find('a')
            job['company'] = company_link.text()
            url = company_link.get('href')
            job['company_url'] = remove_query(url)
        except Exception:
            logger.exception('Error parsing company information')
            error = 'company'

        try:
            job['title'] = div.find('h3', {'class': 'base-search-card__title'}).text()
        except Exception:
            logger.exception('Error parsing job title')
            error = 'title'

        try:
            url = div.find('a', {'class': 'base-card__full-link'}).get('href')
            job['url'] = remove_query(url)
        except Exception:
            logger.exception('Error parsing job url')
            error = 'url'

        try:
            job['location'] = div.find('span', {'class': 'job-search-card__location'}).text()
        except Exception:
            logger.exception('Unable to get location. Setting to None')
            job['location'] = None

        try:
            time = div.find('time', {'class': 'job-search-card__listdate'}) or div.find(
                'time', {'class': 'job-search-card__listdate--new'}
            )
            job['date_posted'] = time.get('datetime')
        except Exception:
            logger.exception('Error parsing job post date')
            error = 'date_posted'

        job['date_found'] = str(timezone.now())

        if error is not None:
            return None
        return job

    def parse(self, search_source: SearchSource) -> list[dict]:
        """Parse jobs."""
        search_source.set_status(Status.RUNNING)
        jobs = []
        page_count = self.get_page_count(search_source.search)
        period = search_source.calculate_period()
        for page in range(1, page_count + 1):
            url = self.get_linkedin_url('/jobs-guest/jobs/api/seeMoreJobPostings/', search_source.search, page, period)
            response = self.firefox.get_with_retry(url)
            if response is None:
                logger.warning('Response for %s is None', url)
                continue
            for div in self.firefox.soupify().find_all('div', {'class': 'job-search-card'}):
                job = self.parse_job(NullableTag(div))
                if job is not None:
                    jobs.append(job)
        search_source.set_status(Status.SUCCESS)
        return jobs

    def populate_job(self, job: Job) -> None:
        """Populate Job with description and easy apply status."""
        response = self.firefox.get_with_retry(job.url)
        if response is None:
            logger.warning('Response for %s is None', job.url)
            if self.firefox.last_status_code == 404:
                logger.warning('Job not found, marking as expired')
                job.update_status(Job.EXPIRED)

        soup = self.firefox.soupify()
        root = NullableTag(soup.html)
        job.raw_html = str(root)

        try:
            job.description = root.find('div', {'class': 'show-more-less-html__markup'}).decode_contents().strip()
        except Exception:
            logger.exception('Error parsing job description')

        try:
            code = root.find('code', {'id': 'applyUrl'})
            if code is not None:
                job.easy_apply = False
            else:
                job.easy_apply = True
        except Exception:
            logger.exception('Failed to parse easy application status. Defaulting to parse')
            job.easy_apply = False

        job.populated = True
        job.save()
