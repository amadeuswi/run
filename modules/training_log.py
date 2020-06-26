from typing import List, Tuple

from config import M_TO_KM
import matplotlib.pyplot as plt
import numpy as np
from modules.effort import WEEKDAYS, Effort
from modules.folder import get_gpx_list
import datetime

FILE_ENDING = 'gpx'


class TrainingLog:
    """ Class for training logs. """

    def __init__(self, year: int, root_path_list: List[str]):
        self.year = year
        self.__gpx_list = get_gpx_list(root_path_list, FILE_ENDING, self.year)
        self.all_efforts_list, self.single_effort_list, self.multi_effort_list = self.__get_effort_list()
        self.max_duration = max([effort.duration for effort in self.all_efforts_list])
        self.first_week_number = min([effort.week_number for effort in self.all_efforts_list])
        self.last_week_number = max([effort.week_number for effort in self.all_efforts_list])

    def get_weekly_totals(self) -> List[float]:
        weekly_totals = []
        for week_number in range(self.first_week_number, self.last_week_number + 1):
            total = np.sum([np.around(effort.distance * M_TO_KM)
                            for effort in self.all_efforts_list if effort.week_number == week_number])
            weekly_totals.append(total)
        return weekly_totals

    def plot_calendar(self, plot_path):
        figsize_height = int(round(8 * (self.last_week_number - self.first_week_number) / 5))
        figsize_width = 8
        _, ax = plt.subplots(1, figsize=(figsize_width, figsize_height))

        for effort in self.single_effort_list:
            ax.scatter(
                effort.weekday_number,
                effort.week_number,
                color='white',
                facecolors='black',
                alpha=0.3,
                marker='o',
                s=3000 * effort.duration / self.max_duration
                )
            ax.text(
                effort.weekday_number - 0.2,
                effort.week_number,
                '{0:10.0f}'.format(effort.distance / 1000),
                ha='center',
                va='center',
                color='black'
                )

        for effort_day_list in self.multi_effort_list:
            day_duration = sum([effort.duration for effort in effort_day_list])
            day_distance = sum([effort.distance for effort in effort_day_list])
            ax.scatter(
                effort_day_list[0].weekday_number,
                effort_day_list[0].week_number,
                color='white',
                facecolors='black',
                alpha=0.3,
                marker='s',
                s=3000 * day_duration / self.max_duration
                )
            ax.text(
                effort_day_list[0].weekday_number - 0.2,
                effort_day_list[0].week_number,
                '{0:10.0f}'.format(day_distance / 1000),
                ha='center',
                va='center',
                color='black'
                )

        # weekly mileage:
        for i, week_number in enumerate(range(self.first_week_number, self.last_week_number + 1)):
            week_mileage = int(np.around(self.get_weekly_totals()[i]))
            ax.text(7.8, week_number - 0.1, f'{week_mileage} km', weight='bold')

        # ticks and labels:
        weekday_labels = [weekday for weekday in WEEKDAYS]
        ax.set_xticks(range(1,8))
        ax.set_xticklabels(weekday_labels)
        ax.set_yticks(range(self.first_week_number, self.last_week_number + 1))
        weeknumber_labels = [
            f'{self.get_date_from_week(weeknumber, self.year)}' for weeknumber in range(
                self.first_week_number,
                self.last_week_number + 1)]
        ax.set_yticklabels(weeknumber_labels)

        # vertical line separator:
        ax.axvline(7.5, color='black', lw=0.5)

        ax.set_xlim((0.0, 8.))
        ax.set_ylim((self.first_week_number - 0.5, self.last_week_number + 0.5))

        # get rid of the frame
        for spine in plt.gca().spines.values():
            spine.set_visible(False)

        # remove all ticks
        ax.xaxis.set_ticks_position('none')
        ax.yaxis.set_ticks_position('none')

        plt.tight_layout()

        plt.savefig(plot_path)

    def __get_effort_list(self) -> Tuple[List[Effort], List[Effort], List[List[Effort]]]:
        effort_list = [Effort(gpx) for gpx in self.__gpx_list]
        effort_list_without_duplicates = self.__get_efforts_without_duplicates(effort_list)
        single_day, multi_day = self.__get_effort_list_split(effort_list_without_duplicates)
        return effort_list_without_duplicates, single_day, multi_day

    def __get_efforts_without_duplicates(self, effort_list: List[Effort]) -> List[Effort]:
        result = []
        for effort in effort_list:
            if effort not in result:
                result.append(effort)
        return result

    def __get_effort_list_split(self, effort_list: List[Effort]) -> Tuple[List[Effort], List[List[Effort]]]:
        """ Returns the effort list split into efforts on single effort days and efforts on multiple effort days. """
        multi_date_list = self.__get_multi_effort_date_list(effort_list)
        single_effort_list = [] # one effort per day
        multi_effort_list = [[] for _ in range(len(multi_date_list))] # multiple efforts per day
        for effort in effort_list:
            date = (effort.year, effort.week_number, effort.weekday_number)
            if date in multi_date_list:
                idx = multi_date_list.index(date)
                multi_effort_list[idx].append(effort)
            else:
                single_effort_list.append(effort)
        return single_effort_list, multi_effort_list 
        # TODO: make a list of total efforts on a day by adding + operator to ``Effort``

    def __get_multi_effort_date_list(self, effort_list: List[Effort]) -> List[Tuple[int, int, int]]:
        """ Returns the list of dates where multiple efforts have been made. """
        multi_date_list = []  # multiple efforts per day
        date_list = []  # all dates
        for effort in effort_list:
            date = (effort.year, effort.week_number, effort.weekday_number)
            if date in date_list and date not in multi_date_list:
                multi_date_list.append(date)
            date_list.append(date)
        return multi_date_list

    @staticmethod
    def get_date_from_week(week_number, year):
        """ Returns the date of Monday in the given week and year. """
        date_string = f'{year}-W{week_number-1}'
        week_date = datetime.datetime.strptime(date_string + '-1', "%Y-W%W-%w")
        return week_date.strftime('%d %b')
