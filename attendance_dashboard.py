import pandas as pd
import matplotlib.pyplot as plt

# Total students in class (edit if needed)
all_students = ["Sudha","Student2","Student3","Student4"]

# Read attendance file
data = pd.read_csv("attendance.csv", names=["Name","Date","Time"])

# Get today's attendance
today = data["Name"].unique().tolist()

present_students = today
absent_students = [s for s in all_students if s not in today]

present_count = len(present_students)
absent_count = len(absent_students)

print("\nPresent Students:")
for s in present_students:
    print(s)

print("\nAbsent Students:")
for s in absent_students:
    print(s)

print("\nTotal Present:", present_count)
print("Total Absent:", absent_count)

# Pie chart
labels = ["Present", "Absent"]
sizes = [present_count, absent_count]

plt.pie(sizes, labels=labels, autopct='%1.0f%%')
plt.title("Student Attendance Overview")

plt.show()