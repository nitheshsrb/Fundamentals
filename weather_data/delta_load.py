import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry
from datetime import datetime

def delta_load():
    end_date = datetime.today().strftime('%Y-%m-%d')