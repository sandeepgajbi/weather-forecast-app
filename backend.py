import requests

API_KEY = "141710af2113bab9f55ef73e1bcd33d5"


def get_data(place, forecast_day, kind):
    try:
        # Validate forecast_day
        if not isinstance(forecast_day, int) or forecast_day <= 0:
            raise ValueError("Forecast day must be a positive integer.")

        # Validate kind
        if kind not in ["Temperature", "Sky"]:
            raise ValueError("Invalid value for 'kind'. It must be 'Temperature' or 'Sky'.")

        url = f"https://api.openweathermap.org/data/2.5/forecast?q={place}&appid={API_KEY}"

        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()

        # Ensure that the response contains the expected data structure
        if "list" not in data:
            raise KeyError("Unexpected response format: 'list' key not found.")

        filter_data = data["list"]
        nr_values = 8 * forecast_day
        filter_data = filter_data[:nr_values]
        filter_date = [item["dt_txt"] for item in filter_data]

        if kind == "Temperature":
            filter_data = [item["main"]["temp"] / 10 for item in filter_data]
        elif kind == "Sky":
            filter_data = [item["weather"][0]["main"] for item in filter_data]

        return filter_date, filter_data, response.status_code

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None, None, response.status_code

    except (ValueError, KeyError) as e:
        print(f"Error processing data: {e}")
        return None, None, response.status_code


if __name__ == "__main__":
    date, data, response_code = get_data(place="Pune1", forecast_day=2, kind="Temperature")
    print(date, data, response_code)
