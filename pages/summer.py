import sys
import os
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
from PIL import Image

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules')))
from modules import preprocessor
from modules import  helper

athlete_data = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', 'data', 'athlete_events.csv'))
region_data = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', 'data', 'noc_regions.csv'))
st.markdown(
    """
    <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
        [data-testid="stSidebarUserContent"] {
            padding-top: 0rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
st.sidebar.page_link("app.py", label="Back to Home", icon="🏠")
df = preprocessor.preprocess_summer(athlete_data, region_data)
st.sidebar.markdown("<h1 style='text-align: center;'>Summer Olympics Analysis</h1>", unsafe_allow_html=True)
image_path = os.path.join(os.path.dirname(__file__), 'image.png')
if os.path.exists(image_path):
    image = Image.open(image_path)
    st.sidebar.image(image, caption='Summer Olympics')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-Wise Analysis', 'Athlete-Wise Analysis')
)
st.markdown(
    """
    <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
#Medal Tally
if user_menu == 'Medal Tally':
    st.sidebar.markdown("<h1 style='text-align: center;'>Medal Tally</h1>", unsafe_allow_html=True)
    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.markdown("<h1 style='text-align: center;'>Overall Anlysis</h1>", unsafe_allow_html=True)
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.markdown("<h1 style='text-align: center;'>Medal Tally in " + str(selected_year) + " Olympics</h1>", unsafe_allow_html=True)
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.markdown(f"<h1 style='text-align: center;'>{selected_country} Overall Performance</h1>",unsafe_allow_html=True)
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.markdown(f"<h1 style='text-align: center;'>{selected_country} performance in {str(selected_year)} Olympics</h1>",unsafe_allow_html=True)
    st.table(medal_tally)

#Overall analysis
if user_menu == 'Overall Analysis':
    Editions = df['Year'].unique().shape[0]
    Cities = df['City'].unique().shape[0]
    Sports = df['Sport'].unique().shape[0]
    Athletes = df['Name'].unique().shape[0]
    Nation = df['region'].unique().shape[0]
    Events = df['Event'].unique().shape[0]

    #Showing stats
    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Edition")
        st.title(Editions)
    with col2:
        st.header("Hosts")
        st.title(Cities)
    with col3:
        st.header("Sports")
        st.title(Sports)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(Events)
    with col2:
        st.header("Nation")
        st.title(Nation)
    with col3:
        st.header("Athletes")
        st.title(Athletes)
    
    #lineplot = no. of countries over the years
    nations_over_time = helper.data_over_time(df, 'region')
    fig = px.line(
        nations_over_time,
        x="Edition",
        y="region",
        markers=True,
        title="Growth of Participating Nations Over Years"
    )

    fig.update_traces(line_shape='spline', line=dict(width=3, color='royalblue'))

    fig.update_layout(
        plot_bgcolor="white",
        xaxis_title="Olympic Edition (Year)",
        yaxis_title="Number of Participating Countries",
        title_font=dict(size=12, family="Arial", color="black"),
        xaxis=dict(showgrid=True, gridcolor="darkgray"),
        yaxis=dict(showgrid=True, gridcolor="darkgray")
    )
    st.plotly_chart(fig)

    #lineplot = no. of events hosted per year
    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(
        events_over_time,
        x="Edition",
        y="Event",
        markers=True,
        title="Total Number of Events per year"
    )

    fig.update_traces(line_shape='spline', line=dict(width=3, color='royalblue'))

    fig.update_layout(
        plot_bgcolor="white",
        xaxis_title="Olympic Edition (Year)",
        yaxis_title="Number of Participating Countries",
        title_font=dict(size=12, family="Arial", color="black"),
        xaxis=dict(showgrid=True, gridcolor="darkgray"),
        yaxis=dict(showgrid=True, gridcolor="darkgray")
    )
    st.plotly_chart(fig)

    #lineplot = no. of Athletes participated
    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(
        athlete_over_time,
        x="Edition",
        y="Name",
        markers=True,
        title="Total Number of Events per year"
    )

    fig.update_traces(line_shape='spline', line=dict(width=3, color='royalblue'))

    fig.update_layout(
        plot_bgcolor="white",
        xaxis_title="Olympic Edition (Year)",
        yaxis_title="Number of Participating Countries",
        title_font=dict(size=12, family="Arial", color="black"),
        xaxis=dict(showgrid=True, gridcolor="darkgray"),
        yaxis=dict(showgrid=True, gridcolor="darkgray")
    )
    st.plotly_chart(fig)

    #heat map for no of events per year
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    heatmap_data = x.pivot_table(
        index='Sport',
        columns='Year',
        values='Event',
        aggfunc='count'
    ).fillna(0).astype(int)

    fig, ax = plt.subplots(figsize=(15, 10))
    sns.heatmap(
        heatmap_data,
        annot=True,      
        fmt="d",           
        cmap="OrRd",
        linewidths=0.5,      
        cbar_kws={'label': 'Number of Events'},
        ax=ax
    )
    ax.set_title("Number of Events per Sport Over the Years", fontsize=18, pad=20)
    ax.set_xlabel("Year", fontsize=14)
    ax.set_ylabel("Sport", fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(fontsize=10)
    plt.tight_layout()
    st.pyplot(fig)

    #data for most successfull athletes -> spots wise
    st.markdown("<h1 style='text-align: center;'>Most Successful Athletes</h1>", unsafe_allow_html=True)
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    x = helper.most_successfull(df, selected_sport)
    st.table(x)

#Country wise Analysis
if user_menu == "Country-Wise Analysis":
    st.sidebar.markdown("<h1 style='text-align: center;'>Country-Wise Analysis</h1>", unsafe_allow_html=True)
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a Country', country_list)
    
    #no. of medals won country wise per year
    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(
        country_df,
        x="Year",
        y="Medal",
        markers=True,
        title="Country-Wise Analysis"
    )
    st.markdown(f"<h1 style='text-align: center;'>{selected_country} Medal tally over the years</h1>", unsafe_allow_html=True)

    fig.update_traces(line_shape='spline', line=dict(width=3, color='royalblue'))

    fig.update_layout(
        plot_bgcolor="white",
        xaxis_title="Years",
        yaxis_title="Total Medals",
        title_font=dict(size=12, family="Arial", color="black"),
        xaxis=dict(showgrid=True, gridcolor="darkgray"),
        yaxis=dict(showgrid=True, gridcolor="darkgray")
    )
    st.plotly_chart(fig)

    #heat map for country won no. of medals per year
    pt = helper.Country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(15, 10))
    sns.heatmap(
        pt,
        annot=True,      
        fmt="d",           
        cmap="crest",
        linewidths=0.5,      
        cbar_kws={'label': 'Number of Events'},
        ax=ax
    )
    ax.set_title(selected_country + " Excels int the following sports", fontsize=18, pad=20)
    ax.set_xlabel("Year", fontsize=14)
    ax.set_ylabel("Sport", fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(fontsize=10)
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown(f"<h1 style='text-align: center;'>Top 15 athletes of {selected_country}</h1>", unsafe_allow_html=True)
    most_successful = helper.most_successful(df, selected_country)
    st.table(most_successful)


#Athlete wise Analysis
if user_menu == 'Athlete-Wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot(
    [x1, x2, x3, x4],
    ['Overall Age', 'Gold', 'Silver', 'Bronze'],
    show_hist=False,
    show_rug=False
    )

    colors = ['royalblue', 'gold', 'silver', 'peru']
    for i, trace in enumerate(fig.data):
        trace.line.update(color=colors[i], width=3, shape='spline')

    fig.update_layout(
        title="Age Distribution of Medalists",
        plot_bgcolor='white',
        xaxis_title="Age", yaxis_title="Density",
        xaxis=dict(showgrid=True, gridcolor='lightgray'),
        yaxis=dict(showgrid=True, gridcolor='lightgray'),
        legend_title="Category",
        title_font=dict(size=16)
    )

    st.markdown(f"<h1 style='text-align: center;'>Age Distribution Among Medalists</h1>", unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)

    x, name = [], []
    famous_sports = [
        'Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
        'Swimming', 'Badminton', 'Sailing', 'Gymnastics', 'Art Competitions',
        'Handball', 'Weightlifting', 'Wrestling', 'Water Polo', 'Hockey',
        'Rowing', 'Fencing', 'Shooting', 'Boxing', 'Taekwondo', 'Cycling',
        'Diving', 'Canoeing', 'Tennis', 'Golf', 'Softball', 'Archery',
        'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
        'Rhythmic Gymnastics', 'Rugby Sevens', 'Beach Volleyball',
        'Triathlon', 'Rugby', 'Polo', 'Ice Hockey'
    ]

    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        ages = temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna()
        if len(ages) > 1:  
            x.append(ages)
            name.append(sport)

    if x:  # only plot if we have valid data
        fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
        fig.update_traces(line=dict(width=3, shape='spline'))
        fig.update_layout(
            title="Distribution of Age wrt Sports (Gold Medalists)",
            plot_bgcolor="white",
            xaxis_title="Age",
            yaxis_title="Density",
            width=1000,
            height=600,
            legend_title="Sport",
            xaxis=dict(showgrid=True, gridcolor="lightgray"),
            yaxis=dict(showgrid=True, gridcolor="lightgray")
        )
        st.markdown(f"<h1 style='text-align: center;'>Distribution of Age with respect to Sports (Gold Medalists)</h1>", unsafe_allow_html=True)

        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Not enough valid data to display age distribution.")

    st.markdown(f"<h1 style='text-align: center;'>Height vs Weight</h1>", unsafe_allow_html=True)

    sport_list = df['Sport'].dropna().unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df, selected_sport)

    fig, ax = plt.subplots(figsize=(6, 4)) 
    sns.scatterplot(
        data=temp_df,
        x='Weight', y='Height',
        hue='Medal', style='Sex',
        s=50, alpha=0.8, ax=ax
    )

    ax.set_title(f"Height vs Weight in {selected_sport}", fontsize=12, pad=10)
    ax.set_xlabel("Weight", fontsize=10)
    ax.set_ylabel("Height", fontsize=10)
    ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.5)

    ax.legend(title="Medal / Sex", bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)

    st.pyplot(fig, use_container_width=True)


    # Men vs Women Participation Over Years
    st.markdown(f"<h1 style='text-align: center;'>Men vs Women Participation Over the Years</h1>", unsafe_allow_html=True)

    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"], markers=True)
    fig.update_traces(line_shape='spline', line=dict(width=3))
    fig.update_layout(
        title='Participation of Men and Women',
        width=1000, height=600,
        plot_bgcolor="white",
        xaxis_title="Year",
        yaxis_title="Number of Athletes",
        xaxis=dict(showgrid=True, gridcolor="lightgray"),
        yaxis=dict(showgrid=True, gridcolor="lightgray"),
        title_font=dict(size=16)
    )
    st.plotly_chart(fig, use_container_width=True)