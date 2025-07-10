# String Manipulation Lessons

This guide walks through common string manipulation tasks using SQL queries on our sample datasets.

By default the sqlite3 interactive environment won't include column names in its output. To activate display of the column names use the command `.headers on` which will make your output more readable.

## How To Study With This Guide

For each task this guide provides both a description of a realistic string manipulation task and code in Python (Pandas) that will produce the desired result. Your task is to write SQL queries that accomplish the same result.

## MPG Dataset String Operations

### 1. Basic String Functions
Task: Extract manufacturer names from car names in the mpg dataset. The manufacturer is always the first word in the car name.

Here's how we'd do it in Python:
```python
>>> df = sns.load_dataset('mpg')
>>> df['name'].str.split().str[0].head()

0    chevrolet
1    buick
2    plymouth
3    amc
4    ford
Name: name, dtype: object
```

Proposed solution here:
```sql
SELECT DISTINCT
    SUBSTR(name, 1, INSTR(name || ' ', ' ') - 1) as manufacturer
FROM mpg
ORDER BY manufacturer;
```

### 2. Case Manipulation and Standardization
Task: Create a standardized view of the data where origin is in UPPERCASE and manufacturer (first word of name) is in Title Case.

Here's how we'd do it in Python:
```python
>>> df = sns.load_dataset('mpg')
>>> df.assign(
...     origin_upper=df['origin'].str.upper(),
...     maker_title=df['name'].str.split().str[0].str.title()
... ).head()

   origin origin_upper     maker_title
0    usa         USA      Chevrolet
1    usa         USA         Buick
2    usa         USA      Plymouth
3    usa         USA           Amc
4    usa         USA          Ford
```

Proposed solution here:
```sql
SELECT
    name,
    UPPER(origin) as origin_upper,
    UPPER(SUBSTR(name, 1, 1)) || UPPER(SUBSTR(name, 2, INSTR(name || ' ', ' ') - 2)) as maker_title
FROM mpg limit 5;
```

### 3. Pattern Matching with LIKE
Task: Find all cars that have either 'custom' or 'deluxe' in their names (case insensitive).

Here's how we'd do it in Python:
```python
>>> df = sns.load_dataset('mpg')
>>> df[df['name'].str.lower().str.contains(r'custom|deluxe')]

                                  name  mpg  cylinders  displacement  horsepower  \
27   ford galaxie 500 custom          14.0         8         351.0       153.0   
82   ford custom 500                  15.5         8         351.0       142.0   
89   chevrolet impala custom          13.0         8         350.0       165.0   
165  ford custom                      17.0         6         250.0       100.0   
```

Proposed solution here:
```sql
SELECT 
    name,
    mpg,
    cylinders,
    displacement,
    horsepower
FROM mpg
WHERE LOWER(name) LIKE '%custom%'
   OR LOWER(name) LIKE '%deluxe%'
ORDER BY name;
```

### 4. Advanced Pattern Matching with GLOB
Task: Find all cars whose names include a number (like '98' or '300').

Here's how we'd do it in Python:
```python
>>> df = sns.load_dataset('mpg')
>>> df[df['name'].str.contains(r'\d')][['name', 'mpg', 'cylinders', 'displacement', 'weight']].head(3)

                             name   mpg  cylinders  displacement  weight
1    buick skylark 320            15.0          8         350.0    3693
5    ford galaxie 500             15.0          8         429.0    4341
11   plymouth 'cuda 340           14.0          8         340.0    3609
```

Proposed solution here:
```sql
SELECT 
    name,
    mpg,
    cylinders,
    displacement,
    weight
FROM mpg
WHERE name GLOB '*[0-9]*'
ORDER BY name;
```

### 5. String Concatenation
Task: Create a full description combining year, origin, and name into a readable format.

Here's how we'd do it in Python:
```python
>>> df = sns.load_dataset('mpg')
>>> df.assign(
...     description=df['model_year'].astype(str) + ' ' + 
...                df['origin'].str.upper() + ' ' + 
...                df['name']
... ).head()

                          description
0  70 USA chevrolet chevelle malibu
1  70 USA buick skylark 320
2  70 USA plymouth satellite
3  70 USA amc rebel sst
4  70 USA ford torino
```

Alternatively a simpler approach would also work:

```python
>>> (df['model_year'].astype(str) + ' ' + df['name'] + ' ' + df['origin']).head(3)
```

Proposed solution here:
```sql
SELECT 
    model_year || ' ' || 
    UPPER(origin) || ' ' || 
    name as description
FROM mpg
LIMIT 5;
```

### 6. String Cleaning
Task: Clean car names by removing extra spaces and standardizing format (e.g., convert multiple spaces to single space).

Here's how we'd do it in Python:
```python
>>> df = sns.load_dataset('mpg')
>>> # Adding some extra spaces to demonstrate cleaning
>>> df['name'] = df['name'].apply(lambda x: '  ' + x + '   ')
>>> df['name'].str.strip().str.replace(r'\s+', ' ').head()

0    chevrolet chevelle malibu
1    buick skylark 320
2    plymouth satellite
3    amc rebel sst
4    ford torino
Name: name, dtype: object
```

Proposed solution here:
```sql
SELECT 
    TRIM(REPLACE(REPLACE(name, '  ', ' '), '  ', ' ')) as cleaned_name
FROM mpg
LIMIT 5;
```

### 7. String Length and Position
Task: Categorize car names by length into 'Short' (< 15 chars), 'Medium' (15-25 chars), or 'Long' (> 25 chars).

Here's how we'd do it in Python:
```python
>>> df = sns.load_dataset('mpg')
>>> def length_category(name):
...     length = len(name)
...     if length < 15:
...         return 'Short'
...     elif length <= 25:
...         return 'Medium'
...     else:
...         return 'Long'
>>> df.assign(name_category=df['name'].apply(length_category)).head(10)

                             name name_category
0  chevrolet chevelle malibu      Medium
1  buick skylark 320              Medium
2  plymouth satellite             Medium
3  amc rebel sst                  Short
4  ford torino                    Short
5  ford galaxie 500               Medium
```

Proposed solution here:
```sql
SELECT 
    name,
    LENGTH(name) as name_length,
    CASE 
        WHEN LENGTH(name) < 15 THEN 'Short'
        WHEN LENGTH(name) <= 25 THEN 'Medium'
        ELSE 'Long'
    END as name_category
FROM mpg
LIMIT 10;
```

## Additional Guidance

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

## Understanding String Functions in SQLite

- SUBSTR(X,Y,Z) extracts a substring from X starting at position Y with length Z
- INSTR(X,Y) finds the first occurrence of Y in X
- LENGTH(X) returns the number of characters in X
- TRIM(X) removes whitespace from both ends of X
- UPPER(X) and LOWER(X) change the case of X
- || is used for string concatenation
- REPLACE(X,Y,Z) replaces all occurrences of Y in X with Z

## Tips for Writing String Manipulation Queries

1. Always consider case sensitivity in your comparisons
2. Use TRIM() when comparing or matching strings that might have extra spaces
3. Combine multiple string functions to achieve more complex transformations
4. Test your queries with edge cases (empty strings, NULL values, etc.)
5. Use appropriate wildcards (% for LIKE, * for GLOB) based on your needs
