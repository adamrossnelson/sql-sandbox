# Exploratory Data Analysis Lessons

This guide walks through common data exploration tasks using SQL queries on our sample datasets.

By default the sqlite3 interactive environment won't include column names in its output. To activate display of the column names use the command `.headers on` which will make your output more readable.

## How To Study With This Guide

For each task this guide both describes a simplistic and realistic data exploration task and also provides code in Python (Pandas) that will produce the desired result. Your task, as a learner who already knows Pandas, is to write SQL queries that will accomplish the exploration task.

## MPG Dataset Explorations

### 1. Overall Vehicle Statistics
Task: Write a query to get the average weight, horsepower, and efficiency across all vehicles.

Here's how we'd do it in Python:
```python
>>> df = sns.load_dataset('mpg')
>>> df[['weight','horsepower','mpg']].mean().apply(lambda x: round(x, 2))

weight        2970.42
horsepower     104.47
mpg             23.51
dtype: float64
```

Proposed solution here:
```sql
SELECT 
    ROUND(AVG(weight), 2) as avg_weight,
    ROUND(AVG(horsepower), 2) as avg_horsepower,
    ROUND(AVG(mpg), 2) as avg_mpg
FROM mpg;
```

Also note that sqllite will support display of column names with the command `.headers on`.

### 2. Statistics by Origin
Task: Write a query to compare vehicle characteristics across different manufacturing origins.

Here's how we'd do it in Python:
```python
>>> df = sns.load_dataset('mpg')
>>> df.groupby('origin')[['weight', 'horsepower', 'mpg']].mean().round(2)

             weight  horsepower    mpg
origin                               
europe    2423.30      80.56   27.89
japan     2221.23      79.84   30.45
usa       3361.93     119.05   20.08
```

Proposed solution here:
```sql
SELECT 
    origin,
    ROUND(AVG(weight), 2) as avg_weight,
    ROUND(AVG(horsepower), 2) as avg_horsepower,
    ROUND(AVG(mpg), 2) as avg_mpg
FROM mpg
GROUP BY origin
ORDER BY avg_mpg DESC;
```

### 3. Yearly Trends
Task: Write a query to see how vehicle characteristics have changed over time.

Here's how we'd do it in Python:
```python
>>> df = sns.load_dataset('mpg')
>>> df.groupby('model_year')[['weight', 'horsepower', 'mpg']].mean().round(2)

            weight  horsepower    mpg
model_year                           
70         3372.79     147.83   17.69
71         2995.43     107.04   21.25
72         3237.71     120.18   18.71
73         3419.03     130.48   17.10
74         2877.93      94.23   22.70
75         3176.80     101.07   20.27
76         3078.74     101.12   21.57
77         2997.36     105.07   23.38
78         2861.81      99.69   24.06
79         3055.34     101.21   25.09
80         2436.66      77.48   33.70
81         2522.93      81.04   30.33
82         2453.55      81.47   31.71
```

Proposed solution here:
```sql
SELECT 
    model_year,
    ROUND(AVG(weight), 2) as avg_weight,
    ROUND(AVG(horsepower), 2) as avg_horsepower,
    ROUND(AVG(mpg), 2) as avg_mpg
FROM mpg
GROUP BY model_year
ORDER BY model_year;
```

### 4. Detailed Analysis by Year and Origin
Task: Write a query to combine year and origin to see more detailed trends.

Here's how we'd do it in Python:
```python
>>> df = sns.load_dataset('mpg')
>>> df.groupby(['model_year', 'origin'])[['weight', 'horsepower', 'mpg']].mean().round(2)

                        weight  horsepower    mpg
model_year origin                               
70         europe  2309.200000   86.200000  25.200000
           japan   2251.000000   91.500000  25.500000
           usa     3716.500000  166.954545  15.272727
71         europe  2024.000000   74.000000  28.750000
           japan   1936.000000   79.250000  29.500000
           usa     3401.600000  119.842105  18.100000
72         europe  2573.200000   79.600000  22.000000
           japan   2300.400000   93.800000  24.200000
           usa     3682.666667  138.777778  16.277778
. . .
80         europe  2348.000000   66.750000  37.288889
           japan   2290.307692   78.846154  35.400000
           usa     2822.428571   88.833333  25.914286
81         europe  2725.000000   76.666667  31.575000
           japan   2269.166667   78.333333  32.958333
           usa     2695.000000   84.538462  27.530769
82         europe  2055.000000   63.000000  40.000000
           japan   2132.777778   74.000000  34.888889
           usa     2637.750000   86.947368  29.450000
```

Proposed solution here:
```sql
SELECT 
    model_year,
    origin,
    ROUND(AVG(weight), 2) as avg_weight,
    ROUND(AVG(horsepower), 2) as avg_horsepower,
    ROUND(AVG(mpg), 2) as avg_mpg
FROM mpg
GROUP BY model_year, origin
ORDER BY model_year, origin;
```

## Tips Dataset Analysis

### 5. Tips as Proportion of Bill
Task: Write a query to view tips both as absolute amounts and as percentages of the total bill.

Here's how we'd do it in Python:
```python
>>> df = sns.load_dataset('tips')
>>> df['proportion'] = df['tip'] / df['total_bill']
>>> df[['total_bill','tip','proportion']].sample(5)

     total_bill   tip  proportion
98        21.01  3.00    0.142789
22        15.77  2.23    0.141408
138       16.00  2.00    0.125000
169       10.63  2.00    0.188147
235       10.07  1.25    0.124131
```

Alternatively the `.assign()` method would produce similar results as follows:

```python
>>> df[['total_bill','tip']].assign(proportion = df['tip'] / df['total_bill'])
```

Proposed solution here:
```sql
SELECT 
    total_bill,
    tip,
    ROUND(tip / total_bill * 100, 2) as tip_percentage,
    day,
    time,
    size as party_size
FROM tips
LIMIT 5;
```

## Penguins Dataset Analysis

### 6. Species and Sex Distribution
Task: Write a query to create a cross-tabulation of penguin species and sex.

Here's how we'd do it in Python:
```python
>>> df = sns.load_dataset('penguins')
>>> pd.crosstab(df['species'], df['sex'])

sex        Female  Male
species                
Adelie         73    73
Chinstrap      34    34
Gentoo         58    61
```

Proposed solution here:
```sql
SELECT 
    species,
    SUM(CASE WHEN sex = 'Male' THEN 1 ELSE 0 END) as male_count,
    SUM(CASE WHEN sex = 'Female' THEN 1 ELSE 0 END) as female_count
FROM penguins
GROUP BY species
ORDER BY species;
```

### 7. Island and Sex Distribution
Task: Write a query to create a cross-tabulation of island location and sex.

Here's how we'd do it in Python:
```python
>>> df = sns.load_dataset('penguins')
>>> pd.crosstab(df['island'], df['sex'])

sex        Female  Male
island                 
Biscoe         80    83
Dream          61    62
Torgersen      24    23
```

Proposed solution here:
```sql
SELECT 
    island,
    SUM(CASE WHEN sex = 'Male' THEN 1 ELSE 0 END) as male_count,
    SUM(CASE WHEN sex = 'Female' THEN 1 ELSE 0 END) as female_count
FROM penguins
GROUP BY island
ORDER BY island;
```

### 8. Island Location, Sex, and Species
Task: Write a query to create a cross-tabulation of species, island location, and sex.

Here's how we'd do it in Python:
```python
>>> df = sns.load_dataset('penguins')
>>> pd.crosstab([df['species'], df['island']], df['sex'])

sex                  Female  Male
species   island                 
Adelie    Biscoe         22    22
          Dream          27    28
          Torgersen      24    23
Chinstrap Dream          34    34
Gentoo    Biscoe         58    61
```

Proposed solution here:
```sql
SELECT 
    species,
    island,
    SUM(CASE WHEN sex = 'Male' THEN 1 ELSE 0 END) as male_count,
    SUM(CASE WHEN sex = 'Female' THEN 1 ELSE 0 END) as female_count
FROM penguins
GROUP BY species, island
ORDER BY species, island;
```

## Additional Guidance for These SQL Queries

1. Enter SQLite command line:
```bash
sqlite3 sandbox.db
```

2. For better output formatting, run these commands first:
```sql
.mode column
.headers on
```

3. To exit SQLite:
```sql
.quit
```

## Understanding the Results

- The ROUND() function is used to limit decimal places for readability
- COUNT(*) shows the number of records in each group
- Percentages are calculated by (tip/total_bill * 100)
- The CASE statements in the penguin queries create pivot-table-like results
