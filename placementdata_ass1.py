import pandas as pd

# Load dataset
df = pd.read_csv(r"C:\Users\SHUBHA\Downloads\final_college_student_placement_dataset.csv")

# 1. Total number of students
print("1.Total students:", len(df))

# 2. Number of male and female students
print(df['Gender'].value_counts())

# 3. Average MBA percentage
print("3.Average MBA %:", df['MBA_Percentage'].mean())

# 4. Students scoring more than 80% in SSC and HSC
high_scorers = df[(df['SSC_Percentage'] > 80) & (df['HSC_Percentage'] > 80)]
print("4.Students scoring >80% in SSC & HSC:",high_scorers)


# 5. Students with prior work experience
experienced_students = df[df['Internship_Experience'] == 'Yes']
print("5.Students with prior work experience:",experienced_students)


# 6. Average MBA score per specialization
print(df.groupby('Specialization')['MBA_Percentage'].mean())

# 7. Count of placed vs not placed students
print(df['placement_success'].value_counts())

# 8. Placement ratio per specialization
placement_ratio = df.groupby('Specialization')['placement_success'].value_counts(normalize=True).unstack()
print("8.Placement ratio per specialization:",placement_ratio)
print(placement_ratio)

# 9. Create placement_success column
def classify(row):
    if row['placement_success'] == 'Placed':
        if row['Salary'] > 950000:
            return "High"
        elif row['Salary'] <= 400000:
            return "Average"
        else:
            return "Placed"
    return "Unplaced"

df['placement_success'] = df.apply(classify, axis=1)
print("Placement success classification:")
print(df[['placement_success', 'Salary', 'placement_success']])

# 10. Degree percentage range leading to highest avg salary (for placed students)
placed_df = df[df['placement_success'] == 'Placed']
bins = [0, 60, 70, 80, 90, 100]
labels = ['0-60', '60-70', '70-80', '80-90', '90-100']
placed_df['Degree Range'] = pd.cut(placed_df['CGPA'], bins=bins, labels=labels)
salary_by_range = placed_df.groupby('Degree Range')['Salary'].mean()
print("Average salary by degree percentage range:")
print(salary_by_range.sort_values(ascending=False))
