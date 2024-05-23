import pandas as pd
import matplotlib.pyplot as plt


# Paths to the CSV files - these will need to be passed into the main() function or defined inside it
signups_path = 'Customer Loyalty History.csv'
flights_path = 'Customer Flight Activity.csv'
campaign_period_start = pd.Timestamp('2018-02-01')
campaign_period_end = pd.Timestamp('2018-04-30')

def load_data(signups_path, flights_path):
    signups_df = pd.read_csv(signups_path)
    flights_df = pd.read_csv(flights_path)
    return signups_df, flights_df

def clean_and_merge(signups_df, flights_df):
    merged_df = pd.merge(signups_df, flights_df, on='Loyalty Number', how='inner')
    return merged_df

def analyze_campaign_effect(merged_df, campaign_period_start, campaign_period_end):
    campaign_data = merged_df[(merged_df['Enrollment Year'] == campaign_period_start.year) &
                              (merged_df['Enrollment Month'].between(campaign_period_start.month, campaign_period_end.month))]
    cancellations_during_campaign = merged_df[(merged_df['Cancellation Year'] == campaign_period_start.year) &
                                              (merged_df['Cancellation Month'].between(campaign_period_start.month, campaign_period_end.month))]
    gross_impact = len(campaign_data['Loyalty Number'].unique())
    net_impact = gross_impact - len(cancellations_during_campaign['Loyalty Number'].unique())
    return gross_impact, net_impact

def analyze_demographics(merged_df, campaign_period_start, campaign_period_end):
    campaign_enrollments = merged_df[(merged_df['Enrollment Year'] == campaign_period_start.year) &
                                     (merged_df['Enrollment Month'].between(campaign_period_start.month, campaign_period_end.month))]
    demographics = ['Gender', 'Education', 'Marital Status']
    demographic_data = {demo: campaign_enrollments[demo].value_counts(normalize=True) for demo in demographics}
    return demographic_data

def analyze_flight_activity(merged_df):
    summer_months = [6, 7, 8]
    flights_summer_2018 = merged_df[(merged_df['Year'] == 2018) & (merged_df['Month'].isin(summer_months))]
    flights_summer_2017 = merged_df[(merged_df['Year'] == 2017) & (merged_df['Month'].isin(summer_months))]
    flights_booked_2018 = flights_summer_2018['Total Flights'].sum()
    flights_booked_2017 = flights_summer_2017['Total Flights'].sum()
    return flights_booked_2017, flights_booked_2018

def plot_campaign_impact(gross_impact, net_impact):
    labels = ['Gross Impact', 'Net Impact']
    values = [gross_impact, net_impact]
    plt.figure(figsize=(8, 5))
    plt.bar(labels, values, color=['blue', 'green'])
    plt.title('Campaign Impact on Loyalty Program Memberships')
    plt.ylabel('Number of Memberships')
    for i, v in enumerate(values):
        plt.text(i, v + 50, str(v), ha='center')
    plt.show()

def plot_demographics(demographic_data):
    for demo, data in demographic_data.items():
        plt.figure(figsize=(8, 5))
        data.plot(kind='bar')
        plt.title(f'Campaign Adoption by {demo}')
        plt.ylabel('Proportion of New Enrollments')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

def plot_flight_activity(flights_booked_2017, flights_booked_2018):
    years = ['2017', '2018']
    flights_booked = [flights_booked_2017, flights_booked_2018]
    plt.figure(figsize=(8, 5))
    plt.plot(years, flights_booked, marker='o', linestyle='-', color='r')
    plt.title('Impact on Booked Flights During Summer')
    plt.ylabel('Total Flights Booked')
    plt.xlabel('Year')
    for i, v in enumerate(flights_booked):
        plt.text(years[i], v + 500, str(v), ha='center')
    plt.show()

def main():
    signups_df, flights_df = load_data(signups_path, flights_path)
    merged_df = clean_and_merge(signups_df, flights_df)

    gross_impact, net_impact = analyze_campaign_effect(merged_df, campaign_period_start, campaign_period_end)
    print(f"Gross impact of the campaign on memberships: {gross_impact}")
    print(f"Net impact of the campaign on memberships (considering cancellations): {net_impact}")
    plot_campaign_impact(gross_impact, net_impact)


    demographic_data = analyze_demographics(merged_df, campaign_period_start, campaign_period_end)
    print("\nCampaign adoption by demographics:")
    for demo, data in demographic_data.items():
        print(f"\n{demo} breakdown:\n{data}")
    plot_demographics(demographic_data)

    
    flights_booked_2017, flights_booked_2018 = analyze_flight_activity(merged_df)
    print(f"\nTotal flights booked during summer 2017: {flights_booked_2017}")
    print(f"Total flights booked during summer 2018: {flights_booked_2018}")
    print(f"Change in number of flights booked from summer 2017 to summer 2018: {flights_booked_2018 - flights_booked_2017}")
    plot_flight_activity(flights_booked_2017, flights_booked_2018)

if __name__ == '__main__':
    main()
