# Marine_Animal_Analytics

__Dataset:__

“National Oceanic and Atmospheric Administration, Department of Commerce - Marine 
  Mammal Food Habits Reference Collection, 1995-2018.” Catalog, Responsible Party 
  (Point of Contact, Custodian), 1 Apr. 2024, catalog.data.gov/dataset/marine-mammal-food
  habits-reference-collection-1995-20181. 

This dataset contains records of bone fragments recovered from the stomach contents and excrement of marine mammals. Records include taxonomic classifications, specimen measurements, collection dates, and verification information.

__Project Overview:__

Marine mammals such as cetaceans and pinnipeds play important roles in ocean ecosystems, and several species are considered keystone species. Understanding the prey species that make up their diets can help identify important feeding grounds and ecosystems that may benefit from conservation efforts. 
This project analyzes the NOAA Marine Mammal Food Habits Reference Collection (1995–2018), which contains records of bone fragments recovered from the stomach contents and excrement of marine mammals. The dataset includes taxonomic information, specimen measurements, collection dates, and verification records.

__Questions This Project Seeks to Answer:__

- What prey families are most commonly represented in marine mammal diets?
- How diverse are the prey species recorded in the collection?
- Have average prey size and weight changed over time?
- Can SQL and interactive visualizations help uncover ecological patterns within the dataset?

__Methods:__

Data Cleaning:
- Removed columns with insufficient data completeness
- Parsed datetime fields into year, month, and day
- Handled missing values
- Detected and removed statistical outliers using the IQR method

Analysis:
- SQL joins and aggregations
- Average length and weight calculations
- Trend analysis

__Demonstrated Experience:__
- Python
- Pandas
- NumPy
- SQLite
- SQL
- Matplotlib

__Key Findings:__
- The dataset contained approximately 80 unique prey families, demonstrating substantial dietary diversity among cetaceans and pinnipeds.
  - The taxonomic hierarchy revealed that a relatively small number of families accounted for a large proportion of identified prey specimens.
  - The family Tetragonuridae was the most frequently represented prey family within the collection, suggesting it is an important dietary component for the marine mammals represented in the dataset.
- SQL queries and visualizations display trends in length and weight of fragments with 2015 having a noticable increase in averages for weight and length.This stability may reflect sustained ecosystem productivity and the continued availability of suitable prey resources for cetaceans and pinnipeds.
- Outlier analysis identified records that substantially affected yearly averages, demonstrating the importance of data validation prior to interpretation.
