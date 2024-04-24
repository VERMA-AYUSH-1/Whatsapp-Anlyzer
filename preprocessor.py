import re
import pandas as pd

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    messages = re.split(pattern, data)
    messages = messages[2:]

    dates = re.findall(pattern, data)
    dates = dates[1:]

    df = pd.DataFrame({'User-Message': messages, 'Message_Date': dates})
    try:
        df['Message_Date'] = pd.to_datetime(df['Message_Date'], format="%d/%m/%y, %H:%M - ")
    except:
        df['Message_Date'] = pd.to_datetime(df['Message_Date'], format="%m/%d/%y, %H:%M - ")
    df.rename(columns={'Message_Date': 'Date'}, inplace=True)

    users = []
    msgs = []
    for message in df['User-Message']:
        temp = message.split(':', maxsplit=1)
        if len(temp) > 1:
            users.append(temp[0])
            msgs.append(temp[1])
    df['Users'] = users
    df['Messages'] = msgs
    df = df[df['Users'] != 'Group-Notification']

    df['Year'] = df['Date'].dt.year
    df['Month_num'] = df['Date'].dt.month
    df['Month'] = df['Date'].dt.month_name()
    df['Only_date'] = df['Date'].dt.date
    df['Day'] = df['Date'].dt.day
    df['Day_name'] = df['Date'].dt.day_name()
    df['Hours'] = df['Date'].dt.hour
    df['Minutes'] = df['Date'].dt.minute

    period = []
    for hour in df[['Day_name', 'Hours']]['Hours']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df
