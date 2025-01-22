import PyQt6.QtCore
import PyQt6.QtGui
import PyQt6.QtWidgets
import sys, PyQt6, requests



# Project 4 - Should you wear a Jacket?

############################################################
# Part 1 - The Backend Stuff


API_KEY = ""
API_KEYWEATHER = ""

chosenCity = "Choose your city"
cityLatitude = 0
cityLongitude = 0
cityTemperature = 0
cityFeelsLike = 0
cityDescription = ""
cityIcon = "01d"
cityName = ""
country = ""

latitude_longitude_search_url = "http://api.openweathermap.org/geo/1.0/direct"
current_weather_search_url = "https://api.openweathermap.org/data/3.0/onecall"

# Getting Coordinates for chosen city



def fetchLatLong():
    longLatParams = {
        "apikey": API_KEY,
        "q": chosenCity  # Replace with the city you want to search for
    }

    # Fetches Latitude and Longitude based on city
    locationResponse = requests.get(latitude_longitude_search_url, params=longLatParams)
    # Parsing our data to JSON
    global locationData
    locationData = locationResponse.json()
    
    if locationData:
        # This one is a list! So we don't need to iterate it
        global cityName, cityLatitude, cityLongitude
        try:
            cityName = locationData[0]["name"]
            # Rounding down for convenience's sake
            cityLatitude = round(locationData[0]["lat"], 2)
            cityLongitude = round(locationData[0]["lon"], 2)
            fetchTemp()
        except (KeyError, IndexError):
            pass

def fetchTemp():
    # Take new params and FORCE THE USER TO USE METRIC LIKE A REGULAR PERSON
    currentWeatherParams = {
    "lat": cityLatitude,
    "lon": cityLongitude,
    "appid": API_KEYWEATHER,
    "units": "metric"
    }
    # Fetch current weather conditions and parse to JSON

    weatherResponse = requests.get(current_weather_search_url, params=currentWeatherParams)
    global weatherData
    weatherData = weatherResponse.json()

    # This one is a dictionary. Let's set the variables to each correspondant piece of data in the JSON:
    global cityTemperature, cityFeelsLike, cityDescription, cityIcon
    cityTemperature = int(weatherData["current"]["temp"])
    cityFeelsLike = weatherData["current"]["feels_like"]
    cityDescription = weatherData["current"]["weather"][0]["description"]
    cityIcon = weatherData["current"]["weather"][0]["icon"]

# Our work here is mostly done. Backend works pretty smoothly.

############################################################
# Part 2 - The UI

class UI(PyQt6.QtWidgets.QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.initUI()



    def loadFonts(self):
        # Load the custom font
        fontId = PyQt6.QtGui.QFontDatabase.addApplicationFont("assets/Roboto.ttf")
        font_family = PyQt6.QtGui.QFontDatabase.applicationFontFamilies(fontId)[0]
        my_font = PyQt6.QtGui.QFont(font_family, 25)
        return my_font
    

    def initUI(self):

        central_widget = PyQt6.QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        # Setting up frame
        self.setWindowTitle("Should You Wear a Jacket?")
        self.setWindowIcon(PyQt6.QtGui.QIcon("assets/jacket.png"))
        self.setStyleSheet("background-color: #2E2E2E; color: #FFFFFF;")
        self.setFixedSize(400, 300)  # Set fixed window size
        self.setWindowFlags(PyQt6.QtCore.Qt.WindowType.WindowCloseButtonHint | PyQt6.QtCore.Qt.WindowType.WindowMinimizeButtonHint)  # Disable resizing

        # Setting up the layout manager
        hbox = PyQt6.QtWidgets.QHBoxLayout()
        central_widget.setLayout(hbox)

        global customFont 
        customFont = self.loadFonts()
        
        # Creating the necessary widgets
        # SIDE LABEL - Yes or No
        self.yesno = PyQt6.QtWidgets.QLabel("Yes!")
        self.yesno.setStyleSheet("font-size: 28px; font-weight: bold; color: #FF6347;")
        self.yesno.setVisible(False)  # Initially hidden

        hbox.addWidget(self.yesno)

        vbox = PyQt6.QtWidgets.QVBoxLayout()

        # TOP LABEL
        self.title = PyQt6.QtWidgets.QLabel("Should You Wear a Jacket?")
        self.title.setStyleSheet("font-size: 25px; font-weight: bold; margin-bottom: 10px;")

        # Add spacers to center the title label
        title_hbox = PyQt6.QtWidgets.QHBoxLayout()
        title_hbox.addStretch(1)
        title_hbox.addWidget(self.title)
        title_hbox.addStretch(1)

        # Icon - REMINDER TO FETCH ICON FROM API!!!!!!

        # Creating an IconLabel
        self.iconLabel = PyQt6.QtWidgets.QLabel()
        iconURL = f"https://openweathermap.org/img/wn/{cityIcon}@4x.png"
        response = requests.get(iconURL)
        if response.status_code == 200:
            # Converting the image data to a Pixmap
            image_data = response.content
            pixmap = PyQt6.QtGui.QPixmap("assets/jacket.png")
            scaled_pixmap = pixmap.scaled(150, 150, PyQt6.QtCore.Qt.AspectRatioMode.KeepAspectRatio, PyQt6.QtCore.Qt.TransformationMode.SmoothTransformation)
            self.iconLabel = PyQt6.QtWidgets.QLabel()
            self.iconLabel.setScaledContents(False)
            self.iconLabel.setPixmap(scaled_pixmap)

        

        # Creating a Temperature Label
        formattedTempText = (str(cityTemperature) + " - " + str(cityDescription).capitalize())
        self.temperatureLabel = PyQt6.QtWidgets.QLabel(formattedTempText)
        self.temperatureLabel.setStyleSheet("font-size: 30px; margin-bottom: 10px; font-style: bold;")
        self.temperatureLabel.setVisible(False)  # Initially hidden
        self.temperatureLabel.setFont(customFont)

        # Creating the City Name Label
        self.cityLabel = PyQt6.QtWidgets.QLabel(chosenCity)
        self.cityLabel.setStyleSheet("font-size: 30px; font-style: bold; margin-bottom: 10px;")

        # Creating the Line Edit and setting up the enter function press
        self.lineEdit = PyQt6.QtWidgets.QLineEdit()
        self.lineEdit.setPlaceholderText("Your city here")
        self.lineEdit.setStyleSheet("padding: 8px; font-size: 16px; border: 1px solid #FFFFFF; border-radius: 5px;")
        self.lineEdit.returnPressed.connect(self.enterPressed)

        # Add spacers to center the icon and city label
        icon_hbox = PyQt6.QtWidgets.QHBoxLayout()
        icon_hbox.addStretch(1)
        icon_hbox.addWidget(self.iconLabel)
        icon_hbox.addStretch(1)

        city_hbox = PyQt6.QtWidgets.QHBoxLayout()
        city_hbox.addStretch(1)
        city_hbox.addWidget(self.cityLabel)
        city_hbox.addStretch(1)

        # Setting all layouts
        hbox.addLayout(vbox)
        vbox.addLayout(title_hbox)  # Add the centered title layout
        vbox.addLayout(icon_hbox)  # Add the centered icon layout
        vbox.addWidget(self.temperatureLabel)
        vbox.addLayout(city_hbox)  # Add the centered city label layout
        vbox.addWidget(self.lineEdit)

    # What to do when we press enter
    def enterPressed(self):
        global chosenCity
        chosenCity = self.lineEdit.text()
        fetchLatLong()
        self.updateUI()
        self.lineEdit.setText("")

    def updateUI(self):
        try:
            country = locationData[0]["country"]
            self.cityLabel.setText(cityName.title() + ", " + country)
            self.cityLabel.setFont(customFont)
            self.title.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 10px; margin-right: 5px;")
            self.temperatureLabel.setText(f"{cityTemperature}° - {cityDescription.capitalize()}")
            self.temperatureLabel.setVisible(True)  # Make visible after fetching data
            self.yesno.setVisible(True)  # Make visible after fetching data

            if cityTemperature >= 15:
                self.yesno.setText("No!")
                self.yesno.setStyleSheet("font-size: 28px; font-weight: bold; color: #32CD32;")
            else:
                self.yesno.setText("Yes!")
                self.yesno.setStyleSheet("font-size: 28px; font-weight: bold; color: #FF6347;")

            iconURL = f"https://openweathermap.org/img/wn/{cityIcon}@4x.png"
            response = requests.get(iconURL)
            if response.status_code == 200:
                image_data = response.content
                pixmap = PyQt6.QtGui.QPixmap()
                pixmap.loadFromData(PyQt6.QtCore.QByteArray(image_data))
                self.iconLabel.setPixmap(pixmap)
        except (KeyError, IndexError):
            self.cityLabel.setText("City not Found.")
        
        


def run():
    app = PyQt6.QtWidgets.QApplication(sys.argv) # The GUI Manager. Manages everything for our window.
    window = UI() # Creates a window based on our template up there
    window.show() # Ensures it is not instantly hidden
    sys.exit(app.exec()) # Makes it so you can easily close it 
    

run()




