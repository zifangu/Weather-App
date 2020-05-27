import breezypythongui
import urllib.request
import json
import datetime
import time
from tkinter import PhotoImage


class weatherApp(breezypythongui.EasyFrame):
    """
    Illustrates command buttons and user events.
    """

    def __init__(self):
        """
        Sets up the window, label, and buttons.
        """
        super().__init__(title="Weather App")

        self.city_name = "Spartanburg, SC"

        # A single label in the first row.
        self.label = self.addLabel(text="Spartanburg, SC",
                                   row=0, column=0,
                                   columnspan=2, sticky="NSEW")

        self.label2 = self.addLabel(text="",
                                   row=1, column=0,
                                   columnspan=2, sticky="NSEW")

       
        self.label4 = self.addLabel(text="",
                                    row=0, column=2,
                                    columnspan=2, sticky="NSEW")
        self.label5 = self.addLabel(text="",
                                    row=4, column=0,
                                    columnspan=2, sticky="NSEW")
        self.image_label = self.addLabel(text="",
                                         row = 1, column = 3,
                                         sticky = "NSEW")

        # Two command buttons in the second row.
        self.enterBtn = self.addButton(text="New Location",
                                       row=3, column=0,
                                       command=self.enter)
        self.updateBtn = self.addButton(text="Update",
                                         row=3, column=1,
                                         command=self.update)

    # Methods to handle user events.
    def enter(self):
        """
        Resets the label to the empty string and the button states.
        """
        self.city_name = self.prompterBox(title = "City Name",
                    promptString = "Enter a city, state (i.e. Seattle, WA)",
                    inputText = self.city_name,
                    fieldWidth = 20)
        self.label["text"] = self.city_name
        city_input = self.city_name
        city_state = city_input.split(", ")
        self.enterBtn["state"] = "normal"
        self.updateBtn["state"] = "normal"
        return city_state


    def update(self):
        """

        :return: weather information at the input location
        """

        def getTemp():
            j = json.loads(getData())
            mainlst = j["main"]
            temp = mainlst["temp"]
            ftemp = str(temp) + " \N{DEGREE SIGN}" + "F"
            return ftemp

        def getUrl():
            city_state = self.label["text"]
            cityState = city_state.split(", ")
            url = "http://api.openweathermap.org/data/2.5/weather?q=%s,%s,USA&appid=" \
                  "{API key}&units=imperial" % (cityState[0], cityState[1])
            return url

        def getData():
            fp = urllib.request.urlopen(getUrl())
            mybytes = fp.read()
            weather = mybytes.decode("utf8")
            fp.close()
            return weather

        def getIcon():
            j = json.loads(getData())
            weatherlst = j["weather"][0]
            icon = weatherlst["icon"]
            return icon

        def getDes():
            j = json.loads(getData())
            weatherlst = j["weather"][0]
            des = weatherlst["description"]
            return des

        def getImage():
            name = getIcon()
            self.image = PhotoImage(file = "%s.gif" % name)
            return self.image
        
        self.label2["text"] = getTemp()
        
        self.label4["text"] = getDes()
        today = datetime.datetime.utcnow()
        today = today.time()
        j = json.loads(getData())
        time_zone = datetime.time(int(abs(j["timezone"])/3600), 0, 0)

        date = datetime.date(1, 1, 1)
        current_time = datetime.datetime.combine(date, today)
        adjust_zone = datetime.datetime.combine(date, time_zone)
        adjust_time = current_time - adjust_zone
        self.label5["text"] = "Current time at that location is: " + str(adjust_time)[:-7]
        self.image_label["image"] = getImage()
        self.enterBtn["state"] = "normal"
        self.updateBtn["state"] = "normal"


def main():
    """
    Instantiate and pop up the window.
    """
    weatherApp().mainloop()


if __name__ == "__main__":
    main()




