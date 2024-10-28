#%% [markdown]
# We are doing data analysis on a dataset with 6,000 entries that contains data on death rates for suicide, 
# by selected population characteristics.
# The dataset is accessible from this website: https://catalog.data.gov/dataset/death-rates-for-suicide-by-sex-race-hispanic-origin-and-age-united-states-020c1

# %%
#%pip install pandas
import pandas as pd
import matplotlib.pyplot as plt

#%%
# Load the CSV file
file_path = 'Death_rates_for_suicide__by_sex__race__Hispanic_origin__and_age__United_States.csv' 
file = pd.read_csv(file_path)

# Display the first few rows of the dataframe
#print("First few rows of the data:")
#print(file.head())

# Explore unique values in each column to understand what each column does
print("\nUnique values in each column:")
for column in file.columns:
    if column == 'ESTIMATE': break
    print(f"{column}: {file[column].unique()}")

print(file.columns)


# %%
# There are three main factors concerning the death rate: sex, age, and race.
# And there are two units: age-adjusted deaths per 100,000 resident population and crude deaths...
# We will approach this dataset by first showing the mortality rate across years by each factor in each unit
# Note that the years are not consecutive, from 1950-1980 are 1950, 1960, 1970, 1980
# In this case it is better to use histogram instead of scatterplot, so that readers can focus more on the trend
# Whereas in scatterplot, people will tend to think that ten years remain the same

# Let's first take a look at the overall trend
# Filter the data for 'total' mortality and 'all persons'
total_mortality = file[(file['STUB_NAME'] == 'Total') & (file['STUB_LABEL'] == 'All persons')]

# Separate the data into age-adjusted and crude
age_adjusted = total_mortality[total_mortality['UNIT_NUM'] == 1]
crude = total_mortality[total_mortality['UNIT_NUM'] == 2]

years = age_adjusted['YEAR'].unique()
first_year = age_adjusted['YEAR'].min()
last_year = age_adjusted['YEAR'].max()

# Set the size of the plot
plt.figure(figsize=(12, 6))

# Plotting Age-Adjusted Rates
plt.subplot(1, 2, 1)  # 1 row, 2 columns, 1st subplot
plt.hist(years, weights=age_adjusted['ESTIMATE'], bins=len(years), alpha=0.7, color='yellow',edgecolor='black')
plt.title('Age-Adjusted Mortality Rate Over the Years')
plt.xlabel(f'Year ({first_year} to {last_year})')
plt.ylabel('Mortality Rate (per 100,000)')

# Plotting Crude Rates
plt.subplot(1, 2, 2)  # 1 row, 2 columns, 2nd subplot
plt.hist(years, weights=crude['ESTIMATE'], bins=len(years), alpha=0.7, color='grey',edgecolor='black')
plt.title('Crude Mortality Rate Over the Years')
plt.xlabel(f'Year ({first_year} to {last_year})')
plt.ylabel('Mortality Rate (per 100,000)')

# Show the plot
plt.tight_layout()
plt.show()

# Interesting to see that the graph shows the pattern that mostly one year has lower number and the following one to 
# two year show almost double.
# And it seems that 2001 has the lowest number of mortality rate among the graph, but why?

#%%
# We are not seeing much difference between age-adjusted morality rate vs. crude morality rate
# Here we concern more the trend of morality rate throughout years
# We use the age-adjuested data
# Now, let's show the morality rate by each main factor
# First, by sex
sex_groups = ['Male','Female']
sex_morality = file[(file['STUB_NAME'] == 'Sex') & (file['UNIT_NUM'] == 1)]
male_morality = sex_morality[sex_morality['STUB_LABEL'] == 'Male']
female_morality = sex_morality[sex_morality['STUB_LABEL'] == 'Female']


# Set the size of the plot
fig, axs = plt.subplots(1, 2, figsize=(12, 6), sharey=True)  # Create 1 row, 2 columns of subplots with shared y-axis

# Plotting Male Mortality Rate
axs[0].hist(years, weights=male_morality['ESTIMATE'], bins=len(years), alpha=0.7, color='blue', edgecolor='black')
axs[0].set_title('Male Mortality Rate Over the Years')
axs[0].set_xlabel(f'Year ({first_year} to {last_year})')
axs[0].set_ylabel('Mortality Rate (per 100,000)')

# Plotting Female Mortality Rate
axs[1].hist(years, weights=female_morality['ESTIMATE'], bins=len(years), alpha=0.7, color='pink', edgecolor='black')
axs[1].set_title('Female Mortality Rate Over the Years')
axs[1].set_xlabel(f'Year ({first_year} to {last_year})')
# axs[1].set_ylabel('Mortality Rate (per 100,000)')  # No need to set Y label again due to sharey

# Automatically adjust subplot parameters to give specified padding
plt.tight_layout()
plt.show()

# On the sex plots, it is showned that male demonstrate a higher mortality rate than female

#%%
# Second, by age. It comes a bit complex because age has many groups.
# We use the crude data
age_groups = file['AGE'].unique()
print(age_groups)
print(len(age_groups))
age_groups = age_groups[(age_groups != '15-24 years') & 
                        (age_groups != '25-44 years') &
                        (age_groups != '45-64 years') & 
                        (age_groups != '65 years and over')]

# %%
#Filter out the age data
age_mortality = file[(file['UNIT_NUM'] == 2) & file['STUB_NAME'].isin(['Total', 'Age'])]

# Set up the plot for main group
colors = ['blue','pink','yellow','cyan','magenta','orange','red','purple','black','brown','grey']
markers = ['o', 's', '^', 'x', 'd', 'p', '*', 'h', 'v', '<','>']
plt.figure(figsize=(12, 12))

# Plot each age group
for age, color, marker in zip(age_groups, colors, markers):
    subset = age_mortality[age_mortality['AGE'] == age]
    plt.plot(subset['YEAR'], subset['ESTIMATE'], alpha=0.7, color=color, marker=marker, label=age)

# Adding labels and title
plt.xlabel(f'Year ({first_year} to {last_year})')
plt.ylabel('Mortality Rate (per 100,000)')
plt.title('Comparison of Mortality Rates Across Age Groups Over Years')
plt.legend(title='Age Group',loc='right',bbox_to_anchor=(1.22, 0.5))
plt.grid(True)

# Show the plot
plt.show()

# It seems that in general, age groups over 20 has a higher mortality rate than the average (all ages).
# Among 1980-2000 years, age 75+ has the highest mortality rate.
# 2000 years next on, younger age groups (15+) have rising mortality rate.

# %%
# Now, we would like to see the morality rate by race
# STUB_LABEL is concatenated by gender and race, and we need to extract race from it

# Filter data for age-adjusted unit
race_groups = file[(file['UNIT_NUM'] == 1) & (file['STUB_NAME']=='Sex and race')]

# Extract race from STUB_LABEL
race_groups['Race'] = race_groups['STUB_LABEL'].str.extract(':(.+)$')[0].str.strip()

print(race_groups)
# Check extracted races to ensure accuracy
print(race_groups['Race'].unique())

# Group data by race and year, then calculate mean mortality rates
race_mortality = race_groups.groupby(['Race', 'YEAR'])['ESTIMATE'].mean().reset_index()

# Plotting
plt.figure(figsize=(14, 12))
races = race_mortality['Race'].unique()
for race in races:
    subset = race_mortality[race_mortality['Race'] == race]
    plt.plot(subset['YEAR'], subset['ESTIMATE'], label=race, marker='o')

plt.title('Age-Adjusted Mortality Rates by Race Over Years')
plt.xlabel(f'Year ({first_year} to {last_year})')
plt.ylabel('Mortality Rate (per 100,000)')
plt.legend(title='Race', bbox_to_anchor=(1.3, 0.5), loc='right')
plt.grid(True)
plt.tight_layout()
plt.show()

# In the graph we can tell that the White race has a higher mortality rate than any other race.
# 'Asian or Pacific Islander' and 'Black or African American' have lowest mortality rate.

#%%
# We would like to see the influence by both sex and race now.

# Filter for age-adjusted data
filtered_data = file[file['UNIT_NUM'] == 1]

# Extract race and sex
filtered_data['Sex'] = filtered_data['STUB_LABEL'].str.split(':').str[0]
filtered_data['Race'] = filtered_data['STUB_LABEL'].str.split(':').str[1].str.strip()

print(filtered_data)

# Group by sex, race, and year to get mean estimates
grouped_data = filtered_data.groupby(['Sex', 'Race', 'YEAR'])['ESTIMATE'].mean().reset_index()

# Plotting
fig, ax = plt.subplots(figsize=(14, 8))

# Colors for each race, assuming a finite set of known races
color_dict = {
    'White': 'blue', 
    'Black or African American': 'green', 
    'American Indian or Alaska Native': 'red', 
    'Asian or Pacific Islander': 'purple'
}

sex_dict = {
    'Male':'o',
    'Female':'x'
}

# Plot each sex and race combination
for (sex, race), group in grouped_data.groupby(['Sex', 'Race']):
    if race.strip() in color_dict:  # Ensure race is in our color dictionary
        ax.plot(group['YEAR'], group['ESTIMATE'], label=f'{sex}: {race}', color=color_dict[race.strip()], marker=sex_dict[sex.strip()], linestyle='-')

ax.set_title('Mortality Rates by Sex and Race Over Years')
ax.set_xlabel('Year')
ax.set_ylabel('Mortality Rate (per 100,000)')
ax.legend(title='Sex and Race', bbox_to_anchor=(1.4, 0.5), loc='right')
ax.grid(True)

plt.tight_layout()
plt.show()

# Regardless of the sex difference, male has a much higher mortality rate than female.
# White Male seems to be the group with highest mortality rate.
# Black or African American has the lowest mortality rate throughout years.


# %%
