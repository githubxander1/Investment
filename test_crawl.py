import pytest
from crawl4ai import AsyncWebCrawler

@pytest.mark.asyncio
async def test():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(url='https://httpbin.org/html')
        print(result)
        print(result.markdown[:200])
        print(result.success)
        assert result.success == True
        return result