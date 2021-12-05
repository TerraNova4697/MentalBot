
workers = list()

# Ссылки на медитацию
meditation = ['https://www.youtube.com/watch?v=Ho91a_GwYxs',
              'https://www.youtube.com/watch?v=aXH-QsPTeEI',
              'https://www.youtube.com/watch?v=inpok4MKVLM',
              'https://www.youtube.com/watch?v=kndqIj8Qgok',
              'https://www.youtube.com/watch?v=qQXW6k86mwk',
              'https://www.youtube.com/watch?v=86m4RC_ADEY',
              'https://www.youtube.com/watch?v=1ZYbU82GVz4',
              'https://www.youtube.com/watch?v=2OEL4P1Rz04',
              'https://www.youtube.com/watch?v=O-6f5wQXSu8',
              'https://www.youtube.com/watch?v=X4WjbW6amQw',
              'https://www.youtube.com/watch?v=ez3GgRqhNvA',
              'https://www.youtube.com/watch?v=itZMM5gCboo',
              'https://www.youtube.com/watch?v=BG79IpCBJTk',
              'https://www.youtube.com/watch?v=4pLUleLdwY4',
              'https://www.youtube.com/watch?v=EwQkfoKxRvo',
              'https://www.youtube.com/watch?v=U9YKY7fdwyg',
              'https://www.youtube.com/watch?v=W19PdslW7iw']

# Ссылки на музыку, которая отправляется работникам
music = ['https://www.youtube.com/watch?v=vDYP6AKw8bk',
         'https://www.youtube.com/watch?v=ZVb_yKMivqo',
         'https://www.youtube.com/watch?v=sNOtS8YsdF8',
         'https://www.youtube.com/watch?v=AnlKTlJLkro',
         'https://www.youtube.com/watch?v=4zeUOUo09Hs',
         'https://www.youtube.com/watch?v=9UMxZofMNbA',
         'https://www.youtube.com/watch?v=JZ9GwwttpRU',
         'https://www.youtube.com/watch?v=tlUcmD0zPI4',
         'https://www.youtube.com/watch?v=_4kHxtiuML0',
         'https://www.youtube.com/watch?v=5ROdNY9lu0w']

# file_id всех аффирмаций, которые отправляются работникам
affirmations = ['AgACAgIAAxkBAAIHRmGsiOOV65UM9t0IFvnQ7Q9KbGYqAAJktzEbOrVgSascLnVsviPjAQADAgADeAADIgQ',
                'AgACAgIAAxkBAAIHR2GsiOcswvoGylhlV7e9uDYEexf2AAJntzEbOrVgSQwZTpLE1MhLAQADAgADeAADIgQ',
                'AgACAgIAAxkBAAIHSGGsiOtROjbXhvI7UjC_Qj9iLqCFAAJotzEbOrVgSRR8jcKWRULNAQADAgADeAADIgQ',
                'AgACAgIAAxkBAAIHSWGsiO-dTy0fwqLr-lDeo22T7NZmAAJptzEbOrVgSZWj4oM6OvjfAQADAgADeAADIgQ',
                'AgACAgIAAxkBAAIHSmGsiPMU4oprIc_BzH2wJZVPSPbMAAJrtzEbOrVgSTzNongVH4D9AQADAgADeAADIgQ',
                'AgACAgIAAxkBAAIHS2GsiPrhuyQz1z60IS800Kj8wb4XAAJstzEbOrVgSQl0aHdUHCGXAQADAgADeAADIgQ',
                'AgACAgIAAxkBAAIHTGGsiQABxDDjcmrirQvJgv4S1HkTeAACbrcxGzq1YEniRMlUipdvbQEAAwIAA3gAAyIE',
                'AgACAgIAAxkBAAIHTWGsiQPA7sBcYTxSU4Q53HPNaUe2AAJvtzEbOrVgSTGYGRxZ75nJAQADAgADeAADIgQ',
                'AgACAgIAAxkBAAIHTmGsiQjS2xSLQIhNsN7hFL_STgbUAAJwtzEbOrVgSbjTKmIQzWSAAQADAgADeAADIgQ',
                'AgACAgIAAxkBAAIHT2GsiQ7XhnursRV6pb_K6k_fgFqzAAJytzEbOrVgSdVbJi1VoNiZAQADAgADeAADIgQ',
                'AgACAgIAAxkBAAIHUGGsiRPE6OxsB0ZNos2kxZfnetHgAAJztzEbOrVgSTdIVIvXc6JqAQADAgADeAADIgQ',
                'AgACAgIAAxkBAAIHUWGsiRjLFiBlDqwOBpEgWxk-bGHWAAJ0tzEbOrVgSSsLSjhf1CobAQADAgADeAADIgQ',
                'AgACAgIAAxkBAAIHUmGsiR5i-PjnRqEVj5w17ReRXTyfAAJ1tzEbOrVgSTj9w2c3KbwPAQADAgADeAADIgQ',
                'AgACAgIAAxkBAAIHU2GsiSaG2P6sV6Fxrw1f2UScKPwOAAJ2tzEbOrVgSYqL9S9rCGnRAQADAgADeAADIgQ',
                'AgACAgIAAxkBAAIHVGGsiSyLiNTPHG7ojAQyJ3yf4ulwAAJ3tzEbOrVgSX5HhLDohA4nAQADAgADeAADIgQ',
                'AgACAgIAAxkBAAIHVWGsiTFtMUxFUJy_yhFnLDFUk21-AAJ4tzEbOrVgSdpYVo9vdSf7AQADAgADeAADIgQ',
                'AgACAgIAAxkBAAIHVmGsiTd0W4hrB8GzjTw8asmuRKbRAAJ5tzEbOrVgScenFCzlLuCKAQADAgADeAADIgQ',
                'AgACAgIAAxkBAAIHV2GsiTuEXoqM5dHhgT2u4QsQxPdyAAJ6tzEbOrVgSYgfJ5hWCziNAQADAgADeAADIgQ',
                'AgACAgIAAxkBAAIHWGGsiUJ7AWN3YfaU_E_1TNxTaPx0AAJ7tzEbOrVgSXz_N7VHuX_pAQADAgADeAADIgQ',
                'AgACAgIAAxkBAAIHWWGsiUjKFSm2xB140X3OgxT-cU_2AAJ8tzEbOrVgSQzFogxrXj9PAQADAgADeAADIgQ',
                'AgACAgIAAxkBAAIHWmGsiVGs2m19MKensfBxs9ZaGPS4AAJ9tzEbOrVgSSuZatHaavGnAQADAgADeAADIgQ',
                'AgACAgIAAxkBAAIHW2GsiVd6bs5Vae70KmV6GlAjp8eiAAJ-tzEbOrVgST1Ge613bzZ4AQADAgADeAADIgQ',
                'AgACAgIAAxkBAAIHXGGsiVzNFMUh-ObJVS8xNQnhEJ4yAAJ_tzEbOrVgSXidMIbHVL3OAQADAgADeAADIgQ',
                'AgACAgIAAxkBAAIHXWGsiWKU0Aj65Oyeh3u5m9JX7OOuAAKAtzEbOrVgSYntbvURQMudAQADAgADeAADIgQ',
                'AgACAgIAAxkBAAIHXmGsiWe1omDyLX3iM9-QGIiJG5f9AAKBtzEbOrVgSW-ggzPLPoawAQADAgADeAADIgQ',
                'AgACAgIAAxkBAAIHX2GsiWtsx5cYNqP6L3xXrBfreTg9AAKCtzEbOrVgSd6slJWYNMxlAQADAgADeAADIgQ',
                'AgACAgIAAxkBAAIHYGGsiW9HBoEqDujjRTmHYsgG4mCBAAKDtzEbOrVgSdZxrQvHaX2WAQADAgADeAADIgQ',
                'AgACAgIAAxkBAAIHYWGsiXfhliRWjzLSFRcpb-mhJVHkAAKEtzEbOrVgSeazWHkuiyhdAQADAgADeAADIgQ']



