import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import COVID19Py




pandemics=["All","Ebola","Swine Flu","Covid-19"]


@st.cache
def get_country_codes():
    # Country Codes
    codes=pd.read_csv('./data.csv')
    codes=codes.set_index('Name')
    return codes


@st.cache
def get_country_data(country_code):
    
    covid19 = COVID19Py.COVID19()
    Country=country_code
    covid19 = COVID19Py.COVID19(data_source="jhu")
    location = covid19.getLocationByCountryCode(Country,timelines=True)
    confirmed=location[0]['timelines']['confirmed']['timeline']
    deaths=location[0]['timelines']['deaths']['timeline']
        
    df=pd.Series(confirmed).to_frame('Timeline')
    df["Date"]=pd.to_datetime(df.index)
    df["Date"]=df['Date'].dt.date
    
    df2=pd.Series(deaths).to_frame('Timeline')
    df2["Date"]=pd.to_datetime(df2.index)
    df2["Date"]=df2['Date'].dt.date
    return df,df2



@st.cache(allow_output_mutation=True)
def make_charts(codes,country_names):

    charts=[]
    main_fig=go.Figure()
    for name in country_names:
        code=codes.loc[name]
        df,df2=get_country_data(code)

        fig=go.Figure()

        fig.add_trace(go.Bar(x=df.Date,
                            y=df.Timeline,
                            name='Confirmed Cases'
                            )
        )

        fig.add_trace(go.Bar(x=df2.Date,
                            y=df2.Timeline,
                            name='Confirmed Deaths'
                            )
        )

        fig.update_layout(title=name,
                   xaxis_title='Date',
                   yaxis_title='Number of Cases')

        charts.append(fig)

        main_fig.add_trace(go.Scatter(x=df.Date,
                                    y=df.Timeline,
                                    name=name)
        )


    main_fig.update_layout(title="Comparison",
                   xaxis_title='Date',
                   yaxis_title='Number of Cases')

    charts.insert(0,main_fig)

    return charts



@st.cache(allow_output_mutation=True)
def load_datasets():
    ebola=pd.read_csv('./ebola/ebola_2014_2016_clean.csv')
    swine_flu=pd.read_csv('./swine_flu/swine_flu.csv')
    mers=pd.read_csv('./mers/weekly_clean.csv')
    sars=pd.read_csv('./sars/sars_2003_complete_dataset_clean.csv')
    covid=pd.read_csv('./covid/covid_19_clean_complete.csv')


    ebola.rename(columns={  "No. of confirmed cases": "ConfirmedCases",
                "No. of confirmed deaths": "ConfirmedDeaths",
                "No. of probable deaths": "ProbDeaths",
                "No. of probable cases": "ProbCases"
            },inplace=True)


    

    
    return ebola,swine_flu,covid




def comparison(ebola,swine_flu,covid):

    spanish_flu={"Cases":  500000000,
                "Deaths": 50000000  
    }

    hiv={"Cases": 75000000,
        "Deaths": 32000000
    }

    names=["Spanish Flu","Hiv","Ebola","Swine Flu","Covid"]
    cases=[spanish_flu["Cases"],hiv["Cases"],ebola.ConfirmedCases.sum(),swine_flu.Cases.sum(),covid.Confirmed.sum()]

    total=spanish_flu["Deaths"]+hiv["Deaths"]+ebola.ConfirmedDeaths.sum()+covid.Deaths.sum()+swine_flu.Deaths.sum()


    size=[(spanish_flu["Deaths"]/total)*100,(hiv["Deaths"]/total)*100,(ebola.ConfirmedDeaths.sum()/total)*100,(swine_flu.Deaths.sum()/total)*100,(covid.Deaths.sum()/total)*100]

    fig = go.Figure()


    fig.add_trace(go.Scatter(
        x=names,
        y=cases,
        text=['Deaths: '+str(spanish_flu["Deaths"]),'Deaths: '+str(ebola.ConfirmedDeaths.sum()),'Deaths: '+str(covid.Deaths.sum())],
        mode='markers',
        marker=dict(
            size=size,
            color=['rgb(93, 164, 214)', 'rgb(255, 144, 14)',  'rgb(44, 160, 101)', 'rgb(255, 65, 54)', 'rgb(255, 65, 104)']
        )
    ))

    fig.update_layout(title='Confirmed Cases',
                   yaxis_title='Confirmed',
                   xaxis_title='Pandemic')

    return fig





@st.cache
def plot_ebola(data):
    gb=data.groupby(["Date"]).sum()
    fig=go.Figure()


    fig.add_trace(go.Scatter(x=gb.index,y=gb["ConfirmedCases"],name="Confirmed"))
    fig.add_trace(go.Scatter(x=gb.index,y=gb["ConfirmedDeaths"],name="Deaths"))


    fig.update_layout(title='Ebola',
                    xaxis_title='Date',
                    yaxis_title='Number of Cases')

    return fig



@st.cache
def plot_swine_flu(swine_flu):
    swine_flu["Date"]=pd.to_datetime(swine_flu["Update Time"])
    swine_flu["Date"]=swine_flu["Date"].dt.date
    gb2=swine_flu.groupby(['Date']).sum()

    fig=go.Figure()


    fig.add_trace(go.Scatter(x=gb2.index,y=gb2["Cases"],name='Confirmed'))
    fig.add_trace(go.Scatter(x=gb2.index,y=gb2["Deaths"],name='Deaths'))


    fig.update_layout(title='Swine Flu',
                    xaxis_title='Date',
                    yaxis_title='Number of Cases')

    return fig




def main():
    st.title("Pandemic Visualizer")
    info_text=st.text("Visualize various Pandemics throughout the modern history")

    st.sidebar.subheader("Pandemic Visualizer")
    pandemic=st.sidebar.selectbox("Pandemic",pandemics)


    ebola,swine_flu,covid=load_datasets()


    if(pandemic=="All"):
        chart=comparison(ebola,swine_flu,covid)
        st.plotly_chart(chart)
    elif(pandemic=='Covid-19'):
        code=get_country_codes()
        country_select=st.sidebar.multiselect("Country",code.index)


        charts=make_charts(code,country_select)


        for chart in charts:
            st.plotly_chart(chart,use_container_width=True)

    elif(pandemic=='Ebola'):  
        info_text.empty()
        st.plotly_chart(plot_ebola(ebola))
    elif(pandemic=='Swine Flu'):
        st.plotly_chart(plot_swine_flu(swine_flu))


if __name__ == "__main__":
    main()


# # print(country_select)

# st.write(code)








# st.sidebar.markdown("Select Multiple Markdowns")





