import os
import csv
import datetime

from django.utils import timezone
from django_rq import job
from redis import Redis
from rq_scheduler import Scheduler

from covid.models import FetchedDataFiles, CountryModel, CovidDataModel, CityModel

# for production only
# @job('default')
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
                        city = each_row[0]
                        country = each_row[1]
                        if country == 'Iran (Islamic Republic of)':
                            country = 'Iran'
                        if country == 'Mainland China':
                            country = 'China'
                        if city == 'Washington, D.C.':
                            city = 'Washington'
                        if city == 'Virgin Islands, U.S.':
                            city = 'Virgin Islands'
                        if city =='Travis, CA (From Diamond Princess)':
                            city = 'Travis, CA'
                        try:
                            date = timezone.make_aware(datetime.datetime.strptime(each_row[2], "%Y-%m-%dT%H:%M:%S"), timezone.get_default_timezone())
                        except ValueError as error:
                            print(error)
                            try:
                                date = timezone.make_aware(datetime.datetime.strptime(each_row[2], "%m/%d/%y %H:%M"), timezone.get_default_timezone())
                            except ValueError as e:
                                print(e)
                                date = timezone.make_aware(datetime.datetime.strptime(each_row[2], "%m/%d/%Y %H:%M"), timezone.get_default_timezone())
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
                        city = CityModel.objects.get_or_create(country=country[0], city=city)
                        covid_data = CovidDataModel(country=country[0], city=city[0], date=date, confirmed_cases=confirmed_cases,
                                                    deaths=deaths, recovered=recovered)
                        covid_data.save()
                        count += 1
            parsed_files = FetchedDataFiles(filename=filename)
            parsed_files.save()


# def run_scheduler():
#     scheduler = Scheduler(connection=Redis(), queue_name='default')
#     scheduler.schedule(
#         scheduled_time=datetime.datetime.now(),  # Time for first execution, in UTC timezone
#         func=fetch_daily_reports,  # Function to be queued
#         interval=21600,  # Time before the function is called again, in seconds
#         repeat=1
#     )
