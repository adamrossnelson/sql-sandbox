# Agg Functions Introduction

Reminder: By default the sqlite3 interactive environment won't include column names in its output. To activate display of the column names use the command `.headers on` which will make your output more readable.

## How To Study With This Guide

In SQL, aggregate functions perform calculations on multiple rows of data and return a single result. The five key aggregate functions are `SUM`, `COUNT`, `AVG` (average), `MIN` (minimum), and `MAX` (maximum). These are analogous to familiar operations in R or Python (e.g. `sum()`, `mean()`, `min()`, `max()` in R/Pandas). Each example will include the SQL query and a brief explanation of the result. Keep in mind that in SQL you often use these functions in combination with `GROUP BY` to aggregate within categories, similar to grouping operations in R (`dplyr::summarise()`) or Pandas (`groupby().agg()`).

## SUM

**What it does:** `SUM()` adds up all the values in a numeric column (or each group of rows). This is like using `sum(column)` in R or `df['column'].sum()` in pandas.

### 1. Total a Column 

Suppose we want the total of all bills in the `tips` dataset. What query would produce this result? 

```sql
-- Write a sql query here
```

This query calculates the sum of the `total_bill` column across all rows in the `tips` table. The result is a single number (the total revenue from all bills). For instance, if we execute this, we might find the total of all bills is around $4827.77. This matches what we would get by summing that column in a DataFrame or tibble.

### 2. Sum with Grouping

We can also sum values per category. For example, from the `mpg` dataset (car fuel efficiency data), we may want the total engine displacement by number of cylinders. What query would produce this result?

```sql
-- Write a sql query here
```

Here, SQL groups the rows by the `cylinders` value and then sums the `displacement` for each group. The output will list each unique cylinder count (e.g. 4, 6, 8) alongside the sum of displacements for cars with that many cylinders. This is similar to using `.groupby('cylinders')['displacement'].sum()` in pandas. For instance, you might see results like cylinders=4 having a large total displacement due to many 4-cylinder cars, etc. (The exact numbers depend on the dataset values.)

## COUNT

**What it does:** `COUNT()` returns the number of rows in a group. It can count all rows (`COUNT(*)`) or only non-null values of a column (`COUNT(column)`). This is analogous to R’s `length()` or `n()` in dplyr, or Python’s `len(df)` or `df['col'].count()`.

### 1. Counting rows

To find out how many records are in a table, use `COUNT(*)`. What query whould show how many entries are in each of our example tables?

```sql
-- Write a sql query here
```

This combined query (using `UNION ALL` to stack results) would produce a list of datasets with their total row counts. We expect to see that `tips` has 244 rows, `penguins` has 344 rows, and `mpg` has 398 rows (assuming the full MPG dataset). These counts correspond to what we know about the datasets (e.g., 244 tips records in one month, 344 penguin observations, etc.).

### 2. Count with grouping

Often we want counts per category. In SQL, we combine `COUNT()` with `GROUP BY`. For instance, in the `penguins` dataset what query will show the number of penguins birds of each species?
  
```sql
-- Write a sql query here
```

This will give a count for each species. The result should show three rows (one for each species of penguin): Adélie – 152, Gentoo – 124, Chinstrap – 68. This matches the known distribution of the Palmer penguins species in the data. In a similar way, in pandas one might do `df.groupby('species').size()` to get these counts.

**Note:** If you want to count unique values, SQL provides `COUNT(DISTINCT column)`. For example, `SELECT COUNT(DISTINCT day) FROM tips;` would tell us how many distinct days are present in the tips data (which should be 4). This is similar to using `nunique()` in pandas or `unique()` in R.

## AVG (Average)

**What it does:** `AVG()` computes the arithmetic mean of a numeric column. In R you might use `mean(column)`, and in Python `df['column'].mean()`.

### 1. Average value 

Find the average total bill amount in the `tips` dataset. What query would produce this result?

```sql
-- Write a sql query here
```

This calculates the mean of all `total_bill` values. The result is a single number. Based on the data, the average bill is about $19.79. In other words, on average people spent around $19.79 per meal. This aligns with what we’d get by computing the mean in R/Python.

### 2. Average value with grouping

We can make this more interesting by grouping. Suppose we want the average bill *by day* of the week. What query will produce result?

```sql
SELECT day, AVG(total_bill) AS avg_bill
FROM tips
GROUP BY day;
```

This query returns the average bill for each day (Thursday, Friday, Saturday, Sunday). For instance, you might find that *aturday has the highest average bill and Friday the lowest (since Friday had fewer, possibly smaller parties). This is analogous to `df.groupby('day')['total_bill'].mean()` in pandas. Each row of the result would show a day and the average bill amount for that day.

## MIN

**What it does:** `MIN()` gives the smallest value in a column (per group if grouped). This is like `min(column)` in R or `df['column'].min()` in pandas.

### 1. Minimum value

Let’s find the smallest (`MIN`) and largest (`MAX`) total bill in the `tips` dataset. We can actually do both in one query for convenience. What query will produce this result?

```sql
-- Write a sql query here
```

This will return two numbers – the minimum and maximum of the `total_bill` column. According to the data, the minimum bill was $3.07 and the maximum bill was $50.81. So the cheapest diner spent \$3.07, and the most expensive bill was $50.81. In Python or R you’d get these with simple min/max functions on the list of total bills.

### 2. Minimum value with grouping

We can also get the minimum of a column within each category. For example, in the `mpg` dataset, suppose we want the minimum miles-per-gallon for cars of each cylinder count. What query will produce this result?

```sql
-- Write a sql query here
```

This yields the lowest MPG value for each cylinder group. Perhaps, 8-cylinder cars have a lowest MPG around (maybe ~9 MPG), 4-cylinder cars might have a higher minimum (perhaps ~18 MPG), etc., reflecting that some big engines are gas guzzlers. This is similar to doing `df.groupby('cylinders')['mpg'].min()` in pandas.

## MAX

**What it does:** `MAX()` returns the largest value in a column (per group if grouped). It’s the opposite of MIN. Think of `max(column)` in R or `df['column'].max()` in pandas.

### 1. Maximum value

Using the same query we showed above, we already obtained the maximum total bill from the `tips` data as $50.81. We can do a separate example for variety: what is the heaviest car in the `mpg` dataset? What query would produce this result?

```sql
-- Write a sql query here
```

In this query, `MAX(weight)` finds the highest weight value. (We include the `name` just to see which car it is – though in practice, selecting non-aggregated columns like that works if that column is functionally dependent on the max or if we use more advanced techniques like subqueries. For simplicity, assume the heaviest weight is unique so this returns the car name as well.) The result might show, for example, a weight around 5000+ lbs for some large 70s American car. In pandas you might identify this by `df['weight'].max()`.

### 2. MAX with grouping

Similarly to MIN, we can find the max within categories. For instance, in the `penguins` data, we could find the maximum bill length for each species. What query would produce this result?

```sql
-- Write a sql query here
```

This will list each species and the longest bill recorded for that species. For example, perhaps Gentoo penguins have the longest bill length among the three species. Such a query is analogous to `df.groupby('species')['bill_length_mm'].max()` in Python.

## Summary

To recap, SQL’s aggregate functions let us easily compute totals, counts, averages, minima, and maxima across our data. They become especially powerful when combined with `GROUP BY` to yield summary statistics for each subgroup in the data (much like tapply in R or groupby in pandas). We saw examples using the tips dataset (summing revenue, averaging bills, finding min/max tips), the mpg dataset (counting cars, summing displacement, grouping by cylinders), and the penguins dataset (counting species, averaging sizes, etc.). These functions are fundamental for exploratory data analysis in SQL – analogous to using summary statistics in other tools. With these, you can derive insights such as *“which category has the highest total or average?”*, *“how many items fall into each group?”*, *“what’s the range of values in this column?”*, and so on, all within your database query.

Experiment by modifying the queries or applying multiple aggregates at once. For example, you can select `COUNT(*), AVG(col), MIN(col), MAX(col)` all in one query to get a full summary of a column. This flexibility makes SQL a powerful tool for data analysis, even for those coming from R/Python backgrounds – the concepts carry over closely, only the syntax differs. Happy querying!
