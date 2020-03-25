import os
import csv
import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django_rq import job
from redis import Redis
from rq_scheduler import Scheduler

from covid.models import FetchedDataFiles, CountryModel, CovidDataModel


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
                header = []

                for each_row in parse_csv:
                    if count == 0:
                        header = each_row
                        count += 1
                        continue
                    else:
                        data = {}
                        if header == ['FIPS', 'Admin2', 'Province_State', 'Country_Region', 'Last_Update', 'Lat',
                                      'Long_', 'Confirmed', 'Deaths', 'Recovered', 'Active',
                                      'Combined_Key'] or header == ['\ufeffFIPS', 'Admin2', 'Province_State',
                                                                       'Country_Region', 'Last_Update', 'Lat', 'Long_',
                                                                       'Confirmed', 'Deaths', 'Recovered', 'Active',
                                                                       'Combined_Key']:
                            data = parse_new_header(each_row)
                        else:
                            data = parse_old_header(each_row)
                        country = CountryModel.objects.get_or_create(country=data['country'])
                        try:
                            covid_data = CovidDataModel.objects.get(country=country[0], date=data['date'].date())
                            covid_data.confirmed_cases += int(data['confirmed_cases'])
                            covid_data.deaths += int(data['deaths'])
                            covid_data.recovered += int(data['recovered'])
                            covid_data.save()
                        except CovidDataModel.DoesNotExist:
                            covid_data = CovidDataModel(country=country[0], date=data['date'].date(),
                                                        datetime=data['date'],
                                                        confirmed_cases=data['confirmed_cases'],
                                                        deaths=data['deaths'], recovered=data['recovered'])
                            covid_data.save()
                        count += 1
            parsed_files = FetchedDataFiles(filename=filename)
            parsed_files.save()


def parse_date(date):
    try:
        date = timezone.make_aware(datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S"),
                                   timezone.get_default_timezone())
        return date
    except ValueError as error:
        print(error)
    try:
        date = timezone.make_aware(
            datetime.datetime.strptime(date, "%m/%d/%y %H:%M"),
            timezone.get_default_timezone())
        return date
    except ValueError as e:
        print(e)
    try:
        date = timezone.make_aware(
            datetime.datetime.strptime(date, "%m/%d/%Y %H:%M"),
            timezone.get_default_timezone())
        return date
    except ValueError as e:
        print(e)
    try:
        date = timezone.make_aware(
            datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S"),
            timezone.get_default_timezone())
        return date
    except ValueError as e:
        print(e)

    return date


def parse_old_header(each_row):
    data = {}
    city = each_row[0]
    country = each_row[1]
    if country == 'Iran (Islamic Republic of)':
        country = 'Iran'
    if country == 'Mainland China':
        country = 'China'
    try:
        latitude = each_row[6] or 0
        longitude = each_row[7] or 0
    except IndexError as error:
        print(error)
        latitude = 0
        longitude = 0
    data.update(country=country)
    data.update(date=parse_date(each_row[2]))
    data.update(confirmed_cases=each_row[3] if each_row[3] != '' else 0)
    data.update(deaths=each_row[4] if each_row[4] != '' else 0)
    data.update(recovered=each_row[5] if each_row[5] != '' else 0)
    data.update(latitude=latitude)
    data.update(longitude=longitude)
    return data


def parse_new_header(each_row):
    data = {}
    city = each_row[2]
    country = each_row[3]
    if country == 'Iran (Islamic Republic of)':
        country = 'Iran'
    if country == 'Mainland China':
        country = 'China'
    try:
        latitude = each_row[5] or 0
        longitude = each_row[6] or 0
    except IndexError as error:
        print(error)
        latitude = 0
        longitude = 0
    data.update(country=country)
    data.update(date=parse_date(each_row[4]))
    data.update(confirmed_cases=each_row[7] if each_row[7] != '' else 0)
    data.update(deaths=each_row[8] if each_row[8] != '' else 0)
    data.update(recovered=each_row[9] if each_row[9] != '' else 0)
    data.update(latitude=latitude)
    data.update(longitude=longitude)
    return data

# def run_scheduler():
#     scheduler = Scheduler(connection=Redis(), queue_name='default')
#     scheduler.schedule(
#         scheduled_time=datetime.datetime.now(),  # Time for first execution, in UTC timezone
#         func=fetch_daily_reports,  # Function to be queued
#         interval=21600,  # Time before the function is called again, in seconds
#         repeat=1
#     )
