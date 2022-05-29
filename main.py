                  #Problem statement: Data analytics in automotive industry.

#Importing libraries.
import plotly.graph_objects as go
import seaborn as sns
import streamlit as st
sns.set_style('darkgrid')
sns.set(font_scale=1.3)
import matplotlib.pyplot as plt
import pandas as pd
import altair as alt

# Title
st.title('Data Analysis for Automotive Industry')

#Importing csv file which contains data for analysis.
Data = pd.read_csv('cars_ds_final.csv')
#Converting Csv columns to lists for further analysis
car = Data.Make.to_list()
uni=Data.Make.unique()
car_model= Data.Model.to_list()
sales = Data.Sales_per_year_in_lakhs.to_list()
mileage = Data.City_Mileage.to_list()
car_prices = Data.Ex_Showroom_Price.to_list()
#Data cleanind by replacing unwanted values like , etc.

res_mileage = [sub.replace('km/litre', '') for sub in mileage]
res_mileage2 = [sub.replace(',', '.') for sub in res_mileage]
res_mileage3 = [sub.replace(' ', '') for sub in res_mileage2]
cnt_mil=0

#Converting mileage values into float dataype
for i in res_mileage3:
     res_mileage3[cnt_mil] = float(res_mileage3[cnt_mil])
     cnt_mil = cnt_mil + 1
#Similarly replacing unwanted values in Price coulumn with correct values and
#converting it into float. Here res3 will contain final cleaned values of Ex showroon price

res = [sub.replace('Rs.', '') for sub in car_prices]
res2 = [sub.replace(',', '') for sub in res]
res3 = [sub.replace(' ', '') for sub in res2]
cnt1 = 0
for i in res3:
     res3[cnt1] = float(res3[cnt1])
     cnt1 = cnt1 + 1


#Craeting main dashboard to choose different analysis options
st.header("Dashboard")
option = st.selectbox('Select the analysis you want!!',('Please select below options',
                                                        'Sales',
                                                        'View price distribution of cars',
                                                        'See Company offering maximum number of models and variants',
                                                        'Mileage analysis',
                                                        "Fuel type and it's demand analysis",
                                                        'Most preferred  specification(Body type)',
                                                        ))
if option=="Fuel type and it's demand analysis":
        option=st.selectbox('select',('Fuel vs Sales analysis','Fuel distribution analysis'))
        fuel = Data.Fuel_Type.to_list()
        if option=='Fuel vs Sales analysis':
            st.write('This analysis will show sales of car based upon their fuel type.')
            #Grouping the data frame for creating required plots
            df_fuel = pd.DataFrame({'Fuel': fuel,
                               'Sale': sales})

            # use groupby() to compute sum
            #Plotting the graph of fuel vs sales
            df_fuel = df_fuel.groupby(['Fuel']).sum()
            st.header('plot of fuel type vs their sales')
            st.write('x-axis=Fuel type'
                      'y-axis=Sales')
            st.bar_chart(df_fuel)
            st.header('-----------------------------------------------------------')
            #Providing report of analysis
            st.header('Report')
            st.write('-Above fuel vs sales analysis, shows that Sales of pertol cars is more'
                     ' than diesel,cng and other fuels')
            st.write('-Hence customers , prefer to buy more petrol and diesel cars other '
                     ' than fuel cars like cng ,etc. ')
            st.write('Therefore , more petrol and diesel cars engines must be manufactured!!')

        #This option will give analysis of a specific company based on fuel type

        elif option=='Fuel distribution analysis':
            st.write('Above pie chart will show fuel distribution of selected company.'
                     ' This will help particular company to take specific decisions '
                     ' to increase thier sales based on Fuel demand and Fuel type of a car.')
            #uni is a list of all unique car companies names.
            #select box is created to choose specific company
            option2= st.selectbox(
                'Choose the company',
                (uni))

#Creating data of fuel type vs it's count and hence plotting.
            c_name = []
            fuel_list = []
            cnt = 0
            #appending fuel type and incrementing count if company name matches
            for i in car:
                if i == option2:

                    fuel_list.append(fuel[cnt])
                    cnt = cnt + 1
                else:
                    cnt = cnt + 1

            fuel_cnt = []
            t = (fuel_list.count('Diesel'))
            t2 = fuel_list.count('Petrol')
            fuel_cnt.append(t)
            fuel_cnt.append(t2)

            fuel_ty = ['Diesel', 'Petrol']
            # The plot
            st.header("Pie chart of fuel type vs it's demand")
            fig = go.Figure(
                go.Pie(
                    labels=fuel_ty,
                    values=fuel_cnt,
                    hoverinfo="label+percent"
                ))

            st.plotly_chart(fig)

#This option will give analysis of city mileage of cars with price and sales.
elif option == 'Mileage analysis':
            option=st.selectbox('Select',('Car and Company which gives highest mileage car',
                                          'Mileage vs sales analysis'))
            if option=='Car and Company which gives highest mileage car':
                mileage_of_cars = []
                uni = Data.Make.unique()
                # print(uni)
                cnt = 0
                for i in res_mileage3:
                    res_mileage3[cnt] = float(res_mileage3[cnt])
                    cnt = cnt + 1
                #Index of maximum value from list
                milmax = max(res_mileage3)
                maxi_index = res_mileage3.index(milmax)

                st.header('Company giving highest mileage car is:')
                st.subheader(car[maxi_index])
                st.header('Highest mileage is')
                st.subheader(milmax)
                st.header('Model of car offering highest mileage is:')
                st.subheader(car_model[maxi_index])
                #creating dataframe and plotting it.

                source1 = pd.DataFrame({
                    'Companies': car,
                    'Mileage': res_mileage3

                })

                bar_chart1 = alt.Chart(source1).mark_bar(size=6).encode(
                    y='Mileage',
                    x='Companies',
                    color=alt.condition(
                        alt.datum.Companies == 'Maruti Suzuki',  # If the year is 1810 this test returns True,
                        alt.value('yellow'),  # which sets the bar orange.
                        alt.value('steelblue')
                    )
                ).configure_view(
                    strokeWidth=0.5,
                    height=500,
                    width=700)

                st.altair_chart(bar_chart1, use_container_width=True)

#This option gives all the analysis related to mileage and it's variation with sales and price

            elif option=='Mileage vs sales analysis':
                df_mileage = pd.DataFrame({'Mileage': res_mileage3,
                                   'Sale(in lakhs)': sales})

                # use groupby() to compute sum
                df_mileage= df_mileage.groupby(['Mileage']).sum()
                st.header('Mileage vs Sales graph')
                st.bar_chart(df_mileage)
                st.header('______________________________________________________________')
                st.header('Report')
                st.write('Sales of cars having mileage between 14 to 25 km/litre is maximum'
                         ' as compared to cars having low mileage.')
                st.write('Hence large number of customers prefer cars with price '
                         ' between 1 lakhs to 25 lakhs and having '
                         ' mileage between 14 to 25 km/litre.')

#Sales segment from dashboard
elif option=='Sales':
            sales = Data.Sales_per_year_in_lakhs.to_list()

#Creating sub choices in sales segment.
            choice = st.radio("Select one", ("None",
                                             "Analyze sales of cars of a specific company",
                                             "Compare sales of companies",
                                             "Analyze the period of a sale in a year",
                                             "Launch Year wise sale of companies",
                                             "Analyze Sales collected from different distribution chanels"))
           #creating dataset for analysis
            df = pd.DataFrame({'Company': car,
                               'Sale': sales})

            # use groupby() to compute sum
            df = df.groupby(['Company']).sum()
            if choice=='Compare sales of companies':

                #analysis of highest and lowest sold company and car
                option5 = st.selectbox('Select',('Highest sold car and least sold car',
                                                 'Highest and least sold company'
                                                 ))


                #st.header(car[inde])
                if option5=='Highest sold car and least sold car':
                    #finding maximum value of sales from sales list
                    max_car_sale=max(sales)
                    #index of maximum sold car
                    index_max_sale=sales.index(max_car_sale)

                    st.header('Highest sold car:')
                    st.write(car_model[index_max_sale])
                    st.header('Company')
                    st.write(car[index_max_sale])
                    st.write('Therefore Maruti Suzuki has highest sold car among all the '
                             ' car companies.')

                    st.header('Least sold car:')
                    min_car_sale=min(sales)
                    index_min_sale = sales.index(min_car_sale)
                    st.write(car_model[index_min_sale])
                    st.header('Company')
                    st.write(car[index_min_sale])
                    st.write('Toyota has least sold car model among all'
                             ' the companies.')

#                    plot the bar graph of sales per company
                    st.header('Plot of Company vs Sale of their highest sold car')
                    st.write('This plot visualizes company vs their highest sold model '
                             ' based upon their sale values.')
                    source4 = pd.DataFrame({
                        'Sales of company in lakhs per year':sales,
                        'company': car

                    })

                    bar_chart4 = alt.Chart(source4).mark_bar(size=4).encode(
                        y='Sales of company in lakhs per year',
                        x='company',
                        color=alt.condition(
                            alt.datum.company == car[index_max_sale],  # If the year is 1810 this test returns True,
                            alt.value('orange'),  # which sets the bar orange.
                            alt.value('steelblue')
                        )
                    ).configure_view(
                        strokeWidth=0.5,
                        height=500,
                        width=1500)
                    st.altair_chart(bar_chart4, use_container_width=True)

# Highest and least sold company
                elif option5=='Highest and least sold company':
                    st.write(df)
                    #Plotting created dataframe
                    st.header('Plot of company s their total sales.')
                    st.write('x-axis= Company name'
                             ' y-axis=Total sales')
                    st.bar_chart(df)
                    st.write('Scroll down for reports!')
                    st.header('_____________________________________________________')
                    st.header('Company having total highest sale(avg per year) is:')
                    max_company_sale = df[['Sale']].idxmax()
                    st.header(df.loc[max_company_sale])

                    st.header('Company having total least sales')
                    min_sale = df[['Sale']].idxmin()
                    st.header(df.loc[min_sale])
                    st.write('Hence Maruti suzuki cars are preferred by large number of '
                             ' customers.')

#This option provides analysis of Sale distribution of a specific company

            elif choice=='Analyze sales of cars of a specific company':

                option4= st.selectbox('Choose from below!!',('Choose','Statistics and visualization','Reports based upon analysis'))

                #This functionality gives option to select any car company
                # Based on selected company, it's sale distribution is showed in tabular
                # as well as in charts
                if option4=='Statistics and visualization':

                    col1,col2=st.columns([6,8])
                    with col2:
                        option2= st.selectbox('Select company you want!!', (uni))
                        company_sale = []
                        car_name = []
                        cnt3=0
                        for i in car:
                            if i==option2:
                                company_sale.append(sales[cnt3])
                                car_name.append(car_model[cnt3])
                                cnt3+=1
                            else:
                                cnt3+=1
                    #Created dataframe
                        source6= pd.DataFrame({
                            'Sales(lakhs)': company_sale,
                            'car_model': car_name

                        })
                        bar_chart6 = alt.Chart(source6).mark_bar(size=4).encode(
                            y='Sales(lakhs)',
                            x='car_model',

                        ).configure_view(
                            strokeWidth=1.0,
                            height=500,
                            width=300)
                        st.altair_chart(bar_chart6, use_container_width=True)
                    with col1:
                        st.header('Statistics are shown below:')
                        st.write(source6)

            #This option gives reports generated from above analysis.
                if option4=='Reports based upon analysis':
                    #here option of different car companies are provided so as to find
                    # highest and least revenue generating model of that particular company.

                    option2 = st.selectbox('Select company you want!!', (uni))
                    company_sale = []
                    car_name = []
                    cnt3 = 0
                    for i in car:
                        if i == option2:

                            company_sale.append(sales[cnt3])
                            car_name.append(car_model[cnt3])
                            cnt3 += 1
                        else:
                            cnt3 += 1

                    #Maximum value from list
                    max_model = max(company_sale)

                    max_index = company_sale.index(max_model)


                    st.header('The Analysis for decisions in buisness are:'
                              ' ___________________________________________')
                    st.subheader('The highest revenue generating car model of this company is:')
                    st.header(car_name[max_index])
                    st.write('-Therefore,company must increase the manufacturing and production of this model to benefit the buisness.'
                                 ' ______________________________________________________________________________________________________')


                    st.write('-Similarly,Company must reduce manufacturing and production of the model '
                             ' giving least revenue to grow their buisness'
                                 ' and focus on production of other models.')

 #This functionality analyses sale happened in months .

            elif choice=='Analyze the period of a sale in a year':
                Month_sales = Data.Purchased_Month.to_list()
                df_month = pd.DataFrame({'Month': Month_sales,
                                         'Sale': sales})

                # use groupby() to compute sum
                df_month = df_month.groupby(['Month']).sum()
                option_month=st.selectbox('Select',('View analysis on sales by month',
                                              'View report based upon analysis'))
                if option_month=='View analysis on sales by month':

                    st.bar_chart(df_month)
                if option_month=='View report based upon analysis':

                    st.header('Maximum sale of cars happen in month:')
                    max_month = df_month[['Sale']].idxmax()
                    st.write(df_month.loc[max_month])

                    st.header('Minimum sale of cars happen in month:')
                    min_month = df_month[['Sale']].idxmin()
                    st.write(df_month.loc[min_month])
                    st.subheader('________________________________________________________________'
                                 ' Hence, in this month, Company should reduce their production'
                                 ' and focus more on manufacturing and marketing strategies.')

#This functionality gives sale collected from showroom ,franchise ,etc
            elif choice=='Analyze Sales collected from different distribution chanels':
                option=st.selectbox('Select',('None','Distribution analysis of company vs sales',
                                    'Preferred medium to buy a car',
                                   'Reports for buisness decisions'))
                channel=Data.Distribution_chanel.to_list()

                if option=='Distribution analysis of company vs sales':
                    df_channel=pd.DataFrame({'Medium':channel,
                                             'Sale':sales})
                    df_channel = df_channel.groupby(['Medium']).sum()
                    st.subheader('Analysis of Distribution medium vs Sales')
                    st.write(df_channel)
                    st.write('x-axis= Distribution channels'
                             ' y-axis=Sales')
                    st.bar_chart(df_channel)
                    fig = plt.figure(figsize=(50, 35))

                    st.header('Plot of Distribution medium vs sales of each company')
                    ax = sns.barplot(x="Make", y="Sales_per_year_in_lakhs", hue="Distribution_chanel",
                                     data=Data)
                    st.pyplot(fig)
                    st.header('_______________________________________')

                if option=='Preferred medium to buy a car':
                    fig1 = plt.figure(figsize=(5,4))
                    sns.countplot(x="Distribution_chanel", data=Data)
                    st.pyplot(fig1)
                    st.header('________________________________________')



                if option=='Reports for buisness decisions':
                    st.header('Following are the reports ,which will help buisness take decisions to'
                              ' grow business.')
                    st.write('From above analysis,More sale of cars take place'
                             ' through own showrooms than franchise. Less sale takes place through resale'
                             ' purchase of cars.Hence companies must setup more number of showrooms'
                             ' than setting up franchise.')
                    st.header("______________________________________________________________________________")
                    st.write('Customers prefer buying cars from showrooms than '
                                 ' franchise and resale purchase.'
                                 ' Hence more showrooms must ne setup to increase and attract customers'
                                 ' and in turn sale of a company.')
            elif choice=='Launch Year wise sale of companies':
                year_sales=Data.Launch_year.to_list()
                df_year = pd.DataFrame({'Year':year_sales,
                                         'Sale': sales})

                # use groupby() to compute sum
                df_year = df_year.groupby(['Year']).sum()
                st.header('Graph of launch year vs sales in lakhs')
                st.write('x-axis=Year of launch of cars'
                          'y-axis=sales in lakhs')
                st.bar_chart(df_year)
                st.header('Report')
                st.write('The cars launched between year 2014 to 2019 have maximum '
                         ' sales and then it decreased gradually.')


elif option=='View price distribution of cars':
            option=st.selectbox('Select',('Price vs sales analysis',
                                          'Company having highest and lowest priced cars',
                                          'Highest and lowest price cars',
                                          'Correlation of price and other specifications'
                                          ))
            #calculating index of maximum value in list of prices(ex showeoom) i.e res3
            a = max(res3)
            index = res3.index(a)
            if option=='Price vs sales analysis':


                st.header('Price vs sales analysis')
                fig = plt.figure(figsize=(10, 4))

                p=sns.lineplot(x=res3, y=sales)
                p.set_ylabel("Sales in lakks", fontsize=20)
                p.set_xlabel("Ex showroom price", fontsize=20)
                st.pyplot(fig)

                st.header('Plot of price distribution')
                st.write('x-axis:Car count'
                         ' , y-axis:Price(Rs)')
                chart_data = pd.DataFrame(
                    res3)
                st.area_chart(chart_data)
                st.header("Report")
                st.write('* Sales of Cars decreases as price crosses 1 crore. ')
                st.write('* Maximum cars are sold between price ranging from 1 lakhs to 25 lakhs'
                         ' Hence most of the companies are producing cars price ranging from '
                         ' 5 lakhs to 17 lakhs which can satisfy and attract middle class customers more.')




            elif option == ('Company having highest and lowest priced cars'):
                df_price= pd.DataFrame({'Company':car,
                                   'price':res3})

                # use groupby() to compute sum
                df_price = df_price.groupby(['Company']).sum()
                st.header('Plot of Company vs Ex showroom Price')
                st.bar_chart(df_price)
                st.write(df_price)
                st.header("____________________________________________________________")
                st.header('Report')
                st.write('-Based upon above analysis,Rolls-Royce company has highest priced cars'
                         ' but their sale is low as compared to other companies ,as Rolls-royce '
                         ' comes under luxurious cars    ')
                st.write('-Bajaj company offers lowest priced cars and their sale is higher than highest priced '
                         ' cars.')
                st.write('-Hence customers prefer mid range(1-25 lakhs) cars over highly expensive luxury cars')

            elif option=='Highest and lowest price cars':
                st.header('Car having highest Ex_showroom price is:')
                st.write(car_model[index])
                st.write('*sale(lakhs):')
                st.write(sales[index])
                st.header('Company:')
                st.write(car[index])

                min_price = min(res3)
                min_index = res3.index(min_price)
                st.header("Car having lowest Ex Showroom price is and it's sales :")
                st.write(car[min_index])
                st.write('*sale(lakhs):')
                st.write(sales[min_index])

                st.header('Model:')
                st.write(car_model[min_index])
                car_price=max(res3)
                car_index=res3.index(car_price)
                #creating dataframe by grouping companies with their price
                st.header('Plot of Companies vs thier total sales(in lakhs)')
                source3 = pd.DataFrame({
                    'companies': car,
                    'Price(Rs)': res3

                })
                bar_chart3 = alt.Chart(source3).mark_bar(size=8).encode(
                    y='Price(Rs)',
                    x='companies',
                    color=alt.condition(
                        alt.datum.companies == car[car_index],  # If the year is 1810 this test returns True,
                        alt.value('pink'),  # which sets the bar orange.
                        alt.value('steelblue')
                    )

                ).configure_view(
                    strokeWidth=0.5,
                    height=500,
                    width=800)
                st.altair_chart(bar_chart3, use_container_width=True)

                #This functionality will find correlation between different
                #specifications and price

            elif option=='Correlation of price and other specifications':

                st.header('Regression plot of height vs price')
                height=Data.Height.to_list()
                fig = plt.figure(figsize=(10, 4))

                ax = sns.regplot(x=res3, y=height)
                ax.set_xlabel("Height", fontsize=20)
                ax.set_ylabel("Price", fontsize=20)
                st.pyplot(fig)

                st.header('Regression plot of length vs price')
                length= Data.Length.to_list()
                fig2 = plt.figure(figsize=(10, 4))
                ax = sns.regplot(x=res3, y=length)
                ax.set_xlabel("Length", fontsize=20)
                ax.set_ylabel("Price", fontsize=20)
                st.pyplot(fig2)

                st.header('Regression plot of width vs price')
                width = Data.Width.to_list()
                fig3= plt.figure(figsize=(10, 4))
                ax = sns.regplot(x=res3, y=width)
                ax.set_xlabel("width", fontsize=20)
                ax.set_ylabel("Price", fontsize=20)
                st.pyplot(fig3)

                st.header('Regression plot of horsepower vs price')
                hp=Data.horsepower.to_list()
                fig4 = plt.figure(figsize=(10, 4))

                ax = sns.regplot(x=res3, y=hp)
                ax.set_xlabel("Horsepower", fontsize=20)
                ax.set_ylabel("Price", fontsize=20)
                st.pyplot(fig4)
                st.header('Report')
                st.write('-Above regression plots gives analysis of price dependency on '
                         ' different specifications like height,length and width')
                st.write('-Plot of height vs price shows negative linear regression and hence as'
                         ' height of the car increases, price decreases.'
                         ' This comes in resonance with hatchback body car type ,since they have'
                         ' greater height than sedan cars.It also shows that price of hatch back cars is'
                         ' less than sedan luxurious cars.')
                st.write('-Plot of length vs price shows positive linear regression. It shows that '
                         ' as length of a car increases, price of car '
                         ' also increases simultaneously. This also proves that sedan car having '
                         ' more length than height have greater prices compared to hatchback cars.')
                st.write('-Plot of width vd price also shows positive linear regression')
                st.write('Plot of horsepower vs price also shows sharp positive regression '
                         ' than width and length. Hence horsepower will be best variable to'
                         ' determine and predict price of cars.')



elif option=='Most preferred  specification(Body type)':

    #This functionality
                 option=st.selectbox('select',(uni))
                 #Car type vs sales of car

                 Body_type=Data.Body_Type.to_list()
                 df_body = pd.DataFrame({'Body': Body_type,
                                    'Sale': sales})

                 # use groupby() to compute sum
                 df_body = df_body.groupby(['Body']).sum()
                 st.header('Body type vs Sales  of cars.')
                 st.write('x axis-body type'
                          ' y axis-sales(in lakhs)')
                 st.bar_chart(df_body)
                 st.write(df_body)
                 st.header('________________________________________________________')
                 st.header('Report')
                 st.write('*Sales of SUV and Hatch back body type cars is more than sedan and '
                          ' other types. ')
                 st.write('Hence Customers prefer SUV and hatchback cars more over sedan.')

#This option wil show company offering large number of car models and variants


elif option == 'See Company offering maximum number of models and variants':

       car = Data.Make.to_list()
       #appending car names and count
       c = []
       val = []
       for i in car:
           if i not in val:
               val.append(i)
               c.append(car.count(i))
       ti = []
       for i in val:
           ti.append(1)


       t = max(c)
       maxi_index = c.index(t)

       st.header("Company offering maximum number of models and variants:")
       st.subheader(val[maxi_index])
       st.subheader('Different Models available:')
       st.subheader(t)
       st.header('Plot of company vs model count ')
       source = pd.DataFrame({
           'Different models': c,
           'company': val

       })

       bar_chart = alt.Chart(source).mark_bar(size=10).encode(
           y='Different models',
           x='company',
           color=alt.condition(
               alt.datum.company ==val[maxi_index],  # If the year is 1810 this test returns True,
               alt.value('orange'),  # which sets the bar orange.
               alt.value('steelblue')
           )
       ).configure_view(
           strokeWidth=1.0,
           height=500,
           width=600)

       st.altair_chart(bar_chart, use_container_width=True)
       st.header('------------------------------------------------------------')
       st.header('Report')
       st.write('Maruti Suzuki offers wide range of models and variants.Hence customers have'
                ' a wider range of choice .Therefore this company also has maximum sales '
                'as they have average prices and also higher mileage.'
                )
       st.write('-Hence companies should focus on designing different models which will'
                ' satisfy the needs of middle class customers.')


#------------------------END--------------------------------------------------------------