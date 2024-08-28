import requests
import schedule
import time
from datetime import datetime
import sqlite3
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from PIL import Image, ImageTk



API_KEY = 'b87030c44c69361d8dcb802e1a2f4c61'  # Task 0 .Replace with your API key
your_city = 'Hong Kong'
API_URL = f'http://api.openweathermap.org/data/2.5/weather?q={your_city}&appid={API_KEY}&units=metric'


# Task 1. define a database and table
def create_weather_table():
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS weather_data(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME NOT NULL, 
                temperature REAL NOT NULL, 
                humidity INTEGER NOT NULL, 
                weather TEXT NOT NULL)''')
    
    conn.commit()
    conn.close()

def fetch_weather_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        weather_data = {
            'timestamp': datetime.now(),
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'weather': data['weather'][0]['description'],
        }

        print(weather_data)
        insert_weather_data(weather_data)
        plot_temperature_trend()
        plot_humidity_trend()


        # Task 2. Add weather data into the database
def insert_weather_data(weather_data):
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()
    c.execute('''
    INSERT INTO weather_data (timestamp, temperature, humidity, weather)
    VALUES (?, ?, ?, ?)
    ''', (weather_data['timestamp'], weather_data['temperature'], weather_data['humidity'], weather_data['weather']))
          
    conn.commit()

    conn.close()


# Task 3. write functions to perform analysis - generate analysis based on weather data
def plot_temperature_trend():
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM weather_data ORDER BY timestamp')
    all_rows = c.fetchall()
    
    timestamps = [datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S.%f') for row in all_rows]  
    temperatures = [row[2] for row in all_rows]
    
    conn.close()

    plt.figure(figsize=(10, 6))
    plt.plot_date(timestamps, temperatures, linestyle='-', marker='')
    plt.xlabel('Timestamp')
    plt.ylabel('Temperature (°C)')
    plt.title('Temperature Trend')
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))  
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(rotation=45)
    plt.grid(True)
    
    plt.show()

def plot_humidity_trend():
    conn = sqlite3.connect('weather_data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM weather_data ORDER BY timestamp')
    all_rows = c.fetchall()
    
    timestamps = [datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S.%f') for row in all_rows]  
    humidities = [row[3] for row in all_rows]
    
    conn.close()

    plt.figure(figsize=(10, 6))
    plt.plot_date(timestamps, humidities, linestyle='-', marker='')
    plt.xlabel('Timestamp')
    plt.ylabel('Humidity (%)')
    plt.title('Humidity Trend')
    
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))  
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.xticks(rotation=45)
    plt.grid(True)
    
    plt.show()



# Task 4. Create interface to interact with data or get reports, use tkinter or terminal but remember to make it data centric and user frinedly

def display_interface():
    root = tk.Tk()
    root.title("Weather Data Analysis")
    root.geometry("400x300")

    try:
        image = Image.open("picture.png")
        photo = ImageTk.PhotoImage(image)
        
        bg_label = tk.Label(root, image=photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception as e:
        print(f"Error loading the image: {e}")

    style = ttk.Style()
    style.configure('TButton',background='#bdc630', foreground='white')

    style.map('TButton', background=[('active', '#bdc630')])

    label = tk.Label(root, text="Select the Weather Data Analysis", font=("Arial", 16))
    label.pack(pady=20)

    temperature_button = ttk.Button(root, text="🌡️ Temperature Trend", command=plot_temperature_trend, width=20, style='TButton', cursor="hand2")
    temperature_button.pack(pady=10)

    humidity_button = ttk.Button(root, text="💧 Humidity Trend", command=plot_humidity_trend, width=20, style='TButton', cursor="hand2")
    humidity_button.pack(pady=10)


    root.mainloop()


def main():
    create_weather_table()

    interval = input("Enter the interval in minutes (default is 1): ")
    interval = int(interval) if interval.isdigit() else 1

    schedule.every(interval).minutes.do(fetch_weather_data)
    
    print(f"Scheduler started. Fetching weather data every {interval} minute(s).")
    
    while True:
        schedule.run_pending()
        time.sleep(1)
display_interface()

if __name__ == "__main__":
    main()
    display_interface()


# Bonus Task 5. compare cities