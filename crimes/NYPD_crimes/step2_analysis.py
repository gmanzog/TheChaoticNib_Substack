"""
https://data.cityofnewyork.us/Public-Safety/NYC-crime/qb7u-rbmr/about_data
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from roughviz.charts import Pie

folder = 'C:/Users/gmger/OneDrive/Desktop/'

df = pd.read_parquet(folder + "/NYPD_Complaint_Data_Historic_20240922.parquet")

# boro = ['PATROL BORO BRONX', 'PATROL BORO MAN SOUTH',
#        'PATROL BORO BKLYN NORTH', 'PATROL BORO BKLYN SOUTH',
#        'PATROL BORO MAN NORTH', 'PATROL BORO QUEENS SOUTH',
#        'PATROL BORO QUEENS NORTH']
# df = df[df['PATROL_BORO'].isin(boro)]

# select only MvsF
df = df[(df['SUSP_SEX'].isin(['M', 'F'])) & (df['VIC_SEX'].isin(['M', 'F']))]


# df.columns
men_susp = df[(df['SUSP_SEX'] == 'M')]
women_susp = df[df['SUSP_SEX'] == 'F']
print(f"total number of crimes involving people: {len(men_susp) + len(women_susp)}")
print(f" of which women as suspect are {len(women_susp) / (len(men_susp) + len(women_susp))}")

allp = df[df['SUSP_SEX'].isin(['M', 'F'])]
print("Which gender is more likely to be a victim of a crime?")
print(allp.groupby("VIC_SEX")['CMPLNT_NUM'].count() / allp['CMPLNT_NUM'].count() * 100)
print(allp.groupby(["SUSP_SEX", "VIC_SEX"])['CMPLNT_NUM'].count() / allp['CMPLNT_NUM'].count() * 100)

pcts = {'category': ['Women', 'Men'], 'value': [60, 40]}
# Create a figure and axes
fig, ax = plt.subplots()
# Create the half pie chart
wedges, texts, autotexts = ax.pie(pcts['value'], labels=pcts['category'], colors=['purple', '#1f77b4'], startangle=90,
                                  counterclock=False, radius=1.5, autopct='%1.0f%%')
# Limiting the display to half pie
# ax.set_ylim(-1, 1)
# Annotating the pie chart with percentage values
for autotext in autotexts:
    autotext.set_color('black')  # Set text color to black
    autotext.set_fontsize(12)  # Set font size

# Equal aspect ratio ensures that pie chart is drawn as a circle.
ax.set(aspect="equal")
# Add a title
plt.title('Likelihood of Being Victim of a Crime')
plt.tight_layout()
plt.savefig("figures/pie.png")
# Show the plot
plt.show()


data = allp.groupby("VIC_SEX")['CMPLNT_NUM'].count() / allp['CMPLNT_NUM'].count() * 100


# print("How many of the men suspect involve men or woman")
# print(men_susp.groupby("VIC_SEX")['CMPLNT_NUM'].count() / men_susp['CMPLNT_NUM'].count() * 100)
# print("How many of the women suspect involve men or woman")
# print(women_susp.groupby("VIC_SEX")['CMPLNT_NUM'].count() / women_susp['CMPLNT_NUM'].count() * 100)

TOTAL = allp['CMPLNT_NUM'].count()
full_count = allp.groupby(["SUSP_SEX", "VIC_SEX"])['CMPLNT_NUM'].count()
uncon_pr = full_count / TOTAL
print(f"what's the probability that the victim is female? {uncon_pr.loc['F', 'F'] + uncon_pr.loc['M', 'F']:.2%}")

pr_male_given_female_vict = uncon_pr.loc['M', 'F'] / (uncon_pr.loc['F', 'F'] + uncon_pr.loc['M', 'F'])
print(f"What's the probability that, given the victim is a female, the suspect is male? {pr_male_given_female_vict:.2%}")

print("counting crimes")
table_count = full_count.unstack(level='VIC_SEX')
table_count['total_suspect'] = table_count.sum(axis=1)
table_count.loc['total_victims'] = table_count.sum(axis=0)

# what are the crimes in general
print("What's the AGE of the victims and suspect?")
for i in ['VIC_AGE_GROUP', 'SUSP_AGE_GROUP']:
    print(f"====> {i}")
    age = allp[allp[i].isin(['65+', '25-44', '18-24', '<18', '45-64'])]
    age = age.groupby(['SUSP_SEX', "VIC_SEX", i])['CMPLNT_NUM'].count() / age['CMPLNT_NUM'].count()
    print(age.unstack('SUSP_SEX'))

print("change to see crime on kids ")
agekid = allp[allp["VIC_AGE_GROUP"].isin(['65+', '25-44', '18-24', '<18', '45-64'])]
agekid = agekid.groupby(['SUSP_SEX', "VIC_SEX", "VIC_AGE_GROUP"])['CMPLNT_NUM'].count() / agekid['CMPLNT_NUM'].count()
print(agekid.unstack('SUSP_SEX').xs("<18", level="VIC_AGE_GROUP"))

# What race
print("What's the RACE of the victims and suspect?")
for i in ['VIC_RACE', 'SUSP_RACE']:
    print(f"====> {i}")
    race = allp.groupby(['SUSP_SEX', "VIC_SEX", i])['CMPLNT_NUM'].count() / allp['CMPLNT_NUM'].count()
    print(race.unstack('SUSP_SEX'))

# By location
allp['location'] = allp['PREM_TYP_DESC'].str.split(" -").str[0].str.split("-").str[0]
loc_pr = allp.groupby('location')['CMPLNT_NUM'].count() / allp['CMPLNT_NUM'].count()
loc_pr.sort_values(ascending=False, inplace=True)
print("Locaiton: uncoditional probs")
print(loc_pr.head(10) * 100)
print("====> In Numbers")
print(allp.groupby('location')['CMPLNT_NUM'].count().sort_values(ascending=False))
location = allp.groupby(['SUSP_SEX', "VIC_SEX", 'location'])['CMPLNT_NUM'].count() / allp['CMPLNT_NUM'].count()
location.sort_values(ascending=False, inplace=True)
print(location.head(10)*100)
print("in numbers")
print(allp.groupby(['SUSP_SEX', "VIC_SEX", 'location'])['CMPLNT_NUM'].count().sort_values(ascending=False))

# which crimes are committed the most?
print("====> In Numbers")
print(allp.groupby('OFNS_DESC')['CMPLNT_NUM'].count().sort_values(ascending=False) / allp['CMPLNT_NUM'].count() * 100)
print(allp.groupby('OFNS_DESC')['CMPLNT_NUM'].count().sort_values(ascending=False))
print("====> by location")
print(allp.groupby(['location', 'OFNS_DESC'])['CMPLNT_NUM'].count().sort_values(ascending=False) / allp['CMPLNT_NUM'].count() * 100)
print(allp.groupby(['location', 'PD_DESC'])['CMPLNT_NUM'].count().sort_values(ascending=False) / allp['CMPLNT_NUM'].count() * 100)
print("===> by location and gender")
print(allp.groupby(['SUSP_SEX', "VIC_SEX", 'OFNS_DESC'])['CMPLNT_NUM'].count().sort_values(ascending=False) / allp['CMPLNT_NUM'].count() * 100)

import calendar
print("TIME DIMENSION")
print("which month has the highest number of crimes")
months = allp.groupby(['month', "VIC_SEX"])['CMPLNT_NUM'].count() / allp['CMPLNT_NUM'].count() * 100
months = months.unstack("VIC_SEX")
months.index = [calendar.month_name[int(i)][:3] for i in months.index]
print(months)
plt.xkcd()
seasons = {'Winter1': [11, 12],
            'Winter': [0, 2],
           'Spring': [2, 4, 5],
           'Summer': [5, 7, 8],
           'Fall': [8, 10, 11]}
colors = {
"Winter1": "blue",
    "Winter": "blue",  # Dark blue
    "Spring": "green",  # Dark blue
    "Summer": "red",  # Orange
    "Fall": "orange",  # Yellow
}
# add seasons
months.columns.name = 'Victim Sex'
months.index.name = 'months'
text_location = {"Winter": 1,  "Spring": 3, "Summer": 6, "Fall": 9}
ax = months.plot(y='F', c='purple', marker="$\u2640$", label='F', markersize=12)  # Circle marker
months.plot(ax=ax, y='M', marker="$\u2642$", label='M', markersize=12)  # Circle marker
for k, (dayname, hrange) in enumerate(seasons.items()):
    ax.fill_betweenx([-1, 10], hrange[0], hrange[-1], color=colors[dayname], alpha=0.2)
    if dayname != "Winter1":
        ax.text(text_location[dayname], 2.3, dayname, fontsize=12, ha='center')
plt.title("Crime Rates by Month/Victim Sex")
ax.set_ylim([2, 6])
plt.xticks([0, 2, 5, 8, 11], ['Jan', 'Mar', 'Jun', 'Sep', 'Nov'])
plt.legend(title='Victim Sex', ncol=2)
plt.tight_layout()
plt.savefig("figures/months.png")
plt.show()

# MONTHS in RESIDENCE
months = allp[allp['location'] == 'RESIDENCE'].groupby(['month', "VIC_SEX"])['CMPLNT_NUM'].count() / allp['CMPLNT_NUM'].count() * 100
months = months.unstack("VIC_SEX")
months.index = [calendar.month_name[int(i)][:3] for i in months.index]
print(months)
plt.xkcd()
seasons = {'Winter1': [11, 12],
            'Winter': [0, 2],
           'Spring': [2, 4, 5],
           'Summer': [5, 7, 8],
           'Fall': [8, 10, 11]}
colors = {
"Winter1": "blue",
    "Winter": "blue",  # Dark blue
    "Spring": "green",  # Dark blue
    "Summer": "red",  # Orange
    "Fall": "orange",  # Yellow
}
# add seasons
months.columns.name = 'Victim Sex'
months.index.name = 'months'
text_location = {"Winter": 1,  "Spring": 3, "Summer": 6, "Fall": 9}
ax = months.plot(y='F', c='purple', marker="$\u2640$", label='F', markersize=12)  # Circle marker
months.plot(ax=ax, y='M', marker="$\u2642$", label='M', markersize=12)  # Circle marker
for k, (dayname, hrange) in enumerate(seasons.items()):
    ax.fill_betweenx([-1, 10], hrange[0], hrange[-1], color=colors[dayname], alpha=0.2)
    if dayname != "Winter1":
        ax.text(text_location[dayname], 2.3, dayname, fontsize=12, ha='center')
plt.title("Crime Rates by Month/Victim Sex")
ax.set_ylim([1, 4])
plt.xticks([0, 2, 5, 8, 11], ['Jan', 'Mar', 'Jun', 'Sep', 'Nov'])
plt.legend(title='Victim Sex', ncol=2)
plt.tight_layout()
plt.savefig("figures/months_residence.png")
plt.show()


print("YEARS")
years = allp.groupby(['year', "VIC_SEX"])['CMPLNT_NUM'].count() / allp['CMPLNT_NUM'].count() * 100
years = years.unstack("VIC_SEX")
# months.index = [calendar.month_name[int(i)][:3] for i in months.index]
y = [str(i) for i in range(2007, 2024)]
years = years.loc[y]
print(years.loc[y])
years.index = pd.to_datetime(years.index).to_period('Y')
plt.xkcd()
years.columns.name = 'Victim Sex'
years.index.name = 'years'
ax = years.plot(y='F', c='purple', marker="$\u2640$", label='F', markersize=12)  # Circle marker
years.plot(ax=ax, y='M', marker="$\u2642$", label='M', markersize=12)  # Circle marker
plt.title("Crime Rates by Year/Victim Sex")
plt.ylabel("%")
plt.legend(title='Victim Sex', ncol=2)
ax.axvline(pd.to_datetime('2020-1-1'), color='k', ls='--')
ax.text(pd.to_datetime('2020-1-1'), 4, "Covid", fontsize=18, ha='right')
ax.set_ylim([1, 4.5])
plt.tight_layout()
plt.savefig("figures/years.png")
plt.show()


print("TIME OF THE DAY")
from datetime import datetime
times = allp[(allp['CMPLNT_TO_TM'] != "(null)") & (allp['year'].isin(y))]
times['time_obj'] = pd.to_datetime(times['CMPLNT_TO_TM'], format="%H:%M:%S")
times['hours'] = times['time_obj'].dt.hour
hours = times.groupby(['hours', "VIC_SEX"])['CMPLNT_NUM'].count() / times['CMPLNT_NUM'].count() * 100
hours = hours.unstack("VIC_SEX")
plt.xkcd()
hours.index.name = 'hours'
hours.columns.name = 'Victim Sex'
ax = hours.plot(y='F', c='purple', marker="$\u2640$", label='F', markersize=12)  # Circle marker
hours.plot(ax=ax, y='M', marker="$\u2642$", label='M', markersize=12)  # Circle marker
plt.title("Crime Rates by Hours/Victim Sex")
plt.ylabel("%")
plt.legend(title='Victim Sex', ncol=2)
colors = {
    "Night": "#000080",  # Dark blue
    "Night1": "#000080",  # Dark blue
    "Morning": "#FFA500",  # Orange
    "Afternoon": "#FFFF00",  # Yellow
    "Evening": "#FF0000", # Red
}
for dayname, hrange in {'Morning': [5, 12],
                        'Afternoon': [12, 17],
                        'Evening': [17, 20],
                        'Night1': [20, 24],
                        'Night': [0, 5]}.items():
    ax.fill_betweenx([-1, 10], hrange[0], hrange[1], color=colors[dayname], alpha=0.2)
    # Add text annotation
    if dayname != "Night1":
        ax.text((hrange[0] + hrange[1]) / 2, .4, dayname, fontsize=12, ha='center')
ax.set_ylim([0, hours.max().max()+.5])
plt.tight_layout()
plt.savefig("figures/hours.png")
plt.show()

#
# times['CMPLNT_TO_TM']
#
# fig, ax = plt.subplots()
#
# # Create the half pie chart
# wedges, texts, autotexts = ax.pie(split['CMPLNT_NUM'], labels=split['index'], startangle=90, radius=1)
#
# # Set the aspect to 'equal' to ensure a circular shape
# ax.axis('equal')
#
# # Create a white circle to cover the bottom half
# centre_circle = plt.Circle((0,0), 0.5, color='white')
# ax.add_artist(centre_circle)
#
# plt.show()
#
# # Which crimes are committed?
# men_susp
#
# man[man['VIC_SEX']=='F'].groupby("pd_desc".upper())['CMPLNT_NUM'].count()
#
# mf = man[man['VIC_SEX'].isin(['M', 'F'])].dropna(subset=['Latitude', 'Longitude'])
g = sns.scatterplot(data=allp[allp['PATROL_BORO'].isin(['PATROL BORO BRONX', 'PATROL BORO MAN SOUTH',
       'PATROL BORO BKLYN NORTH', 'PATROL BORO BKLYN SOUTH',
       'PATROL BORO MAN NORTH', 'PATROL BORO QUEENS SOUTH',
       'PATROL BORO QUEENS NORTH'])],
                y='Latitude', x='Longitude', hue='VIC_SEX', s=.5)
g.get_legend().set_visible(False)
plt.title("Where Crimes Happen")
plt.tight_layout()
plt.savefig("figures/scatter.png")
plt.show()
# get rid of axis in the plot

#
