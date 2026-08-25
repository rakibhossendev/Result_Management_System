# Existing AI Assistant Tools - Descriptions & Test Prompts

## Tool Descriptions

### 1. `get_student_data` (by internal ID)
**Purpose**: Fetch a single student's complete profile using their internal database ID (`student_id`).
**Returns**: Student ID, roll number, full name, semester, group, CGPA, department info (name, code), teacher ID, principal ID.
**Scope**: Only students belonging to the requesting teacher.

### 2. `get_student_by_roll` (by roll number)
**Purpose**: Fetch a single student's complete profile using their human-facing roll number.
**Returns**: Same as `get_student_data` - all profile fields plus department information.
**Scope**: Only students belonging to the requesting teacher.
**Preferred for**: User-facing queries since roll numbers are what teachers/students know.

### 3. `get_student_attendance`
**Purpose**: Retrieve complete attendance history for one student.
**Returns**: Student profile (ID, roll, name) + list of attendance records (date, status).
**Scope**: Only attendance records for students belonging to the requesting teacher.

### 4. `get_student_marks`
**Purpose**: Retrieve all marks across all subjects and topics for one student.
**Returns**: Student profile + list of marks with subject name/code, topic name, full marks, and obtained marks.
**Scope**: Only marks for students belonging to the requesting teacher.

### 5. `get_class_attendance`
**Purpose**: Get attendance summary for an entire class (semester + group).
**Returns**: Class info + list of all students with total days, present days, and attendance percentage.
**Scope**: Only students in the specified class belonging to the requesting teacher.

### 6. `get_class_marks_summary`
**Purpose**: Get statistical summary of marks for an entire class.
**Returns**: Class info + subject-wise statistics (number of students, average, min, max obtained marks).
**Scope**: Only marks for the requesting teacher's students in that class.

---

## Test Prompts

### Individual Student Lookup

#### Testing `get_student_by_roll`:
- "Show me the profile of student with roll number 101"
- "Who is student with roll 101?"
- "Get details for student roll number 45"
- "What's the CGPA of student 101?"

#### Testing `get_student_data` (rarely triggered - model prefers roll):
- "Look up student with ID 5"
- "Get student data for student_id 12"

### Attendance Lookup

#### Testing `get_student_attendance`:
- "What's the attendance record for student roll 101?"
- "Show me attendance history of student 101"
- "How many days was student with roll 45 present?"
- "Has student 101 been absent recently?"

### Marks Lookup

#### Testing `get_student_marks`:
- "Show me all marks for student roll 101"
- "What did student 45 score in their subjects?"
- "Get the marks record for student 101"
- "How is student 45 performing in their exams?"

### Class-Level Attendance

#### Testing `get_class_attendance`:
- "What's the attendance percentage for semester 2 group A?"
- "Show me attendance summary for class 3B"
- "Which students in semester 1 group B have attendance issues?"
- "Give me attendance stats for semester 4, group A"

### Class-Level Marks Summary

#### Testing `get_class_marks_summary`:
- "Show marks summary for semester 2 group A"
- "What's the average score in each subject for class 3B?"
- "How is semester 1 group A performing overall?"
- "Give me subject-wise performance for class 2A"

### Multi-Tool Test Cases (tests tool selection accuracy)

1. **Ambiguous query**: "Tell me about student 101"
   - Should trigger `get_student_by_roll` (most common interpretation)

2. **Comparison request**: "Compare attendance and marks of student 45"
   - Should trigger both `get_student_attendance` and `get_student_marks`

3. **Class + specific data**: "Show me attendance for class 2A and also marks summary for the same class"
   - Should trigger both `get_class_attendance` and `get_class_marks_summary`

### Error Handling Tests

- "Show me student roll 999" (non-existent roll)
- "What's the attendance for student 999?"
- "Get class attendance for semester 10 group Z" (invalid class)
- "Show marks for semester 5 group X" (no students in class)

### Edge Cases

- "Attendance of roll 0" (invalid roll number)
- "Marks summary for group A" (missing semester)
- "Show semester 2 group" (missing group letter)
- "What about student 101 102?" (multiple students in one query)

---

## Expected Tool Call Mapping

| Test Prompt | Expected Tool | Key Arguments |
|------------|--------------|---------------|
| "Show student roll 101" | `get_student_by_roll` | `student_roll: 101` |
| "Attendance for 101" | `get_student_attendance` | `student_roll: 101` |
| "Marks of 101" | `get_student_marks` | `student_roll: 101` |
| "Class 2A attendance" | `get_class_attendance` | `semester: 2, group: "A"` |
| "Class 2A marks" | `get_class_marks_summary` | `semester: 2, group: "A"` |
| "Student 101 performance" | Could trigger multiple tools | Depends on context |

---

## Testing Checklist

1. **Start with simple queries** to verify each tool works independently.
2. **Test with real data** - use actual roll numbers from your database.
3. **Check scoping** - log in as different teachers and verify you only see your own students' data.
4. **Monitor console logs** - watch which tools Mistral chooses for each query.
5. **Test edge cases** - non-existent students, missing data, invalid inputs.
6. **Verify formatting** - make sure the AI's natural language response is readable and accurate.
7. **Test multi-turn** - ask follow-up questions like "What about student 102?" after a previous query.# Existing AI Assistant Tools - Descriptions & Test Prompts

## Tool Descriptions

### 1. `get_student_data` (by internal ID)
**Purpose**: Fetch a single student's complete profile using their internal database ID (`student_id`).
**Returns**: Student ID, roll number, full name, semester, group, CGPA, department info (name, code), teacher ID, principal ID.
**Scope**: Only students belonging to the requesting teacher.

### 2. `get_student_by_roll` (by roll number)
**Purpose**: Fetch a single student's complete profile using their human-facing roll number.
**Returns**: Same as `get_student_data` - all profile fields plus department information.
**Scope**: Only students belonging to the requesting teacher.
**Preferred for**: User-facing queries since roll numbers are what teachers/students know.

### 3. `get_student_attendance`
**Purpose**: Retrieve complete attendance history for one student.
**Returns**: Student profile (ID, roll, name) + list of attendance records (date, status).
**Scope**: Only attendance records for students belonging to the requesting teacher.

### 4. `get_student_marks`
**Purpose**: Retrieve all marks across all subjects and topics for one student.
**Returns**: Student profile + list of marks with subject name/code, topic name, full marks, and obtained marks.
**Scope**: Only marks for students belonging to the requesting teacher.

### 5. `get_class_attendance`
**Purpose**: Get attendance summary for an entire class (semester + group).
**Returns**: Class info + list of all students with total days, present days, and attendance percentage.
**Scope**: Only students in the specified class belonging to the requesting teacher.

### 6. `get_class_marks_summary`
**Purpose**: Get statistical summary of marks for an entire class.
**Returns**: Class info + subject-wise statistics (number of students, average, min, max obtained marks).
**Scope**: Only marks for the requesting teacher's students in that class.

---

## Test Prompts

### Individual Student Lookup

#### Testing `get_student_by_roll`:
- "Show me the profile of student with roll number 101"
- "Who is student with roll 101?"
- "Get details for student roll number 45"
- "What's the CGPA of student 101?"

#### Testing `get_student_data` (rarely triggered - model prefers roll):
- "Look up student with ID 5"
- "Get student data for student_id 12"

### Attendance Lookup

#### Testing `get_student_attendance`:
- "What's the attendance record for student roll 101?"
- "Show me attendance history of student 101"
- "How many days was student with roll 45 present?"
- "Has student 101 been absent recently?"

### Marks Lookup

#### Testing `get_student_marks`:
- "Show me all marks for student roll 101"
- "What did student 45 score in their subjects?"
- "Get the marks record for student 101"
- "How is student 45 performing in their exams?"

### Class-Level Attendance

#### Testing `get_class_attendance`:
- "What's the attendance percentage for semester 2 group A?"
- "Show me attendance summary for class 3B"
- "Which students in semester 1 group B have attendance issues?"
- "Give me attendance stats for semester 4, group A"

### Class-Level Marks Summary

#### Testing `get_class_marks_summary`:
- "Show marks summary for semester 2 group A"
- "What's the average score in each subject for class 3B?"
- "How is semester 1 group A performing overall?"
- "Give me subject-wise performance for class 2A"

### Multi-Tool Test Cases (tests tool selection accuracy)

1. **Ambiguous query**: "Tell me about student 101"
   - Should trigger `get_student_by_roll` (most common interpretation)

2. **Comparison request**: "Compare attendance and marks of student 45"
   - Should trigger both `get_student_attendance` and `get_student_marks`

3. **Class + specific data**: "Show me attendance for class 2A and also marks summary for the same class"
   - Should trigger both `get_class_attendance` and `get_class_marks_summary`

### Error Handling Tests

- "Show me student roll 999" (non-existent roll)
- "What's the attendance for student 999?"
- "Get class attendance for semester 10 group Z" (invalid class)
- "Show marks for semester 5 group X" (no students in class)

### Edge Cases

- "Attendance of roll 0" (invalid roll number)
- "Marks summary for group A" (missing semester)
- "Show semester 2 group" (missing group letter)
- "What about student 101 102?" (multiple students in one query)

---

## Expected Tool Call Mapping

| Test Prompt | Expected Tool | Key Arguments |
|------------|--------------|---------------|
| "Show student roll 101" | `get_student_by_roll` | `student_roll: 101` |
| "Attendance for 101" | `get_student_attendance` | `student_roll: 101` |
| "Marks of 101" | `get_student_marks` | `student_roll: 101` |
| "Class 2A attendance" | `get_class_attendance` | `semester: 2, group: "A"` |
| "Class 2A marks" | `get_class_marks_summary` | `semester: 2, group: "A"` |
| "Student 101 performance" | Could trigger multiple tools | Depends on context |

---

## Testing Checklist

1. **Start with simple queries** to verify each tool works independently.
2. **Test with real data** - use actual roll numbers from your database.
3. **Check scoping** - log in as different teachers and verify you only see your own students' data.
4. **Monitor console logs** - watch which tools Mistral chooses for each query.
5. **Test edge cases** - non-existent students, missing data, invalid inputs.
6. **Verify formatting** - make sure the AI's natural language response is readable and accurate.
7. **Test multi-turn** - ask follow-up questions like "What about student 102?" after a previous query.

Remember that the model may occasionally call the wrong tool or combine multiple tools. If you see consistent issues with tool selection, you may need to refine the tool descriptions in `TOOLS_SCHEMA`.