from SDL_Pi_HDC1080 import SDL_Pi_HDC1080


class TempHumidity:
  def __init__(self) -> None:
    self.hdc1080 = SDL_Pi_HDC1080()


  def read_temperature(self):
    return self.hdc1080.readTemperature()


  def read_humidity(self):
    return self.hdc1080.readHumidity()
