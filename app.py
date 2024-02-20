import streamlit as st
import function
import preprocessing
import matplotlib.pyplot as plt
import pandas as pd
# import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

st.sidebar.title("Whatsapp Chat Analyzer")

search_word = st.sidebar.text_input("Search for a word")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df=preprocessing.preprocess(data)

    #showing the dataframe
    # st.dataframe(df)

    if 'group_notification' in df['user'].unique():
        user_list = df['user'].unique().tolist()
        user_list.remove('group_notification')
        user_list.sort()
        user_list.insert(0, "Overall")
    else:
        user_list = df['user'].unique().tolist()
        user_list.sort()
        user_list.insert(0, "Overall")

    selected_user=st.sidebar.selectbox("Show the analysis wrt ",user_list)

    if st.sidebar.button("Show Analysis"):
        
        total_message,words,num_media_message,links=function.fetch_stats(selected_user,df)

        st.title("Top Statistics")

        col1,col2,col3,col4=st.columns(4)

        with col1:
            st.header("Total Messages:")
            st.title(total_message)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_message)
        with col4:
            st.header("Link Shared")
            st.title(links)

        #Monthly Timeline
        st.title("Monthly Timeline")
        timeline=function.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color="green")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        #Daily Timeline
        st.title("Daily Timeline")
        daily_timeline=function.daily_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['message'],color="black")
        plt.xticks(rotation="vertical")
        st.pyplot(fig)

        #Activity Map according to days
        st.title("Activity Map")
        col1,col2=st.columns(2)

        with col1:
            st.header("Most Busy day")
            busy_day=function.week_activity(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color="pink")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month=function.month_activity(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color="yellow")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        if selected_user=="Overall":
            st.title("Most Busy User")
            x=function.most_busy_user(df)
            fig,ax=plt.subplots()

            col1,col2=st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color="red")
                plt.xticks(rotation="vertical")
                st.pyplot(fig)

            with col2:
                pass
        
        # st.title("Weekly Activity Map")
        # user_heatmap = function.activity_heatmap(selected_user,df)
        # fig,ax = plt.subplots()
        # ax = sns.heatmap(user_heatmap)
        # st.pyplot(fig)

        #WordCloud
        st.title("WordCloud")
        df_wc=function.create_wordcloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        most_common_df=function.most_commoon_words(selected_user,df)
        st.dataframe(most_common_df)

        #Emoji Analysis
        emoji_df=function.emoji_used(selected_user,df)
        st.title("Emoji Analysis")

        col1,col2=st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax=plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)

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
