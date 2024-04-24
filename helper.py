import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import emoji
from urlextract import URLExtract

extractor = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]

    num_messages = df.shape[0]

    words = []
    for message in df['Messages']:
        words.extend(message.split(' '))

    num_media_msgs = sum('Media omitted' in message for message in df['Messages'])

    urls = []
    for message in df['Messages']:
        url = extractor.find_urls(message)
        urls.extend(url)

    return num_messages, len(words), num_media_msgs, len(urls)


def most_busy_user(df):
    name = df['Users'].value_counts().head().index
    count = df['Users'].value_counts().head().values
    new_df = round((df['Users'].value_counts()/df.shape[0])*100,2).reset_index()
    return name, count, new_df


def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]

    wc = WordCloud(height=500, width=500, min_font_size=2, background_color='white')
    df_wc = wc.generate(df['Messages'].str.cat(sep=" "))
    return df_wc


def most_used_words(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]

    temp = df[df['Users'] != 'Group-Notification']

    words = []
    for message in temp['Messages']:
        for word in message.lower().split():
            if word != '╬═╬' and word not in stop_words:
                words.append(word)

    most_used_word_df = pd.DataFrame(Counter(words).most_common(20))
    return most_used_word_df


def most_used_emojis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]

    emojis = []
    for message in df['Messages']:
        lst = []
        val = list(emoji.analyze(message))
        for i in range(len(val)):
            lst.append(val[i][0])
        if len(lst) > 0: emojis.extend(lst)

    most_used_emojis_df = pd.DataFrame(Counter(emojis).most_common(10))
    return most_used_emojis_df


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]

    monthly_timeline_df = df.groupby(['Year', 'Month', 'Month_num']).count()['Messages'].reset_index()
    time = [f"{row['Month']}-{row['Year']}" for index, row in monthly_timeline_df.iterrows()]
    monthly_timeline_df['Time'] = time
    return monthly_timeline_df


def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]

    daily_timeline_df = df.groupby(['Only_date']).count()['Messages'].reset_index()
    return daily_timeline_df


def monthly_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]

    monthly_activity_df = df.groupby(['Month']).count()['Messages'].reset_index()
    return monthly_activity_df


def daily_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]

    daily_activity_df = df.groupby(['Day_name']).count()['Messages'].reset_index()
    return daily_activity_df


def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]

    user_heatmap = df.pivot_table(index='Day_name', columns='period', values='Messages', aggfunc='count').fillna(0)
    return user_heatmap
