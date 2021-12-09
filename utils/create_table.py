import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

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

    driveService = googleapiclient.discovery.build('drive', 'v3',
                                                   http=httpAuth)  # Выбираем работу с Google Drive и 3 версию API
    access = driveService.permissions().create(
        fileId=spreadsheetId,
        body={'type': 'user', 'role': 'writer', 'emailAddress': "nikitabechthold@gmail.com"},
        # Открываем доступ на редактирование
        fields='id'
    ).execute()


def update_table():
    results2 = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId, body={
        "valueInputOption": "USER_ENTERED",
        # Данные воспринимаются, как вводимые пользователем (считается значение формул)
        "data": [
            {"range": "Декабрь 2021!A1:C1",
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


if __name__ == "__main__":
    update_table()
