import os
import csv
import datetime

from django_rq import job
from redis import Redis
from rq_scheduler import Scheduler

from covid.models import FetchedDataFiles, CountryModel, CovidDataModel


@job('default')
def fetch_daily_reports():
    folder_path = os.getcwd() + "/lib/dataFiles/csse_covid_19_daily_reports"
    file_lists = os.listdir(folder_path)
    parsed_files_queryset = FetchedDataFiles.objects.values_list('filename', flat=True)
    for filename in file_lists:
        if filename not in parsed_files_queryset:
            with open(os.path.join(folder_path, filename), 'r') as f:
                parse_csv = csv.reader(f, delimiter=",")
                count = 0
                for each_row in parse_csv:
                    if count == 0:
                        count += 1
                        continue
                    else:
                        state = each_row[0]
                        country = each_row[1]
                        if country == 'Iran (Islamic Republic of)':
                            country = 'Iran'
                        if country == 'Mainland China':
                            country = 'China'
                        try:
                            date = datetime.datetime.strptime(each_row[2], "%Y-%m-%dT%H:%M:%S")
                        except ValueError as error:
                            print(error)
                            try:
                                date = datetime.datetime.strptime(each_row[2], "%m/%d/%y %H:%M")
                            except ValueError as e:
                                print(e)
                                date = datetime.datetime.strptime(each_row[2], "%m/%d/%Y %H:%M")
                        confirmed_cases = each_row[3] if each_row[3] != '' else 0
                        deaths = each_row[4] if each_row[4] != '' else 0
                        recovered = each_row[5] if each_row[5] != '' else 0
                        try:
                            latitude = each_row[6] or 0
                            longitude = each_row[7] or 0
                        except IndexError as error:
                            print(error)
                            latitude = 0
                            longitude = 0
                        country = CountryModel.objects.get_or_create(country=country)
                        covid_data = CovidDataModel(country=country[0], date=date, confirmed_cases=confirmed_cases,
                                                    deaths=deaths, recovered=recovered, state=state, latitude=latitude,
                                                    longitude=longitude)
                        covid_data.save()
                        count += 1
            parsed_files = FetchedDataFiles(filename=filename)
            parsed_files.save()


def run_scheduler():
    scheduler = Scheduler(connection=Redis(), queue_name='default')
    scheduler.schedule(
        scheduled_time=datetime.datetime.now(),  # Time for first execution, in UTC timezone
        func=fetch_daily_reports,  # Function to be queued
        interval=21600,  # Time before the function is called again, in seconds
        repeat=0
    )
