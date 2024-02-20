import streamlit as st
import function
import preprocessing
import matplotlib.pyplot as plt
# import seaborn as sns
import plotly.express as px
import warnings
warnings.filterwarnings('ignore')
import pandas as pd

#Set page title and favicon
st.set_page_config(page_title="WhatsApp Chat Analyzer", page_icon=":speech_balloon:")

#Slidebar title
st.sidebar.title("Whatsapp Chat Analyzer")

search_word = st.sidebar.text_input("Search for a word")


#File Upload
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df=preprocessing.preprocess(data)

    #showing the dataframe
    # st.dataframe(df)

    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user=st.sidebar.selectbox("Show the analysis wrt ",user_list)

    if st.sidebar.button("Show Analysis"):
        
        total_message,words,num_media_message,links=function.fetch_stats(selected_user,df)

        st.title("Top Statistics")

        col1,col2,col3,col4=st.columns(4)

        with col1:
            st.metric("Total Messages", total_message)
        with col2:
            st.metric("Total Words", words)
        with col3:
            st.metric("Media Shared", num_media_message)
        with col4:
            st.metric("Links Shared", links)

        #Monthly Timeline
        st.title("Monthly Timeline")
        timeline = function.monthly_timeline(selected_user, df)
        fig = px.line(timeline, x='time', y='message', title='Monthly Message Count')
        st.plotly_chart(fig)

        #Daily Timeline
        st.title("Daily Timeline")
        daily_timeline = function.daily_timeline(selected_user, df)
        fig = px.line(daily_timeline, x='only_date', y='message', title='Daily Message Count')
        st.plotly_chart(fig)

        # Activity Map according to days
        st.title("Activity Map")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Most Active Days")
            busy_day = function.week_activity(selected_user, df)
            fig = px.bar(busy_day, x=busy_day.index, y=busy_day.values, labels={'x': 'Day', 'y': 'Message Count'})
            st.plotly_chart(fig)
        with col2:
            st.subheader("Most Active Months")
            busy_month = function.month_activity(selected_user, df)
            fig = px.bar(busy_month, x=busy_month.index, y=busy_month.values, labels={'x': 'Month', 'y': 'Message Count'})
            st.plotly_chart(fig)

        # Most Busy User (if selected user is Overall)
        if selected_user == "Overall":
            st.title("Most Active Users")
            busy_users = function.most_busy_user(df)
            st.bar_chart(busy_users)

        # Weekly Activity Map
        # st.title("Weekly Activity Map")
        # user_heatmap = function.activity_heatmap(selected_user,df)
        # fig,ax = plt.subplots()
        # ax = sns.heatmap(user_heatmap)
        # st.pyplot(fig)

        # WordCloud
        st.title("WordCloud")
        df_wc = function.create_wordcloud(selected_user, df)
        st.image(df_wc.to_image())

        # Most Common Words
        st.title("Most Common Words")
        most_common_df = function.most_commoon_words(selected_user, df)
        st.dataframe(most_common_df)

        # Emoji Analysis
        st.title("Emoji Analysis")
        emoji_df = function.emoji_used(selected_user, df)
        fig = px.pie(emoji_df.head(10), values=1, names=0, title='Emoji Usage')
        st.plotly_chart(fig)

        # Search functionality
        if search_word:
            word_counts = df[df['message'].str.contains(search_word, case=False)]['user'].value_counts()
            st.title(f"Occurrences of Word '{search_word}'")
            st.write(f"The word '{search_word}' appeared {word_counts.sum()} times in the chat.")
            if not word_counts.empty:
                st.write("Occurrences by user:")
                # Beautiful DataFrame
                styled_df = pd.DataFrame({"User": word_counts.index, "Occurrences": word_counts.values}).style.bar(subset=["Occurrences"], color='#d65f5f')
                st.dataframe(styled_df)
