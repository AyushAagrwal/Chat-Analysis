import streamlit as st
import function
import preprocessing
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

st.sidebar.title("Whatsapp Chat Analyzer 🎈")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df=preprocessing.preprocess(data)

    st.dataframe(df)

    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user=st.sidebar.selectbox("Show the analysis wrt ",user_list)

    if st.sidebar.button("Show Analysis"):
        
        total_message,words,num_media_message,links=function.fetch_stats(selected_user,df)

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
