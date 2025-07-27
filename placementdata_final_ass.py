import pandas as pd

# Load dataset
df = pd.read_csv(r"C:\Users\SHUBHA\Downloads\final_college_student_placement_dataset.csv")

# 1. Salary bands for placed students
placed_students = df[df['Placement'] == 'Placed'].copy()

def salary_band(salary):
    if salary < 300000:
        return 'Low'
    elif salary <= 600000:
        return 'Medium'
    else:
        return 'High'

placed_students['Salary_Band'] = placed_students['Salary'].apply(salary_band)
print("\n1. Salary bands for placed students:\n", placed_students[['College_ID', 'Salary', 'Salary_Band']])

# 2. Placement stats by gender and specialization
placement_rate = df.groupby(['Gender', 'Academic_Performance'])['Placement'].apply(lambda x: (x == 'Yes').mean())
average_salary = df[df['Placement'] == 'Yes'].groupby(['Gender', 'Academic_Performance'])['Salary'].mean()
avg_mba_score = df.groupby(['Gender', 'Academic_Performance'])['MBA_Percentage'].mean()

print("\n2. Placement Rate:\n", placement_rate)
print("\nAverage Salary (Placed only):\n", average_salary)
print("\nAverage MBA Score:\n", avg_mba_score)


# 3. Number of students with any missing values
missing_count = df.isnull().any(axis=1).sum()
print("3.Students with missing values:", missing_count)

# 4. Rows with missing salary
print("\n4.Rows with missing salary:")
print(df[df['Salary'].isnull()])

# 5. Students with complete records
complete_records = df.dropna()
print("\n5.Number of complete records:", complete_records.shape[0])

# 6. Duplicate student entries
duplicates = df[df.duplicated()]
print("\n6.Duplicate entries:")
print(duplicates)

# 7. Drop duplicates
df_no_duplicates = df.drop_duplicates()
print("\n7.Dataset shape after removing duplicates:", df_no_duplicates.shape)

# 8. Duplicates based on College_ID
id_duplicates = df[df.duplicated(subset='College_ID')]
print("\n8.Duplicates based on College_ID:")
print(id_duplicates)

# 9. Unique specializations
print("\n9.Unique specializations:", df['Academic_Performance'].unique())

# 10. Unique MBA scores
print("\n10.Unique MBA scores:", df['MBA_Percentage'].nunique())

# 11. Unique combinations of gender, specialization, and status
print("\n11.Unique gender-specialization-status combinations:",
      df[['Gender', 'Academic_Performance', 'Placement']].drop_duplicates().shape[0])

# 12. Average salary of placed students
print("\n12.Average salary of placed students:", df[df['Placement'] == 'Yes']['Salary'].mean())

# 13. Min and max CGPA
print("\n13.Min CGPA:", df['CGPA'].min(), "Max CGPA:", df['CGPA'].max())

# 14. Placed vs Unplaced count
print("\n14.Placement count:\n", df['Placement'].value_counts())

# 15. Stats by specialization
spec_summary = df.groupby('Academic_Performance').agg({
    'SSC_Percentage': 'mean',
    'MBA_Percentage': 'mean',
    'Placement': lambda x: (x == 'Yes').sum()
})
print("\n15.Specialization summary:\n", spec_summary)

# 16. Summary table
summary_table = pd.DataFrame({
    'Column': df.columns,
    'Null Count': df.isnull().sum().values,
    'Unique Count': df.nunique().values,
    'Duplicate Count': [df[col].duplicated().sum() for col in df.columns]
})
print("\n16.Summary Table:")
print(summary_table)
