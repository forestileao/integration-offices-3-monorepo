from requests import get, post
from datetime import datetime

class HttpApi:
  def __init__(self) -> None:
    self.base_url = 'https://integration-offices-3-monorepo.onrender.com'
    self.headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.5",
    "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4MmM1ODc2My04ODcwLTQ2MTQtOTM1Mi01OTVkYTRjZjg5NDkiLCJleHAiOjIwNTE4MjA0Njd9.xYZP-S1vS2o-ddZKkp99a1HpajUj01FTwCbu9YFHy3w"
    }


  def get_parameters(self, chamber_id):
    try:
      response = get(self.base_url + '/chamber/parameters/' + chamber_id + '/', headers=self.headers)

      if response.status_code != 200:
        return None

      return response.json()
    except Exception as e:
      return None

  def send_metrics(self, chamber_id: str, soil_moisture: float, temperature: float, humidity: float, water_level: float, lightState: bool = False):
    try:
      payload = {
          'lightState': lightState,
          "chamberId": chamber_id,
          "estimateDate": datetime.now().isoformat(),  # Format the datetime to ISO string
          "soilMoisture": soil_moisture,  # Replace with actual soil moisture sensor value
          "temperature": temperature or 25,  # Replace with actual temperature sensor value
          "humidity": humidity,  # Replace with actual humidity sensor value
          "waterLevel": water_level  # Replace with actual water level sensor value
      }

      response = post(self.base_url + '/estimates/', json=payload, headers=self.headers)
      print('Tried to send Metris, status code:', response.status_code, 'response:', response.content)
      return response.status_code >= 200 and response.status_code < 300
    except Exception as e:
      print(e)
      return False

  def send_photo(self, chamber_id: str, img_bin: bytes):
    try:
      files = {
          'photo': ('photo.jpg', img_bin, 'image/jpeg')  # Specify filename and content type
      }
      response = post(
          self.base_url + f'/photos/{chamber_id}/',
          files=files,
          headers=self.headers
      )
      print('Tried to send photo, status code:', response.status_code, 'response:', response.content)
      return response.status_code >= 200 and response.status_code < 300
    except Exception as e:
      print(e)
      return False


if __name__ == '__main__':
  chambers = [
    {
      'id': '90617ba4-ee9b-488f-82bc-cbe8b43aac67',
      'parameters': {
        "temperatureRange": "17",
        "soilMoistureLowerLimit": 60,
        "photoCaptureFrequency": "60",
        "id": "b231822f-5e74-41ea-9678-0c61404fe6dd",
        "lightingRoutine": "07:40/18:20",
        "ventilationSchedule": "10:00/11:00"
      }
    },
    {
      'id': '7ce04bef-2212-4a9b-8262-ed659cd124ab',
      'parameters': {
        "temperatureRange": "28",
        "soilMoistureLowerLimit": 60,
        "photoCaptureFrequency": "60",
        "id": "1e43809c-0daa-413f-ab18-988ef80e4af6",
        "lightingRoutine": "07:40/18:20",
        "ventilationSchedule": "10:00/11:00"
        }
    },
  ]

  api = HttpApi()



  for chamber in chambers:
    print(api.get_parameters(chamber['id']))
    print(api.send_metrics(chamber['id'], 50, 25, 50, 50))

    with open('example.jpg', 'rb') as f:
      print(api.send_photo(chamber['id'], f.read()))
