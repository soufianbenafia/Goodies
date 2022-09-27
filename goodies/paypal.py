import sys

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment


class PayPalClient:
    def __init__(self):
        self.client_id = "AaCYTz814T9bwzTi7tfvnzLusUdTkXX0OKlNMQOjLhfT2w4OQcRt2-SD2v4M4mwOLtiLCun8mEdbU9XS"
        self.client_secret = "EMZIxw-hrL0mlSv14HgPhRjBz7ohzTot8UogJ886rV3GtE-4NYAWeRzhgfF2cEV-XQxSg6K8Om9seJCq"
        self.environment = SandboxEnvironment(
            client_id=self.client_id, client_secret=self.client_secret)
        self.client = PayPalHttpClient(self.environment)
