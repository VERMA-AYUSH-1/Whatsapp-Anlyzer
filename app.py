import streamlit as st
import preprocessor
import helper

import matplotlib.pyplot as plt
import seaborn as sns

st. set_page_config(layout="wide")
st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")

st.title("Welcome to the Whatsapp Chat Analyzer !!")
st.markdown("#### Please select a file to continue")

if uploaded_file is not None:

    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    df = preprocessor.preprocess(data)

    user_list = df['Users'].unique().tolist()
    user_list.remove('Group-Notification')
    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user = st.sidebar.selectbox("Show Analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):

        num_messages, words, num_media_msgs, num_shared_links = helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Total Media Shared")
            st.title(num_media_msgs)

        with col4:
            st.header("Total Links Shared")
            st.title(num_shared_links)

        st.header("Monthly Timeline")
        monthly_timeline_df = helper.monthly_timeline(selected_user, df)
        plt.figure(figsize=(10,6))
        fig, ax1 = plt.subplots()
        ax1.plot(monthly_timeline_df['Time'], monthly_timeline_df['Messages'], color='purple')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.header("Daily Timeline")
        daily_timeline_df = helper.daily_timeline(selected_user, df)
        plt.figure(figsize=(30,10))
        fig, ax2 = plt.subplots()
        ax2.plot(daily_timeline_df['Only_date'], daily_timeline_df['Messages'], color='aqua')
        plt.xticks(rotation=40)
        st.pyplot(fig)

        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Monthly Activity Map")
            monthly_activity_df = helper.monthly_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(monthly_activity_df['Month'], monthly_activity_df['Messages'], color='crimson')
            plt.xticks(rotation=40)
            st.pyplot(fig)

        with col2:
            st.header("Daily Activity Map")
            daily_activity_df = helper.daily_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(daily_activity_df['Day_name'], daily_activity_df['Messages'], color='orange')
            plt.xticks(rotation=40)
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        if selected_user == 'Overall':
            st.title('Most Busy User')
            col1, col2 = st.columns(2)

            name, count, new_df = helper.most_busy_user(df)

            with col1:
                st.header("Busiest Users")
                fig, ax = plt.subplots()
                ax.bar(name, count, color='pink')
                plt.xlabel('Users')
                plt.ylabel('No. of Msgs')
                plt.xticks(rotation=40)
                st.pyplot(fig)

            with col2:
                st.header("Msgs Percentage")
                new_df = new_df.rename(columns={'Users': 'Username', 'count': 'Percentage'})
                st.dataframe(new_df)

        st.title("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        st.title("Most Used Words")
        most_used_words_df = helper.most_used_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_used_words_df[0], most_used_words_df[1])
        plt.xticks(rotation=10)
        st.pyplot(fig)

        col1, col2 = st.columns(2)

        with col1:
            st.title("Most used emojis")
            most_used_emojis_df = helper.most_used_emojis(selected_user, df)
            st.dataframe(most_used_emojis_df)

        with col2:
            st.title("Emoji Pie Chart")
            fig,ax = plt.subplots()
            ax.pie(most_used_emojis_df[1].head(), labels=most_used_emojis_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)
