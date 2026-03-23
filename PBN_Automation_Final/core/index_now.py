import requests
import json
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IndexNowClient:
    def __init__(self, host, api_key, key_location=None):
        """
        :param host: Domain of the site (e.g. luckybetvip.com)
        :param api_key: IndexNow API Key
        :param key_location: URL to the key file (defaults to root if not provided)
        """
        self.host = host
        self.api_key = api_key
        # If key_location is not provided, IndexNow expects it at https://host/api_key.txt
        self.key_location = key_location or f"https://{host}/{api_key}.txt"
        self.endpoints = [
            "https://www.bing.com/indexnow",
            "https://yandex.com/indexnow",
            "https://search.indexnow.org/indexnow"
        ]

    def submit_urls(self, url_list):
        """
        Submit a list of URLs to IndexNow endpoints.
        Automatically splits large batches to comply with API limits.
        """
        if isinstance(url_list, str):
            url_list = [url_list]

        # Rate limiting: Split into batches of max 100 URLs
        MAX_BATCH_SIZE = 100
        all_results = {}
        
        for i in range(0, len(url_list), MAX_BATCH_SIZE):
            batch = url_list[i:i + MAX_BATCH_SIZE]
            logger.info(f"Submitting batch {i//MAX_BATCH_SIZE + 1}: {len(batch)} URLs")
            
            payload = {
                "host": self.host,
                "key": self.api_key,
                "keyLocation": self.key_location,
                "urlList": batch
            }

            batch_results = {}
            for endpoint in self.endpoints:
                try:
                    response = requests.post(
                        endpoint,
                        headers={"Content-Type": "application/json; charset=utf-8"},
                        data=json.dumps(payload),
                        timeout=10
                    )
                    batch_results[endpoint] = {
                        "status_code": response.status_code,
                        "success": 200 <= response.status_code < 300
                    }
                    if batch_results[endpoint]["success"]:
                        logger.info(f"Successfully submitted to {endpoint}")
                    else:
                        logger.warning(f"Failed to submit to {endpoint}: {response.status_code} {response.text}")
                except Exception as e:
                    logger.error(f"Error submitting to {endpoint}: {e}")
                    batch_results[endpoint] = {"error": str(e), "success": False}
            
            all_results[f"batch_{i//MAX_BATCH_SIZE + 1}"] = batch_results
        
        return all_results

if __name__ == "__main__":
    # Test stub
    # KEY = os.getenv("INDEXNOW_API_KEY", "test_key")
    # client = IndexNowClient("luckybetvip.com", KEY)
    # client.submit_urls(["https://luckybetvip.com/test-article/"])
    pass
