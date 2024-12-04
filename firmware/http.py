from requests import get, post
from datetime import datetime

class HttpApi:
  def __init__(self) -> None:
    self.base_url = 'https://integration-offices-3-monorepo.onrender.com'
    self.headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.5",
    "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkNTBhZjE0My01MWEyLTQwOWQtOWMwMC0xNTg4OGRkMjM2MDQiLCJleHAiOjE3MzMyODA4MjJ9.awasT04BX2fx4dtmIwkrATYdshRdFZvZNeuiHIgsrVg"
    }


  def get_parameters(self, chamber_id):
    response = get(self.base_url + '/chamber/parameters/' + chamber_id, headers=self.headers)

    if response.status_code != 200:
      return None

    return response.json()

  def send_metrics(self, chamber_id: str, soil_moisture: float, temperature: float, humidity: float, api_url: str, token: str):

    payload = {
        "chamberId": chamber_id,
        "leafCount": 99999,
        "greenArea": 99999,
        "estimateDate": datetime.now().isoformat(),  # Format the datetime to ISO string
        "soilMoisture": soil_moisture or 50,  # Replace with actual soil moisture sensor value
        "temperature": temperature or 25,  # Replace with actual temperature sensor value
        "humidity": humidity or 50  # Replace with actual humidity sensor value
    }


    response = post(api_url + '/estimates/', json=payload, headers={"Authorization": token})

    return response.status_code >= 200 and response.status_code < 300
