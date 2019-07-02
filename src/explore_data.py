import os
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt


def parse_data(input_file: str):
    """Takes the csv file and returns a pandas dataframe with headers"""

    csv_data = pd.read_csv(input_file)

    # Assuming the first column is date, convert that to python datetime class
    csv_data['Date'] = pd.to_datetime(csv_data['Date'], dayfirst=True)

    # Add all column values for each row to give cumulative amount
    csv_data['Cumulative'] = csv_data.sum(axis=1)

    return csv_data


def trend_plots(input_data, show=True, save=False, fig_num=1, y_label='Reservoir level',
                save_location=os.path.join('plots', ''), save_name='plot.pdf'):
    """Takes the data frame and plots all the trend lines"""

    sb.set(style='darkgrid')

    # Plot the data from each reservoir
    plt.figure(fig_num)
    plot_handle = plt.gca()

    reservoir_names = list(input_data)
    for reservoir in reservoir_names[1:-1]:
        sb.lineplot(x='Date', y=reservoir, data=input_data)

    plt.legend(reservoir_names[1:-1], bbox_to_anchor=(1, 1), loc='lower right', ncol=2)
    plot_handle.set_title('Time vs ' + y_label)
    plot_handle.set(xlabel='Date (in years)', ylabel=y_label + ' (in mil. cu.ft.)')
    # plot_handle.set_xticklabels(rotation=30)

    if show:
        plt.show(fig_num)

    if save:
        plt.savefig(os.path.join(save_location, save_name), bbox_inches='tight')

    plt.close(fig_num)

    return plot_handle


def individual_comparison(levels_data, rain_data, show=True, save=False,
                          fig_num=1, save_location=os.path.join('plots', '')):
    """comparison between rainfall received and reservoir level for each reservoir"""

    sb.set(style='darkgrid')

    # Plot the data from each reservoir
    plot_handles = []

    reservoir_names = list(levels_data)
    for reservoir in reservoir_names[1:]:
        plt.figure(fig_num)
        current_plot = plt.gca()
        plot_handles.append(current_plot)
        sb.lineplot(x='Date', y=reservoir, data=levels_data)
        sb.lineplot(x='Date', y=reservoir, data=rain_data)

        plt.legend(['Level', 'Rainfall'], bbox_to_anchor=(1, 1), loc='lower right', ncol=1)
        current_plot.set_title('Time vs ' + reservoir + ' levels')
        current_plot.set(xlabel='Date (in years)', ylabel=reservoir + ' (in mil. cu.ft.)')

        if show:
            plt.show(fig_num)

        if save:
            plt.savefig(os.path.join(save_location, reservoir + '.pdf'), bbox_inches='tight')

        plt.close(fig_num)
        fig_num += 1

    return plot_handles


if __name__ == '__main__':
    reservoir_levels = parse_data(os.path.join('data', 'chennai_reservoir_levels.csv'))
    reservoir_rainfall = parse_data(os.path.join('data', 'chennai_reservoir_rainfall.csv'))

    reservoir_level_plot = trend_plots(reservoir_levels, show=False,
                                       save=True, save_name='levels.pdf')
    reservoir_rainfall_plot = trend_plots(reservoir_rainfall, show=False, y_label='Reservoir rainfall',
                                          fig_num=2, save=True, save_name='rainfall.pdf')

    reservoir_comparisons = individual_comparison(reservoir_levels, reservoir_rainfall, show=False,
                                                  save=True, fig_num=3)
