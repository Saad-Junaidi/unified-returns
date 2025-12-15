from sp_api.api import Orders
from sp_api.base import SellingApiException, Marketplaces
import os

class AmazonClient:
    def __init__(self):
        # Your version of Credentials expects a DICT
        credentials_dict = {
            "refresh_token": os.getenv("SP_API_REFRESH_TOKEN"),
            "lwa_app_id": os.getenv("SP_API_LWA_CLIENT_ID"),
            "lwa_client_secret": os.getenv("SP_API_LWA_CLIENT_SECRET"),
            "aws_secret_access_key": os.getenv("SP_API_AWS_SECRET"),
            "aws_access_key_id": os.getenv("SP_API_AWS_ACCESS_KEY"),
        }

        self.orders_api = Orders(
            marketplace=Marketplaces.US,
            credentials=credentials_dict
        )

    def get_orders(self):
        try:
            result = self.orders_api.get_orders(
                CreatedAfter="2025-12-12T00:00:00Z"
            )
            return result.payload
        except SellingApiException as e:
            return {"error": str(e)}
