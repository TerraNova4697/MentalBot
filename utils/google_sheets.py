import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

from data.variables import workers

def get_month(i: int):
    months = {1: "Январь", 2: "Февраль", 3: "Март", 4: "Апрель",
              5: "Май", 6: "Июнь", 7: "Июль", 8: "Август",
              9: "Сентябрь", 10: "Октябрь", 11: "Ноябрь", 12: "Декабрь"}
    return months[i]

CREDENTIALS_FILE = 'ultra-optics-334613-834dd2281452.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                               ['https://www.googleapis.com/auth/spreadsheets',
                                                                'https://www.googleapis.com/auth/drive'])

httpAuth = credentials.authorize(httplib2.Http())
service = googleapiclient.discovery.build('sheets', 'v4', http=httpAuth)
spreadsheetId = '1li-wubGJPLn1zfrtxKOzBLvhrwIpUPD87KFDo69oTXE'


def create_table():
    spreadsheet = service.spreadsheets().create(body={
        'properties': {'title': 'Статистика', 'locale': 'ru_RU'},
        'sheets': [{'properties': {'sheetType': 'GRID',
                                   'sheetId': 0,
                                   'title': 'Декабрь 2021',
                                   'gridProperties': {'rowCount': 2, 'columnCount': 3}}}]
    }).execute()
    spreadsheetId = spreadsheet['spreadsheetId']
    print('https://docs.google.com/spreadsheets/d/' + spreadsheetId)


def update_table(sheetName, count, only_ones, average):
    results = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId, body={
        "valueInputOption": "USER_ENTERED",
        # Данные воспринимаются, как вводимые пользователем (считается значение формул)
        "data": [
            {"range": f"{sheetName}!A2:C2",
             "majorDimension": "ROWS",  # Сначала заполнять строки, затем столбцы
             "values": [
                 [f'{count}', f"{only_ones}", f"{average}"]  # Заполняем вторую строку
             ]}
        ]
    }).execute()


def give_access(email: str):
    driveService = googleapiclient.discovery.build('drive', 'v3',
                                                   http=httpAuth)  # Выбираем работу с Google Drive и 3 версию API
    access = driveService.permissions().create(
        fileId=spreadsheetId,
        body={'type': 'user', 'role': 'writer', 'emailAddress': email},
        # Открываем доступ на редактирование
        fields='id'
    ).execute()


def create_list(name: str):
    results = service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheetId,
        body=
        {
            "requests": [
                {
                    "addSheet": {
                        "properties": {
                            "title": name,
                            "gridProperties": {
                                "rowCount": 2,
                                "columnCount": 3
                            }
                        }
                    }
                }
            ]
        }).execute()

    results2 = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId, body={
        "valueInputOption": "USER_ENTERED",
        # Данные воспринимаются, как вводимые пользователем (считается значение формул)
        "data": [
            {"range": f"{name}!A1:C1",
             "majorDimension": "ROWS",  # Сначала заполнять строки, затем столбцы
             "values": [
                 ["Кол-во сотрудников, которые прошли опрос в этом месяце",
                  "Процент из общего числа сотрудников прошли тест только 1 раз",
                  "Средний показатель эмоционального состояния всех сотрудников"],  # Заполняем первую строку
             ]}
        ]
    }).execute()

    spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheetId).execute()
    sheetList = spreadsheet.get('sheets')
    sheetId = sheetList[-1]["properties"]["sheetId"]

    results3 = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body={
        "requests": [

            # Задать ширину столбца A: 20 пикселей
            {
                "updateDimensionProperties": {
                    "range": {
                        "sheetId": sheetId,
                        "dimension": "COLUMNS",  # Задаем ширину колонки
                        "startIndex": 0,  # Нумерация начинается с нуля
                        "endIndex": 3  # Со столбца номер startIndex по endIndex - 1 (endIndex не входит!)
                    },
                    "properties": {
                        "pixelSize": 200  # Ширина в пикселях
                    },
                    "fields": "pixelSize"  # Указываем, что нужно использовать параметр pixelSize
                }
            }
        ]
    }).execute()

    results4 = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body={
        "requests": [
            {
                "updateCells": {
                    "rows": {
                        "values": {
                            "userEnteredFormat": {
                                "wrapStrategy": "WRAP"
                            }
                        }
                    },
                    "fields": 'userEnteredFormat.wrapStrategy',
                    "range": {
                        "sheetId": sheetId,
                        "startRowIndex": 0,  # Нумерация начинается с нуля
                        "startColumnIndex": 0,
                    }
                }
            }
        ]
    }).execute()

    results4 = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body={
        "requests": [
            {
                "updateCells": {
                    "rows": {
                        "values": {
                            "userEnteredFormat": {
                                "wrapStrategy": "WRAP"
                            }
                        }
                    },
                    "fields": 'userEnteredFormat.wrapStrategy',
                    "range": {
                        "sheetId": sheetId,
                        "startRowIndex": 0,  # Нумерация начинается с нуля
                        "startColumnIndex": 1,
                    }
                }
            }
        ]
    }).execute()

    results4 = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body={
        "requests": [
            {
                "updateCells": {
                    "rows": {
                        "values": {
                            "userEnteredFormat": {
                                "wrapStrategy": "WRAP"
                            }
                        }
                    },
                    "fields": 'userEnteredFormat.wrapStrategy',
                    "range": {
                        "sheetId": sheetId,
                        "startRowIndex": 0,  # Нумерация начинается с нуля
                        "startColumnIndex": 2,
                    }
                }
            }
        ]
    }).execute()


def update_statistics(answers, month, year):

    avr_values: float = 0.0
    workers_list = list()
    how_many_tests = dict()
    for answer in answers:
        avr_values += float(answer[11])
        if answer[1] not in workers_list:
            workers_list.append(answer[1])
        if answer[1] not in how_many_tests:
            how_many_tests[answer[1]] = 1
        else:
            how_many_tests[answer[1]] += 1
    only_ones = 0
    for key in how_many_tests:
        if how_many_tests[key] == 1:
            only_ones += 1
    percent = "%.1f" % (only_ones*100/len(workers)) + "%"
    avr_values /= len(answers)
    worker_count = len(workers_list)
    avr_values_str = "%.1f" % avr_values + "/5.0"

    sheetName = f"{get_month(month)} {str(year)}"

    try:
        update_table(sheetName, str(worker_count), str(percent), avr_values_str)
    except Exception as err:
        create_list(sheetName)
        update_table(sheetName, str(worker_count), str(percent), avr_values_str)


if __name__ == "__main__":
    create_table()
