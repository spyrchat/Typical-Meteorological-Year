from meteo_data_processing import get_tmy, plot_mean_wd_per_hour
import matplotlib.pyplot as plt
plt.close('all')

if __name__ == "__main__":
    wd_list = get_tmy(41.141816091983856, 25.891168951039393)
    print(wd_list)
    plot_mean_wd_per_hour(wd_list)