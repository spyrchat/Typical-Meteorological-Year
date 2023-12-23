import urllib.request

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
        hour = int(time_UTC[i].split(':')[1][:2])  # Extract hour
        hourly_wind_data[hour].append(wind_direction)

    # Calculate mean wind direction per hour
    mean_directions = {}
    for hour, directions in hourly_wind_data.items():
        mean_direction = sum(directions) / len(directions) if directions else 0
        mean_directions[hour] = mean_direction

    return mean_directions

# Example usage
if __name__ == "__main__":
    mean_wind_directions = get_tmy(41.141816091983856, 24.891168951039393)
    print(mean_wind_directions)
