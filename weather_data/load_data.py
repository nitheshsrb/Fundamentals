import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
import datetime

def load_data (start_date, end_date,load_type):
	# Setup the Open-Meteo API client with cache and retry on error
	cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
	retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
	openmeteo = openmeteo_requests.Client(session = retry_session)

	if load_type == "actuals":
		# Make sure all required weather variables are listed here
		# The order of variables in hourly or daily is important to assign them correctly below
		url = "https://archive-api.open-meteo.com/v1/archive"
		params = {
			"latitude": 51.5085,
			"longitude": -0.1257,
			"start_date": start_date,
			"end_date": end_date,
			"daily": ["temperature_2m_max", "dew_point_2m_mean", "et0_fao_evapotranspiration", "snowfall_sum", "cloud_cover_mean"],
			"timezone": "GMT",
		}
		responses = openmeteo.weather_api(url, params = params)

		# Process first location. Add a for-loop for multiple locations or weather models
		response = responses[0]
		print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
		print(f"Elevation: {response.Elevation()} m asl")
		print(f"Timezone: {response.Timezone()}{response.TimezoneAbbreviation()}")
		print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

		# Process daily data. The order of variables needs to be the same as requested.
		daily = response.Daily()
		daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
		daily_dew_point_2m_mean = daily.Variables(1).ValuesAsNumpy()
		daily_et0_fao_evapotranspiration = daily.Variables(2).ValuesAsNumpy()
		daily_snowfall_sum = daily.Variables(3).ValuesAsNumpy()
		daily_cloud_cover_mean = daily.Variables(4).ValuesAsNumpy()

		daily_data = {
			"date": pd.date_range(
				start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
				end =  pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
				freq = pd.Timedelta(seconds = daily.Interval()),
				inclusive = "left"
			)
		}

		daily_data['date'] = pd.to_datetime(daily_data['date']).date
		daily_data["temperature_2m_max"] = daily_temperature_2m_max
		daily_data["dew_point_2m_mean"] = daily_dew_point_2m_mean
		daily_data["et0_fao_evapotranspiration"] = daily_et0_fao_evapotranspiration
		daily_data["snowfall_sum"] = daily_snowfall_sum
		daily_data["cloud_cover_mean (%)"] = daily_cloud_cover_mean

		daily_dataframe = pd.DataFrame(data = daily_data)
		daily_dataframe.sort_values(by='date',ascending = False)
	else:

		# Make sure all required weather variables are listed here
		# The order of variables in hourly or daily is important to assign them correctly below
		url = "https://api.open-meteo.com/v1/forecast"
		params = {
			"latitude": 51.5085,
			"longitude": -0.1257,
			"daily": ["temperature_2m_max", "dew_point_2m_mean","et0_fao_evapotranspiration_sum", "snowfall_sum", "cloud_cover_mean"],
			"timezone": "GMT",
			"start_date": start_date,
			"end_date": end_date
		}
		responses = openmeteo.weather_api(url, params = params)

		# Process first location. Add a for-loop for multiple locations or weather models
		response = responses[0]
		print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
		print(f"Elevation: {response.Elevation()} m asl")
		print(f"Timezone: {response.Timezone()}{response.TimezoneAbbreviation()}")
		print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

		# Process daily data. The order of variables needs to be the same as requested.
		daily = response.Daily()
		daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
		daily_dew_point_2m_mean = daily.Variables(1).ValuesAsNumpy()
		daily_et0_fao_evapotranspiration_sum = daily.Variables(2).ValuesAsNumpy()
		daily_snowfall_sum = daily.Variables(3).ValuesAsNumpy()
		daily_cloud_cover_mean = daily.Variables(4).ValuesAsNumpy()

		daily_data = {
			"date": pd.date_range(
				start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
				end =  pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
				freq = pd.Timedelta(seconds = daily.Interval()),
				inclusive = "left"
			)
		}

		daily_data["temperature_2m_max"] = daily_temperature_2m_max
		daily_data["dew_point_2m_mean"] = daily_dew_point_2m_mean
		daily_data["et0_fao_evapotranspiration_sum"] = daily_et0_fao_evapotranspiration_sum
		daily_data["snowfall_sum"] = daily_snowfall_sum
		daily_data["cloud_cover_mean"] = daily_cloud_cover_mean

		daily_dataframe = pd.DataFrame(data = daily_data)
	return daily_dataframe


