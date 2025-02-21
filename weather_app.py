import sys
import requests
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)
from PyQt5.QtCore import Qt


class WeatherApp(QWidget):

    def __init__(self):
        super().__init__()

        # Initializing the widgets
        self.city_label = QLabel("Enter city name:", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)

        # Initializing the UI
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")

        # Layout Manager
        vbox = QVBoxLayout()

        # Adding widgets to the layout manager
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        # Pass in the layout manager to the weather app object
        self.setLayout(vbox)

        # Aligning the elements
        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        # Setting an object name for each widget so that CSS styling can be applied
        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")

        # Setting the stylesheet
        self.setStyleSheet(
            """
            QLabel, QPushButton{
                font-family: Calibri;
            }
            QLabel#city_label{
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#city_input{
                font-size: 40px;
            }
            QPushButton#get_weather_button{
                font-size: 30px;
                font-weight: bold;
            }
            QLabel#temperature_label{
                font-size: 75px;
            }
            QLabel#emoji_label{
                font-size: 100px;
                font-family: Segoe UI emoji;
            }
            QLabel#description_label{
                font-size: 50px;
            }
        """
        )

        # Connecting the signal to a slot (signal = clicked, slot = get_weather function)
        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "53def18b4b48b33b3dc6de85aecd47b8"

        # Getting the text input inside the line edit (text box)
        city = self.city_input.text()

        # Get the URL from the documentation in the openweathermap.org website
        # https://openweathermap.org/current#name
        # This is the url used to fetch the data, using f-string, we input the city
        # inputted by the user on the city_input line edit and api_key that we got
        # from the website itself
        url = (
            f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        )

        try:
            # response object
            # API request by creating response object using the requests module
            response = requests.get(url)

            # This method will raise any exception if there's any HTTP errors because normally
            # the try catch does not do that
            response.raise_for_status()

            # Converts the data into a .json
            data = response.json()

            # cod -> status code
            if data["cod"] == 200:
                self.display_weather(data)

        # Catching possible exceptions
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad request:\nPlease check your input.")
                case 401:
                    self.display_error("Unauthorized:\nInvalid API key.")
                case 403:
                    self.display_error("Forbidden:\nAccess is denied.")
                case 404:
                    self.display_error("Not Found:\nCity not found.")
                case 500:
                    self.display_error(
                        "Internal Server Error:\nPlease try again later."
                    )
                case 502:
                    self.display_error(
                        "Bad Gateway:\nInvalid response from the server."
                    )
                case 503:
                    self.display_error("Service Unavailable:\nServer is down.")
                case 504:
                    self.display_error("Gateway Timeout:\nNo response from the server.")
                case _:
                    self.display_error(f"HTTP error occured: {http_error}")

        except requests.exceptions.ConnectionError:
            self.display_error("Connection Error:\nCheck your internet connection.")
        except requests.exceptions.Timeout:
            self.display_error("Timeout Error:\nThe request timed out.")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many Redirects:\nCheck the URL.")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error: {req_error}")

    def display_error(self, message):
        # Change the font-size
        self.emoji_label.setStyleSheet("font-size: 20px;")

        # We will use the temperature_label part of the widget
        # to display the error message since no temperature
        # will be shown anyway.

        # The error message will take its place
        self.emoji_label.setText(message)

        self.temperature_label.clear()
        self.description_label.clear()

    def display_weather(self, data):
        self.emoji_label.setStyleSheet("font-size: 100px;")

        # Calling the temperature data from the data json file
        temperature_k = data["main"]["temp"]
        temperature_c = temperature_k - 273.15
        # temperature_f = (temperature_k * 9 / 5) - 459.67

        # Retrieving weather description data from the data json file
        weather_description = data["weather"][0]["description"]

        # Retrieving weather ID data from the data json file
        # https://openweathermap.org/weather-conditions
        weather_id = data["weather"][0]["id"]

        self.temperature_label.setText(f"{temperature_c:.0f}°C")
        self.emoji_label.setText(self.get_weather_emoji(weather_id))
        self.description_label.setText(weather_description)

    @staticmethod
    def get_weather_emoji(weather_id):

        if 200 <= weather_id <= 232:
            return "⛈️"
        elif 300 <= weather_id <= 321:
            return "🌦️"
        elif 500 <= weather_id <= 531:
            return "🌧️"
        elif 600 <= weather_id <= 622:
            return "🌨️"
        elif 701 <= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "☀️"
        elif 800 <= weather_id <= 804:
            return "🌥️"
        else:
            return ""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()

    weather_app.show()

    sys.exit(app.exec_())
