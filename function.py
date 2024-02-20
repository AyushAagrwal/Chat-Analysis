from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

def fetch_stats(selected_user,df):

    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    
    #Total numbers of message
    total_message=df.shape[0]
    
    #Total numbers of words
    words=[]
    for i in df['message']:
        words.extend(i.split())

    #Fetch numbers of media messages
    num_media_message=df[df['message']=='<Media omitted>'].shape[0]

    extract=URLExtract()

    links=[]
    for i in df['message']:
        links.extend(extract.find_urls(i))    

    return total_message,len(words),num_media_message,len(links)
    
def most_busy_user(df):
    x=df['user'].value_counts().head()
    
    return x

#Create WordCloud
def create_wordcloud(selected_user,df):
    
    f=open('stop_hinglish.txt','r')
    stop_words=f.read()

    if selected_user !="Overall":
        df=df[df['user']==selected_user]

    temp=df[df['user']!='group_notofications']
    temp=temp[temp['message']!='<Media omitted>']

    def remove_stop_word(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message']=temp['message'].apply(remove_stop_word)
    df_wc=wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

#Most common Words
def most_commoon_words(selected_user,df):

    f=open('stop_hinglish.txt','r')
    stop_words=f.read()

    if selected_user !="Overall":
        df=df[df['user']==selected_user]

    temp=df[df['user']!='group_notofications']
    temp=temp[temp['message']!='<Media omitted>']
    
    words=[]

    for i in temp['message']:
        for word in i.lower().split():
            if word not in stop_words:
                words.append(word)
    
    most_common_df=pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_used(selected_user,df):

    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    
    emojis=[]
    for i in df['message']:
        emojis.extend([c for c in i if c in emoji.UNICODE_EMOJI['en']])
    emoji_df=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df