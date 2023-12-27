import urllib.request, urllib.parse, urllib.error
import math
import numpy as np
import matplotlib.pyplot as plt
import os
"""
ΟΝΟΜΑΤΕΠΩΝΥΜΟ: Χρήστος Μπιγδέλης
ΑΜ: 151930
"""

# <--- ΕΔΩ ΘΑ ΜΠΟΥΝ ΟΙ ΒΙΒΛΙΟΘΗΚΕΣ ΠΟΥ ΘΑ ΧΡΗΣΙΜΟΠΟΙΉΣΕΤΕ

def get_tmy(lati, long):
    time_UTC, WD10m = [], []

    try:
        fhand = urllib.request.urlopen(f'https://re.jrc.ec.europa.eu/api/tmy?lat={lati}&lon={long}')

        for line in fhand:
            line = line.decode().strip()
            if line.startswith("20"):  # Check for data lines
                words = line.split(',')
                time_UTC.append(words[0])
                WD10m.append(float(words[8]))  # Assuming 9th item is wind direction

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
    hours = list(mean_wind_directions.keys())
    directions = list(mean_wind_directions.values())

    plt.scatter(hours, directions)
    plt.xlabel('Hour of the Day')
    plt.ylabel('Mean Wind Direction (Degrees)')
    plt.title('Mean Wind Direction Per Hour')
    plt.plot(hours, directions, '--', label='Dashed Line')
    plt.grid(True)
    plt.text(0.5, 1.1, "Χρήστος Μπιγδέλης, 151930", ha='center', va='bottom', transform=plt.gca().transAxes)
    # Saving the plot as a JPEG file
    folder_path = r'C:\dewp2023'

    # Check if the folder exists, and create it if not
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Your plot code here

    # Save the plot in the created folder
    plt.savefig(os.path.join(folder_path, '151930_graph3.jpeg'))
    # plt.savefig('C:\\BLABLA\\151930_graph3.jpeg')

    plt.show()

# ΣΧΟΛΙΑΣΕΤΕ ΤΟΝ ΚΩΔΙΚΑ ΣΑΣ

if __name__ == "__main__":
    mean_wind_directions = get_tmy(41.141816091983856, 24.891168951039393)
    print(mean_wind_directions)
    plot_mean_wd_per_hour(mean_wind_directions)