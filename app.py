import streamlit as st
import pandas as pd
import helper
import plotly.express as px
import plotly.figure_factory as ff


df_atheletes = pd.read_csv('athletes.csv')
df_medallists = pd.read_csv('medallists.csv')
df_medals = pd.read_csv('medals.csv')
df_medals_total = pd.read_csv('medals_total.csv')
df_events = pd.read_csv('events.csv')

df_medals['medal_date'] = pd.to_datetime(df_medals['medal_date'])


st.set_page_config(page_title='Paris Olympics Analysis Dashboard', page_icon='https://flaticons.net/icon.php?slug_category=sports&slug_icon=olympics-logo', layout='wide', initial_sidebar_state='auto')



countries = helper.get_countries(df_atheletes)
countries = sorted(countries)
countries.insert(0, 'All')

st.sidebar.header("Paris Olympics Analysis Dashboard")
st.sidebar.image('https://flaticons.net/icon.php?slug_category=sports&slug_icon=olympics-logo')
user_menu = st.sidebar.radio('Select:',["Overall Analysis", "Medals Analysis", "Athlete Analysis"])

total_sports, total_events, total_participants, total_countries = helper.get_overall_cards(df_atheletes,df_events)

if user_menu == "Overall Analysis":
    st.title("Overall Analysis")
    st.subheader('Top Statistics')
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.write("Total Sports")
        st.title(total_sports)
    with col2:
        st.write("Total Events")
        st.title(total_events)
    with col3:
        st.write("Total Participants")
        st.title(total_participants)
    with col4:
        st.write("Total Countries")
        st.title(total_countries)
        
    st.subheader('Top Countries')
    view_top = st.slider('Select Top Countries:', 1, 92, 5)
    df_medals_total.index = df_medals_total.index+1
    st.table(df_medals_total.head(view_top))
    bar_question = st.checkbox('See this as a bar chart?', value=True)
    
    if bar_question == True:
        df_melted = pd.melt(df_medals_total.head(view_top), id_vars=['country_code'], value_vars=['Gold Medal', 'Silver Medal', 'Bronze Medal'],  var_name='medal', value_name='count')

        fig = px.bar(df_melted, x='country_code', y='count', color='medal', title='Medals by Country', labels={'count': 'Medals Count', 'country_code': 'Country Code'}, barmode='stack')

        st.plotly_chart(fig)
        
    st.subheader('Top Sports')
    df_sports = df_events.groupby('sport').size().reset_index(name='count').sort_values('count', ascending=False)
    fig = px.bar(df_sports.head(13), x='sport', y='count', 
             title='Number of Events by Sport', 
             labels={'count': 'Number of Events', 'sport': 'Sport'},
             color='count', 
             color_continuous_scale='Viridis')
    st.plotly_chart(fig)
    
    
    
    
    
elif user_menu == "Medals Analysis":
    selected_country = st.sidebar.selectbox('Select Country', countries)
    total_gold, total_silver, total_bronze = helper.get_medal_cards(df_medals_total,selected_country)
    st.title("Medal Analysis")
    st.subheader('Medal Counts')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("Total Golds")
        st.title(total_gold)
    with col2:
        st.write("Total Silvers")
        st.title(total_silver)
    with col3:
        st.write("Total Bronzes")
        st.title(total_bronze)
        
    st.subheader('Medal Distribution')
    try:
        df_medals_grouped = helper.filter_by_country(df_medals,selected_country).groupby(['medal_date', 'medal_type']).size().reset_index(name='count')
        df_pivot = df_medals_grouped.pivot(index='medal_date', columns='medal_type', values='count').fillna(0)

        datefig = px.line(df_pivot, x=df_pivot.index, y=df_pivot.columns,
                    labels={'value': 'Number of Medals', 'medal_date': 'Date'},
                    title='Medals Awarded Each Day',
                    markers=True)

        st.plotly_chart(datefig)
        st.write("You can click on the legend to hide/show the medal type.")
    except:
        st.write("Sorry, it seems like this country has not won any medals.") 
        
        
    st.subheader('Gender Distribution of Winners')
    df_gender = helper.filter_by_country(df_medallists,selected_country).groupby('gender').size().reset_index(name='count')
    if df_gender.empty:
        st.write("Sorry, it seems like this country has not won any medals.")
    else:
        fig = px.pie(df_gender, values='count', names='gender', title='Gender Distribution Pie Plot')
        st.plotly_chart(fig)
        st.text('*In team sports each member is counted as a winner so the medal count may not be equal to the number of medals won by the country.')
        
    
    st.subheader('Age Distribution of Winners')
    df_medallists = helper.calculate_medalists_age(helper.filter_by_country(df_medallists,selected_country)) 
    x2 = df_medallists[df_medallists['medal_type'] == 'Gold Medal']['age'].dropna()
    x3 = df_medallists[df_medallists['medal_type'] == 'Silver Medal']['age'].dropna()
    x4 = df_medallists[df_medallists['medal_type'] == 'Bronze Medal']['age'].dropna()
    try:
        col4, col5, col6 = st.columns(3)
        with col4:
            st.write("Average Gold Medalist Age")
            st.title(round(x2.mean()))
        with col5:
            st.write("Average Silver Medalist Age")
            st.title(round(x3.mean()))
        with col6:
            st.write("Average Bronze Medalist Age")
            st.title(round(x4.mean()))
    except:
        pass

    
    try:


        fig = ff.create_distplot([x2, x3, x4], [ 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
        st.plotly_chart(fig)       
    except:
        st.write("Insufficient data to plot the age distribution. Try picking another country.")
        
    st.subheader('Top Athletes')
    df_most_medals = df_medallists
    try:

        df_most_medals = helper.get_top_medalists_df(df_most_medals,selected_country)
        df_most_medals.index = df_most_medals.index+1
        top_medals_value = st.slider('Select Top Athletes:', 1, df_most_medals.shape[0])
        st.table(df_most_medals.head(top_medals_value))
    except:
        st.write("Sorry, it seems like this country has no recurring medallists.")
        
    st.subheader('See Medalists by Discipline')
    selected_discipline = st.selectbox('Select Discipline:', df_medallists['discipline'].unique())
    df_top_medallists_by_discipline = helper.fetch_by_discipline(df_medallists, selected_discipline ,selected_country)
    if df_top_medallists_by_discipline.empty:
        st.write("Sorry, it seems like has not won any medals")
    else:
        st.table(df_top_medallists_by_discipline.reset_index(drop=True))    
      
    
    
elif user_menu == "Athlete Analysis":
    selected_country = st.sidebar.selectbox('Select Country', countries)
    
    st.title("Athlete Analysis")
    st.subheader('Age Distribution of Athletes')
    df_atheletes_age = helper.calculate_age(df_atheletes, selected_country)
    df_atheletes_age.dropna(inplace=True)
    try:
        dist_age = ff.create_distplot([df_atheletes_age], ['Age'], show_hist=False, show_rug=False)
        st.plotly_chart(dist_age)
    except:
        st.write("Insufficient data to create visualisation.")
    
    st.subheader('Top Cities by Athlete Count')
    df_filtered = helper.filter_by_country(df_atheletes, selected_country)
    df_filtered = df_filtered[df_filtered['birth_place'].notna()]
    df_unique_birthplace = df_filtered.drop_duplicates(subset='birth_place')
    athletes_geodata = df_unique_birthplace[['country_code', 'name', 'birth_place']]
    athletes_geodata['cleaned_birth_place'] = athletes_geodata['birth_place'].apply(helper.clean_birth_place)
    athletes_geodata = athletes_geodata[athletes_geodata['cleaned_birth_place'].str.match(r'^[A-Za-z\s]+$', na=False)]
    athletes_geodata = athletes_geodata.drop(columns=['birth_place'])
    df_city_count = athletes_geodata['cleaned_birth_place'].value_counts().reset_index()
    df_city_count.columns = ['birth_place', 'Athelete Count']
    df_city_count = df_city_count[df_city_count['Athelete Count'] > 1]
    df_city_count.index = df_city_count.index+1
    if df_city_count.empty:
        st.write("Sorry, it seems like there are no cities with more than one athlete.")
    else:
        if df_city_count.shape[0] == 1:
            st.table(df_city_count)
        else:
            number_entries = st.number_input('Select Number of Cities To Display:', 1, df_city_count.shape[0])
            st.table(df_city_count.head(number_entries))
        
    st.subheader('Oldest and Youngest Athletes')
    df_atheletes['disciplines'] = df_atheletes['disciplines'][0]
    df_atheletes['disciplines'] = df_atheletes['disciplines'].str.replace(r'[^a-zA-Z\s]', '', regex=True)
    df_ath_age = df_atheletes[['name','age','country_code','disciplines']]
    df_ath_age.dropna(inplace=True, subset=['age'])
    df_ath_age_top = df_ath_age.sort_values('age', ascending=False)
    df_ath_age_bottom = df_ath_age.sort_values('age', ascending=True)
    df_ath_age = pd.concat([df_ath_age_top.head(5), pd.DataFrame([['--']*4], columns=df_ath_age_top.columns), df_ath_age_bottom.head(5).sort_values('age', ascending=False)])
    st.table(df_ath_age.reset_index(drop=True))
    
    st.subheader('Most Spoken Languages')
    df_lang_filter = helper.filter_by_country(df_atheletes, selected_country)
    df_languages = helper.split_by_deli(df_lang_filter,'lang')
    df_languages = df_languages.apply(lambda x: x.str.replace(r'[^a-zA-Z]', '', regex=True))
    df_languages_top = helper.get_top(df_languages)
    lang_fig = px.bar(df_languages_top.head(11), x='column', y='frequency', title='Most Spoken Languages', labels={'frequency': 'Frequency', 'column': 'Language'})
    st.plotly_chart(lang_fig)
    
    st.subheader('Male Participation vs Female Participation')
    df_gender_overall = helper.filter_by_country(df_atheletes,selected_country).groupby('gender').size().reset_index(name='count')

    fig = px.pie(df_gender_overall, values='count', names='gender', title='Gender Distribution Pie Plot')
    st.plotly_chart(fig)
    
    
    st.subheader('Top Occupations of Athletes')
    df_occ_filter = helper.filter_by_country(df_atheletes, selected_country)
    df_occu = helper.split_by_deli(df_occ_filter,'occupation')
    df_occu = df_occu.apply(lambda x: x.str.replace(r'[^a-zA-Z\s]', '', regex=True))
    df_occu_top = helper.get_top(df_occu)
    df_occu_top = df_occu_top[df_occu_top['frequency'] > 1]
    occ_fig = px.bar(df_occu_top.head(10), x='column', y='frequency', title='Top Occupations of Athletes', labels={'frequency': 'Frequency', 'column': 'Occupation'})
    st.plotly_chart(occ_fig)
    
    
    
    

    

