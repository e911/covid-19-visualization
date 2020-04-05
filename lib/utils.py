import os
import csv
import datetime

import requests
from django.utils import timezone
from django_rq import job
from redis import Redis
from rq_scheduler import Scheduler

from covid.models import FetchedDataFiles, CountryModel, CovidDataModel


# deprecated function
# lib/dataFiles will not be updated from now on
# def fetch_data_from_github():
#     github_repo_api_url = 'https://api.github.com/repos/CSSEGISandData/COVID-19/contents/csse_covid_19_data/csse_covid_19_daily_reports/'
#     get_github_response = requests.get(github_repo_api_url)
#     parsed_files_queryset = FetchedDataFiles.objects.values_list('filename', flat=True)
#     for each in get_github_response.json():
#         filename = each['name']
#         if filename == '.gitignore' or filename == 'README.md' or filename in parsed_files_queryset:
#             continue
#         raw_content_url = each['download_url']
#         get_response_content = requests.get(raw_content_url).content.decode('utf-8')
#         get_content_row_list = csv.reader(get_response_content.splitlines(), delimiter=',')
#         rows_list = list(get_content_row_list)
#         with open(f'lib/dataFiles/csse_covid_19_daily_reports/{filename}', 'w', newline='') as csvfile:
#             data_writer = csv.writer(csvfile)
#             for each in rows_list:
#                 data_writer.writerow(each)
#     fetch_daily_reports()
#
#
# # for production only
# # @job('default')
# def fetch_daily_reports():
#     folder_path = os.getcwd() + "/lib/dataFiles/csse_covid_19_daily_reports"
#     file_lists = os.listdir(folder_path)
#     parsed_files_queryset = FetchedDataFiles.objects.values_list('filename', flat=True)
#     for filename in file_lists:
#         if filename not in parsed_files_queryset:
#             with open(os.path.join(folder_path, filename), 'r') as f:
#                 parse_csv = csv.reader(f, delimiter=",")
#                 count = 0
#                 header = []
#
#                 for each_row in parse_csv:
#                     if count == 0:
#                         header = each_row
#                         count += 1
#                         continue
#                     else:
#                         data = {}
#                         if header == ['FIPS', 'Admin2', 'Province_State', 'Country_Region', 'Last_Update', 'Lat',
#                                       'Long_', 'Confirmed', 'Deaths', 'Recovered', 'Active',
#                                       'Combined_Key'] or header == ['\ufeffFIPS', 'Admin2', 'Province_State',
#                                                                     'Country_Region', 'Last_Update', 'Lat', 'Long_',
#                                                                     'Confirmed', 'Deaths', 'Recovered', 'Active',
#                                                                     'Combined_Key']:
#                             data = parse_new_header(each_row)
#                         else:
#                             data = parse_old_header(each_row)
#                         country = CountryModel.objects.get_or_create(country=data['country'])
#                         try:
#                             covid_data = CovidDataModel.objects.get(country=country[0], date=data['date'].date())
#                             covid_data.confirmed_cases += int(data['confirmed_cases'])
#                             covid_data.deaths += int(data['deaths'])
#                             covid_data.recovered += int(data['recovered'])
#                             covid_data.save()
#                         except CovidDataModel.DoesNotExist:
#                             covid_data = CovidDataModel(country=country[0], date=data['date'].date(),
#                                                         datetime=data['date'],
#                                                         confirmed_cases=data['confirmed_cases'],
#                                                         deaths=data['deaths'], recovered=data['recovered'])
#                             covid_data.save()
#                         count += 1
#             parsed_files = FetchedDataFiles(filename=filename)
#             parsed_files.save()
#
#
# def parse_date(date):
#     try:
#         date = timezone.make_aware(datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S"),
#                                    timezone.get_default_timezone())
#         return date
#     except ValueError as error:
#         print(error)
#     try:
#         date = timezone.make_aware(
#             datetime.datetime.strptime(date, "%m/%d/%y %H:%M"),
#             timezone.get_default_timezone())
#         return date
#     except ValueError as e:
#         print(e)
#     try:
#         date = timezone.make_aware(
#             datetime.datetime.strptime(date, "%m/%d/%Y %H:%M"),
#             timezone.get_default_timezone())
#         return date
#     except ValueError as e:
#         print(e)
#     try:
#         date = timezone.make_aware(
#             datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S"),
#             timezone.get_default_timezone())
#         return date
#     except ValueError as e:
#         print(e)
#
#     return date
#
#
# def parse_old_header(each_row):
#     data = {}
#     city = each_row[0]
#     country = each_row[1]
#     if country == 'Iran (Islamic Republic of)':
#         country = 'Iran'
#     if country == 'Mainland China':
#         country = 'China'
#     try:
#         latitude = each_row[6] or 0
#         longitude = each_row[7] or 0
#     except IndexError as error:
#         print(error)
#         latitude = 0
#         longitude = 0
#     data.update(country=country)
#     data.update(date=parse_date(each_row[2]))
#     data.update(confirmed_cases=each_row[3] if each_row[3] != '' else 0)
#     data.update(deaths=each_row[4] if each_row[4] != '' else 0)
#     data.update(recovered=each_row[5] if each_row[5] != '' else 0)
#     data.update(latitude=latitude)
#     data.update(longitude=longitude)
#     return data
#
#
# def parse_new_header(each_row):
#     data = {}
#     city = each_row[2]
#     country = each_row[3]
#     if country == 'Iran (Islamic Republic of)':
#         country = 'Iran'
#     if country == 'Mainland China':
#         country = 'China'
#     try:
#         latitude = each_row[5] or 0
#         longitude = each_row[6] or 0
#     except IndexError as error:
#         print(error)
#         latitude = 0
#         longitude = 0
#     data.update(country=country)
#     data.update(date=parse_date(each_row[4]))
#     data.update(confirmed_cases=each_row[7] if each_row[7] != '' else 0)
#     data.update(deaths=each_row[8] if each_row[8] != '' else 0)
#     data.update(recovered=each_row[9] if each_row[9] != '' else 0)
#     data.update(latitude=latitude)
#     data.update(longitude=longitude)
#     return data


# def run_scheduler():
#     scheduler = Scheduler(connection=Redis(), queue_name='default')
#     scheduler.schedule(
#         scheduled_time=datetime.datetime.now(),  # Time for first execution, in UTC timezone
#         func=fetch_daily_reports,  # Function to be queued
#         interval=21600,  # Time before the function is called again, in seconds
#         repeat=1
#     )


def fetch_time_series_data_from_github():
    raw_content_time_series_github_files_list = [
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv',
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv']
    parsed_files_queryset = FetchedDataFiles.objects.values_list('filename', flat=True)
    file_index = 0
    for raw_content_url in raw_content_time_series_github_files_list:
        get_response_content = requests.get(raw_content_url).content.decode('utf-8')
        get_content_row_list = csv.reader(get_response_content.splitlines(), delimiter=',')
        rows_list = list(get_content_row_list)
        filename = raw_content_url.split('/')[-1]
        with open(f'lib/dataFiles/csse_covid_19_daily_reports/{filename}', 'w', newline='') as csvfile:
            data_writer = csv.writer(csvfile)
            for each in rows_list:
                data_writer.writerow(each)
        get_headers = rows_list[0]
        get_date_headers = get_headers[4::]
        get_remaining_date_headers = list(set(get_date_headers) - set(parsed_files_queryset))
        for each_rows in rows_list[1::]:
            index = 0
            country = CountryModel.objects.get_or_create(country=each_rows[1])
            for each_headers_date in get_remaining_date_headers:
                try:
                    covid_data = CovidDataModel.objects.get(country=country[0],
                                                               date=parse_time_series_date(each_headers_date))
                    if file_index == 0:
                        covid_data.confirmed_cases += int(each_rows[get_headers.index(each_headers_date)])
                    if file_index == 1:
                        covid_data.deaths += int(each_rows[get_headers.index(each_headers_date)])
                    if file_index == 2:
                        covid_data.recovered += int(each_rows[get_headers.index(each_headers_date)])
                    covid_data.save()
                    index += 1
                except CovidDataModel.DoesNotExist:
                    covid_data = CovidDataModel(country=country[0],
                                                   date=parse_time_series_date(each_headers_date).date(),
                                                   datetime=parse_time_series_date(each_headers_date),
                                                   confirmed_cases=int(each_rows[get_headers.index(each_headers_date)]))
                    covid_data.save()
                    index += 1
                if file_index == 2:
                    try:
                        fetched_data_file = FetchedDataFiles.objects.get(filename=each_headers_date)
                    except FetchedDataFiles.DoesNotExist:
                        parsed_files = FetchedDataFiles(filename=each_headers_date)
                        parsed_files.save()
        file_index += 1


def parse_time_series_date(date):
    try:
        date = timezone.make_aware(datetime.datetime.strptime(date, "%m/%d/%y"),
                                   timezone.get_default_timezone())
        return date
    except ValueError as error:
        print(error)
    return date
