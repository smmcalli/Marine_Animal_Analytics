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
