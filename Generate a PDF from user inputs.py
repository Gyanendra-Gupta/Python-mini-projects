# This code generates a PDF report summarizing a student's attendance, including a table with total days,present days,
# absent days, and attendance percentage. It also includes a bar graph visually representing the student's 
# attendance over the given days (green for present, red for absent).

import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import os

# Function to generate the graph for attendance
def generate_attendance_graph(attendance_data, student_name):
    # Data for plotting
    days = list(attendance_data.keys())
    attendance = list(attendance_data.values())
    
    # Create the plot
    plt.figure(figsize=(6, 4))
    
    # Define colors: Green for Present (1), Red for Absent (0)
    colors = ['green' if status == 1 else 'red' for status in attendance]
    
    # Plot the attendance data
    plt.bar(days, attendance, color=colors, label=f"Attendance of {student_name}")
    
    plt.title(f"Attendance for {student_name}")
    plt.xlabel("Days")
    plt.ylabel("Attendance (1=Present, 0=Absent)")
    plt.grid(True)
    
    # Add a legend
    plt.legend(["Present (1)", "Absent (0)"])
    
    # Save the plot to a BytesIO object
    img_stream = BytesIO()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)
    plt.close()
    return img_stream

# Function to generate the PDF with attendance data and visualization
def generate_pdf_for_teacher_and_student(student_name, teacher_name, present_days, absent_days):
    # Generate attendance data (Day 1, Day 2, ... for total days)
    total_days = present_days + absent_days
    attendance_data = {f"Day {i+1}": 1 for i in range(present_days)}
    attendance_data.update({f"Day {i+1+present_days}": 0 for i in range(absent_days)})

    # Calculate attendance summary
    days_present = present_days
    days_absent = absent_days
    attendance_percentage = (days_present / total_days) * 100
    
    # File path for the generated PDF
    file_path = f"{student_name}_attendance.pdf"
    
    # Create a canvas object for PDF generation
    c = canvas.Canvas(file_path, pagesize=letter)
    
    # Set title and font for the PDF
    c.setTitle(f"Attendance Report for {student_name}")
    c.setFont("Helvetica", 12)
    
    # Add student and teacher information
    c.drawString(100, 750, f"Attendance Report for {student_name}")
    c.drawString(100, 730, f"Teacher: {teacher_name}")
    
    # Add attendance summary in a table-like format
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, 710, "Attendance Summary:")
    
    # Table headers
    c.setFont("Helvetica", 10)
    c.drawString(100, 690, "Total Days")
    c.drawString(200, 690, "Days Present")
    c.drawString(300, 690, "Days Absent")
    c.drawString(400, 690, "Attendance %")
    
    # Table values
    c.drawString(100, 670, str(total_days))
    c.drawString(200, 670, str(days_present))
    c.drawString(300, 670, str(days_absent))
    c.drawString(400, 670, f"{attendance_percentage:.2f}%")
    
    # Add graph for attendance
    img_stream = generate_attendance_graph(attendance_data, student_name)
    
    # Save the image stream to a temporary file
    temp_image_path = "temp_attendance_graph.png"
    with open(temp_image_path, "wb") as temp_file:
        temp_file.write(img_stream.read())
    
    # Add the image to the PDF
    c.drawImage(temp_image_path, 100, 400, width=400, height=200)  # Adjust the position and size as needed
    
    # Save the PDF
    c.save()
    
    # Remove the temporary image file after adding it to the PDF
    os.remove(temp_image_path)
    
    print(f"PDF generated successfully: {file_path}")

# Example usage
student_name = input("Enter student name: ")
teacher_name = input("Enter teacher name: ")

# Input how many days the student is present and absent
present_days = int(input("Enter how many days the student is present: "))
absent_days = int(input("Enter how many days the student is absent: "))

generate_pdf_for_teacher_and_student(student_name, teacher_name, present_days, absent_days)
