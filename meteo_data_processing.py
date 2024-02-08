import urllib.request, urllib.parse, urllib.error
import math
import numpy as np
import matplotlib.pyplot as plt
import os

def get_tmy(lati, long):
    time_UTC, WD10m = [], []

    try:
        fhand = urllib.request.urlopen(f'https://re.jrc.ec.europa.eu/api/tmy?lat={lati}&lon={long}')

        for line in fhand:
            line = line.decode().strip()
            if line.startswith("20"):  # Check for data lines
                words = line.split(',')
                time_UTC.append(words[0])
                WD10m.append(float(words[8]))  # Wind Direction is the 9th item in the list

    except Exception as e:
        print(f"An error occurred: {e}")
        return

    # Process wind direction data
    hourly_wind_data = {hour: [] for hour in range(24)}

    for i, wind_direction in enumerate(WD10m):
        try:
            hour = int(time_UTC[i].split(':')[1][:2])  # Extract hour
            hourly_wind_data[hour].append(wind_direction)
        except Exception as e:
            print(f"Error processing time_UTC[{i}]: {time_UTC[i]}, Error: {e}")

    # Calculate mean wind direction per hour
    mean_directions = {}
    for hour, directions in hourly_wind_data.items():
        # Convert degrees to vectors
        vectors = [(math.cos(math.radians(d)), math.sin(math.radians(d))) for d in directions]
        # Calculate mean vector
        mean_vector = np.mean(vectors, axis=0)
        # Convert vector back to degrees
        radians = math.atan2(mean_vector[1], mean_vector[0])
        mean_direction = math.degrees(radians)
        mean_direction = mean_direction if mean_direction >= 0 else mean_direction + 180
        mean_directions[hour] = mean_direction

    return mean_directions


def plot_mean_wd_per_hour(wd_list):
    hours = sorted(wd_list.keys())  # Ensure the hours are sorted
    directions = [wd_list[h] for h in hours]  # Sort directions according to sorted hours

    plt.figure(figsize=(12, 8))  # Set a figure size for better visibility
    plt.scatter(hours, directions, marker='o', s=100)  # Increase marker size
    plt.plot(hours, directions, 'b--', label='Variation in the duration of the Day')  # Add color to the dashed line for visibility
    plt.xlabel('Hour of the Day (UTC)')
    plt.ylabel('Mean Wind Direction (degrees)')
    plt.title('Mean Wind Direction per Hour of the Day (UTC)')
    plt.xticks(range(0, 24))
    plt.legend()  # Add a legend
    plt.grid(True)

    for i, txt in enumerate(directions):
        plt.annotate(f"{txt:.2f}", (hours[i], directions[i]), textcoords="offset points", xytext=(0,10), ha='center')

    plt.text(0.5, -0.1, "Typical Wind Direction per Hour of the Day (UTC)")
    
    folder_path = r'C:\wind_direction_data_plots'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    plt.savefig(os.path.join(folder_path, 'meteo_plot.jpeg'))
    plt.show()

