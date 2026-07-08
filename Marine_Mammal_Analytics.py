#preprocess data: removing excesss
from datetime import datetime
with open('C:/Users/sammi/Downloads/MML_AEP_Marine Mammal Food Habits Reference Collection, 1995-2018.csv','r') as f:
        f=f.readlines()
        #print(len(f))                          #1008 data points before cleaning data
        header=(f[0])
        header=header.split(',')
        len(header)

        species=[]                              #want to draw conclusions on how many different types of bones have been recorded
        need_to_edit=[]                         # notes which datasets have missing values
        check=[]                                #checkingmissing values organized by column header
        for i in range(1,len(f)):
            f[i]=f[i].split(',')
            if f[i][6] not in species:
                species.append(f[i][6])
            if len(f[i])!=19:
                need_to_edit.append(i)
            if (f[i][9])!='':
                check.append(i)
        for i in range(0,len(need_to_edit)-4):
            f[need_to_edit[i]][2]=f[need_to_edit[i]][2]+f[need_to_edit[i]][3]
            f[need_to_edit[i]].pop(3)
        need_to_edit=need_to_edit[-4:]
        f.pop(669) #removing unusable data
        f.pop(617)
        f.pop(607)
        f.pop(604)
        f.pop(1004)

#check:
#0:1008 1:993 2:918 3:1006 4:1005 5:1005 6:1000 7:847 8:198 9:682 10:35 11:317 12:189 13:104 14:62 15:97 16:13 17:65 18:993
#removing all columns with <33% of the data filled because they do not have enough information for me to obtain useful results
#of what type of prey are consumed. As stated in my writeup, these columns do list crutial information as I am looking mostly at species and size.
#columns 0-7,9 will be used


        year_cat=[]                                #looking at dates. I adjust to datetime later in code
        month_cat=[]
        day_cat=[]
        date_splt_list=[]
        for i in range(1,len(f)):
            f[i]=f[i][0:10]
            f[i].pop(8)
            f[i][1]=f[i][1][0:10]
            date_splt=f[i][1].split('-')
            date_splt_list.append(date_splt)
        for i in range(0,len(date_splt_list)):
            if len(date_splt_list[i][0])!=4:
                date_splt_list[i]=[0000]
            year=int(date_splt_list[i][0])
            year_cat.append(year)


        f.pop(0)                                    #separating header from rest of data
        header=header[0:10]
        header.pop(8)

        verified = []  # looping through the data to find the columns with multiple verifiers
        bone = []
        family1 = []
        genus1 = []
        species1 = []
        cona1 = []
        species2 = []
        genus2 = []
        fam1 = []
        for i in range(0, len(f)):
            if f[i][2] == '"L.Lehman K.Hughes"':
                f[i][2] = 'L.Lehman K.Hughes'
                x = f[i][2].split(' ')
                y = [f[i][0], f[i][0]]
                for g in range(0, 1):
                    verified = verified + x
            else:
                verified.append(f[i][2])
                y = [f[i][0]]
            bone = bone + y
            # f[i].pop(2)
            fam = f[i][3]
            if (
            fam,) not in family1:  # looping through data to make dictionaries for other tables in order to comply with 3NF
                family1.append((fam,))
            if fam not in fam1:
                fam1.append(fam)

            # f[i].pop(3)
            gen = f[i][4]
            if gen not in genus1:
                genus1.append(gen)
            spe = f[i][5]
            if spe not in species1:
                species1.append(spe)
                genus2.append(gen)
            cn = f[i][6]
            if cn not in cona1:
                cona1.append(cn)
                species2.append(spe)
        gen = []
        fam = []
        spe = []
        gen2 = []
        cona = []
        spe2 = []
        for i in range(0, len(f)):
            if f[i][4] not in gen:
                gen.append(f[i][4])
                fam.append(f[i][3])
            if f[i][5] not in spe:
                gen.append(f[i][5])
                gen2.append(f[i][4])
            if f[i][6] not in cona:
                cona.append(f[i][6])
                spe2.append(f[i][5])
        del f[i][4]
        del f[i][2]
        fa = range(1, len(family1))
        s = range(1, len(species2))

        family_fk_lookup = dict(zip(fam1, fa))
        species_lookup = dict(zip(species2, s))
        genus_lookup = dict(zip(genus2, s))
        values_ver = zip(bone, verified)
        genfam_list = [family_fk_lookup.get(item, item) for item in fam]
        genus_vals = list(zip(genus1, genfam_list))

        spefam_list = [genus_lookup.get(item, item) for item in gen2]
        species_vals = list(zip(species1, spefam_list))

        cona_list = [species_lookup.get(item, item) for item in spe2]
        cona_vals = list(zip(cona1, cona_list))
        data = f  # removing data from other tables from data needed for records table
        for i in range(0,len(data)):                 #removing data from other tables from data needed for records table
            data[i].pop(5)
            data[i].pop(4)
            data[i].pop(3)
            data[i].pop(2)
        yearlist=[]                                 #making columns for year, month, and day
        monthlist=[]
        daylist=[]
        for row in data:
            date_cat = row[1]
            if date_cat:
                date_obj = datetime.strptime(date_cat, '%Y-%m-%d')
                year = date_obj.year
                month = date_obj.month
                day = date_obj.day
            else:
                year, month, day = 0000, 00, 00       # Set to None if date is empty
            yearlist=yearlist+[year]
            monthlist=monthlist+[month]
            daylist= daylist+[day]

        for i in range(0,len(data)):
            data[i].append(yearlist[i])
            data[i].append(monthlist[i])
            data[i].append(daylist[i])
        data.pop(1002)
print(cona_vals)

#making sure the data base is fresh/clearing db
import sqlite3
conn = sqlite3.connect('finals2.db')
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

for table in tables:
    table_name = table[0]
    cursor.execute(f"DELETE FROM {table_name};")
    conn.commit()
conn.close()

import sqlite3
import pandas as pd
conn = sqlite3.connect('finals2.db')
def create_family(conn):
    cursor = conn.cursor()
    clr_sql='''DROP TABLE IF EXISTS family;'''
    sql_fam='''
        CREATE TABLE family (
        familyID INTEGER PRIMARY KEY AUTOINCREMENT,
        familyName TEXT NOT NULL
        )'''
    insert_fam='''
        INSERT INTO Family (familyName)
        VALUES (?)
        '''
    with conn:
        conn.execute(clr_sql)
        cursor.execute(sql_fam)

        cursor.executemany(insert_fam, family1)
        conn.commit()

        cursor.execute('SELECT * FROM family')
    return pd.read_sql_query("""SELECT * FROM Family""", conn)
family=create_family(conn)
family

conn = sqlite3.connect('finals2.db')
def create_genus(conn):
    clr_sql='''DROP TABLE IF EXISTS genusName;'''
    sql_gen_table='''
        CREATE TABLE genusName (
        genusID INTEGER PRIMARY KEY AUTOINCREMENT,
        genus TEXT NOT NULL,
        familyID INTEGER,
        FOREIGN KEY (familyID) REFERENCES family(familyID)
        )'''
    insert_sql ='''
        INSERT INTO genusName (genus, familyID)
        VALUES (?,?)
        '''
    with conn:
        cursor = conn.cursor()
        cursor.execute(clr_sql)
        cursor.execute(sql_gen_table)
        cursor.executemany(insert_sql, genus_vals)
        #conn.commit()
    return pd.read_sql_query("""SELECT * FROM genusName""", conn)
genus=create_genus(conn)
genus

conn = sqlite3.connect('finals2.db')
def create_species(conn):
    clr_sql='''DROP TABLE IF EXISTS species;'''
    sql_spe_table='''
    CREATE TABLE IF NOT EXISTS species (
    speciesID INTEGER PRIMARY KEY AUTOINCREMENT,
    species TEXT NOT NULL,
    genusID INTEGER,
    FOREIGN KEY (genusID) REFERENCES genus(genusID)
    )'''
    insert_spe='''
    INSERT INTO species (species, genusID)
    VALUES (?,?)
    '''
    with conn:
        cursor = conn.cursor()
        cursor.execute(clr_sql)
        cursor.execute(sql_spe_table)
        cursor.executemany(insert_spe, species_vals)
        conn.commit()
    return pd.read_sql_query("""SELECT * FROM species""", conn)



species=create_species(conn)
species

conn = sqlite3.connect('finals2.db')
def create_commonname(conn):
    conn = sqlite3.connect('finals2.db')
    clr_sql='''DROP TABLE IF EXISTS commonName;'''
    create_ver_sql='''
        CREATE TABLE IF NOT EXISTS commonName (
        cnID INTEGER PRIMARY KEY AUTOINCREMENT,
        common_name TEXT NOT NULL,
        speciesID INTEGER,
        FOREIGN KEY (speciesID) REFERENCES species(speciesID)
        )'''
    insert_sql_verifications = '''
        INSERT INTO commonName (common_name, speciesID)
        VALUES (?, ?)
        '''
    with conn:
        cursor = conn.cursor()
        cursor.execute(clr_sql)
        cursor.execute(create_ver_sql)
        cursor.executemany(insert_sql_verifications, cona_vals)
    return pd.read_sql_query("""SELECT * FROM commonName""", conn)

commonName=create_commonname(conn)
commonName

conn = sqlite3.connect('finals2.db')
def create_verified(conn):
    conn = sqlite3.connect('finals2.db')
    clr_sql='''DROP TABLE IF EXISTS verified;'''
    create_ver_sql='''
        CREATE TABLE verified (
        verificationID INTEGER PRIMARY KEY AUTOINCREMENT,
        bone INTEGER,
        verified_by TEXT
        )'''
    insert_sql_verifications = '''
        INSERT INTO verified (bone, verified_by)
        VALUES (?, ?)
        '''
    with conn:
        cursor = conn.cursor()
        cursor.execute(clr_sql)
        cursor.execute(create_ver_sql)
        cursor.executemany(insert_sql_verifications, values_ver)
    return pd.read_sql_query("""SELECT * FROM verified""", conn)

verified=create_verified(conn)

conn = sqlite3.connect('finals2.db')
def create_records(conn):
    clr_sql='''DROP TABLE IF EXISTS records;'''
    sql_table='''
        CREATE TABLE IF NOT EXISTS records(
        boneID INTEGER PRIMARY KEY AUTOINCREMENT,
        bone TEXT,
        date_cat TEXT,
        common_name TEXT,
        sl_cm REAL,
        wt_gm REAL,
        year INTEGER,
        month INTEGER,
        day INTEGER
        )
        '''
    insert_sql = '''
    INSERT INTO records (bone, date_cat, common_name, sl_cm, wt_gm, year, month,day)
    VALUES (?, ?, ?, ?, ?, ?, ?,?)
    '''
    with conn:
        cursor = conn.cursor()
        cursor.execute(clr_sql)
        cursor.execute(sql_table)
        cursor.executemany(insert_sql, data)
    length=[]
    for i in range(0,len(data)):
        if len(data[i])!=8:
            length.append(data[i])


    return pd.read_sql_query("""SELECT * FROM records""", conn)

records=create_records(conn)
records

#determing outliers that are present (and will be removed later)
import numpy as np
df=records
df.replace("", np.nan, inplace=True)
df['sl_cm'] = pd.to_numeric(df['sl_cm'], errors='coerce')
df=df.dropna()
sorted_by_year = df.sort_values(by='year', ascending=True)
#whats up with 2004
len_2004 = df[df['year'] == 2004]['sl_cm']
#print(len_2004)

Q1 = sorted_by_year['sl_cm'].quantile(0.25)
Q3 = sorted_by_year['sl_cm'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
filtered_df = sorted_by_year[(sorted_by_year['sl_cm'] >= lower_bound) & (sorted_by_year['sl_cm'] <= upper_bound)]


records=filtered_df.groupby('year')['sl_cm'].mean() #with outlier from 2004 removed
OGmean_len_by_yr=df.groupby('year')['sl_cm'].mean()


import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


def fetch_data_wt():
    conn = sqlite3.connect('finals2.db')
    query = '''
    SELECT year, AVG(wt_gm) AS avg_wt_gm
    FROM records
    WHERE year >= 1970 AND year IS NOT NULL  -- Ensure data is from 1970 onwards
    GROUP BY year
    ORDER BY year;
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def plot_histogram(df, year_range):
    filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

    plt.figure(figsize=(10, 6))
    plt.bar(filtered_df['year'], filtered_df['avg_wt_gm'], color='lightgreen', edgecolor='black')
    plt.xlim(year_range[0], year_range[1])
    plt.xticks(range(year_range[0], year_range[1] + 1, 5))
    plt.title('Average WT_GM per Year')
    plt.xlabel('Year')
    plt.ylabel('Average WT_GM')

    st.pyplot(plt)


def main():
    st.title('WT_GM Data Visualization')

    df = fetch_data_wt()

    year_range = st.slider(
        'Select year range',
        min_value=int(df['year'].min()),
        max_value=int(df['year'].max()),
        value=(int(df['year'].min()), int(df['year'].max())),
        step=1,
        key = 'weight_slider'
    )

    plot_histogram(df, year_range)

if __name__ == "__main__":
    main()

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


def fetch_data_sl():
    conn = sqlite3.connect('finals2.db')
    query = '''
    SELECT year, AVG(sl_cm) AS avg_sl_cm
    FROM records
    WHERE year >= 1970 AND year IS NOT NULL  -- Ensure data is from 1970 onwards
    GROUP BY year
    ORDER BY year;
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def plot_histogram(df, year_range):
    filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

    plt.figure(figsize=(10, 6))
    plt.bar(filtered_df['year'], filtered_df['avg_sl_cm'], color='skyblue', edgecolor='black')
    plt.xlim(year_range[0], year_range[1])
    plt.xticks(range(year_range[0], year_range[1] + 1, 5))
    plt.title('Average SL_CM per Year')
    plt.xlabel('Year')
    plt.ylabel('Average SL_CM')

    st.pyplot(plt)


def main():
    st.title('SL_CM Data Visualization')

    df = fetch_data_sl()

    year_range = st.slider(
        'Select year range',
        min_value=int(df['year'].min()),
        max_value=int(df['year'].max()),
        value=(int(df['year'].min()), int(df['year'].max())),
        step=1,
        key='length_slider'
    )

    plot_histogram(df, year_range)


if __name__ == "__main__":
    main()


def fetch_family_data():
    conn = sqlite3.connect('finals2.db')
    query = '''
    SELECT familyName, COUNT(*) AS family_count
    FROM family
    GROUP BY familyName
    ORDER BY family_count DESC;
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def plot_pie_chart(df):
    plt.figure(figsize=(8, 8))
    colors = plt.cm.Paired.colors[:len(df)]
    wedges, texts, autotexts = plt.pie(
        df['family_count'],
        labels=df['familyName'],
        autopct='%1.1f%%',
        startangle=90,
        colors=colors
    )
    plt.title('Family Distribution in the Database')
    plt.legend(wedges, df['familyName'], title="Family", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    plt.tight_layout()
    st.pyplot(plt)

def main():
    st.title('Family Distribution Pie Chart')
    df_family = fetch_family_data()
    plot_pie_chart(df_family)

#if __name__ == "__main__":
 #   main()

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


def fetch_family_bone_count():
    conn = sqlite3.connect('finals2.db')
    query = '''
    SELECT f.familyName, COUNT(r.boneID) AS bone_count
    FROM family f
    LEFT JOIN genusName g ON f.familyID = g.familyID
    LEFT JOIN species s ON g.genusID = s.genusID
    LEFT JOIN commonName cn ON s.speciesID = cn.speciesID
    LEFT JOIN records r ON cn.common_name = r.common_name
    GROUP BY f.familyName
    ORDER BY bone_count DESC;
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def fetch_family_bone_count():
    conn = sqlite3.connect('finals2.db')
    query = '''
    SELECT f.familyName, COUNT(r.boneID) AS bone_count
    FROM family f
    LEFT JOIN genusName g ON f.familyID = g.familyID
    LEFT JOIN species s ON g.genusID = s.genusID
    LEFT JOIN commonName cn ON s.speciesID = cn.speciesID
    LEFT JOIN records r ON cn.common_name = r.common_name
    GROUP BY f.familyName
    ORDER BY bone_count DESC;
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


def plot_family_bone_chart(df, selected_families, min_bone_count):
    filtered_df = df[df['familyName'].isin(selected_families) & (df['bone_count'] >= min_bone_count)]

    plt.figure(figsize=(10, 6))
    plt.bar(filtered_df['familyName'], filtered_df['bone_count'], color='lightgreen', edgecolor='black')
    plt.xlabel('Family Name')
    plt.ylabel('Number of Bones')
    plt.title('Number of Bones per Family')
    plt.xticks(rotation=90)
    plt.tight_layout()
    st.pyplot(plt)


def main():
    st.title('Interactive Family and Bone Distribution')

    df_family_bones = fetch_family_bone_count()

    all_families = df_family_bones['familyName'].tolist()

    selected_families = st.multiselect(
        'Select Families to Display',
        options=all_families,
        default=all_families
    )

    min_bone_count = st.slider(
        'Select Minimum Number of Bones to Display',
        min_value=int(df_family_bones['bone_count'].min()),
        max_value=int(df_family_bones['bone_count'].max()),
        value=int(df_family_bones['bone_count'].min()),
        step=1
    )

    if selected_families:
        plot_family_bone_chart(df_family_bones, selected_families, min_bone_count)
    else:
        st.write("Please select at least one family.")


if __name__ == "__main__":
    main()


#Part 5 machine learning attempt
def fetch_family_bone_count():
    conn = sqlite3.connect('finals2.db')
    query = '''
    SELECT f.familyName, COUNT(r.boneID) AS bone_count
    FROM family f
    LEFT JOIN genusName g ON f.familyID = g.familyID
    LEFT JOIN species s ON g.genusID = s.genusID
    LEFT JOIN commonName cn ON s.speciesID = cn.speciesID
    LEFT JOIN records r ON cn.common_name = r.common_name
    GROUP BY f.familyName
    ORDER BY bone_count DESC;
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def plot_family_bone_chart(df):
    plt.figure(figsize=(10, 6))
    plt.bar(df['familyName'], df['bone_count'], color='lightgreen', edgecolor='black')
    plt.xlabel('Family Name')
    plt.ylabel('Number of Bones')
    plt.title('Number of Bones per Family')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

def main():
    df_family_bones = fetch_family_bone_count()
    plot_family_bone_chart(df_family_bones)

if __name__ == "__main__":
    main()

#streamlit run EASfinalDash.py