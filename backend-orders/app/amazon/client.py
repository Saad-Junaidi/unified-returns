from datetime import datetime, timezone
from sp_api.api import Orders
from sp_api.base import SellingApiException, Marketplaces
import os


class AmazonClient:
    def __init__(self):
        credentials = {
            "refresh_token": os.getenv("SP_API_REFRESH_TOKEN"),
            "lwa_app_id": os.getenv("SP_API_LWA_CLIENT_ID"),
            "lwa_client_secret": os.getenv("SP_API_LWA_CLIENT_SECRET"),
            "aws_secret_access_key": os.getenv("SP_API_AWS_SECRET"),
            "aws_access_key_id": os.getenv("SP_API_AWS_ACCESS_KEY"),
        }

        self.orders_api = Orders(
            marketplace=Marketplaces.US,
            credentials=credentials,
        )

    def get_orders(self, last_updated_after: datetime):
        try:
            # FORCE UTC + AMAZON-APPROVED FORMAT
            if last_updated_after.tzinfo is None:
                last_updated_after = last_updated_after.replace(
                    tzinfo=timezone.utc
                )

            timestamp = last_updated_after.strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            )

            result = self.orders_api.get_orders(
                LastUpdatedAfter=timestamp
            )

            return result.payload

        except SellingApiException as e:
            raise RuntimeError(str(e))
