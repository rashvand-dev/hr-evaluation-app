"""
1. FUNCTION Initialize_Database
        [INPUTS: Session_State]
        [OUTPUTS: DB_Names, DB_Role, DB_Experience, DB_Quality, DB_Teamwork, DB_Responsibility, DB_Key_Skills]
        1.1 IF Session_State.DB does not exist THEN
                1.2 DB_DataFrame = Create_DataFrame_With_Default_Employees_And_Skills()
                1.3 Save DB_DataFrame to Session_State.db
        1.4 ENDIF
        1.5 RETURN Null
1.6 ENDFUNCTION

2. FUNCTION Manage_Database
        [INPUTS: Action, Target_Name, New_Role, New_Exp, New_Q, New_T, New_R, New_Skills]
        [OUTPUTS: Updated_DB]
        2.1 IF Action == "Add_Update" AND Target_Name is not empty THEN
                2.2 REMOVE existing record where Name == Target_Name
                2.3 APPEND New_Row (Name, Role, Exp, Quality, Teamwork, Responsibility, Key_Skills) to DB
        2.4 ENDIF
        2.5 IF Action == "Delete" AND Target_Name is not empty THEN
                2.6 REMOVE record where Name == Target_Name
        2.7 ENDIF
        2.8 RETURN Updated_DB
2.9 ENDFUNCTION

3. FUNCTION Calculate_Performance_Weighted
        [INPUTS: Quality, Teamwork, Responsibility, W_Quality, W_Teamwork, W_Responsibility]
        [OUTPUTS: Weighted_Average, Status]
        3.1 Total_Weight = W_Quality + W_Teamwork + W_Responsibility
        3.2 IF Total_Weight == 0 THEN
                3.3 RETURN 0.0, "Error"
        3.4 ENDIF
        3.5 Weighted_Average = ((Quality * W_Quality) + (Teamwork * W_Teamwork) + (Responsibility * W_Responsibility)) / Total_Weight
        3.6 IF Weighted_Average >= 80 THEN
                3.7 Status = "عالی"
        3.8 ELSE IF Weighted_Average >= 60 THEN
                3.9 Status = "متوسط"
        3.10 ELSE THEN
                3.11 Status = "نیازمند بهبود"
        3.12 ENDIF
        3.13 RETURN Weighted_Average, Status
3.14 ENDFUNCTION

4. FUNCTION Generate_AI_Report
        [INPUTS: Name, Role, Exp, Skills, Average, Status]
        [OUTPUTS: AI_Report]
        4.1 Prompt = Construct_Detailed_HR_Prompt(Name, Role, Exp, Skills, Average, Status)
        4.2 Try connect to OpenAI API using GapGPT Base_URL and API_Key
        4.3 Response = Send Chat Completion Request (Model: "gpt-4o-mini", System_Role: "HR Manager", User_Prompt: Prompt)
        4.4 AI_Report = Extract text from Response or set error message if exception occurs
        4.5 RETURN AI_Report
4.6 ENDFUNCTION

5. FUNCTION Save_Word_Report
        [INPUTS: Name, Role, Exp, Skills, Average, Status, AI_Report]
        [OUTPUTS: Word_File_Bytes]
        5.1 Word_Doc = Create_New_Document()
        5.2 Add_Right_Aligned_Heading(Word_Doc, "گزارش رسمی ارزیابی عملکرد")
        5.3 Add_Right_Aligned_Paragraph(Word_Doc, Employee_Details_Text)
        5.4 Add_Right_Aligned_Heading(Word_Doc, "تحلیل هوش مصنوعی:")
        5.5 FOR EACH line IN AI_Report split by newline DO
                5.6 Add_Right_Aligned_Paragraph(Word_Doc, line)
        5.7 ENDFOR
        5.8 Word_File_Bytes = Save_Document_To_Memory_BytesIO(Word_Doc)
        5.9 RETURN Word_File_Bytes
5.10 ENDFUNCTION

6. MAIN
        [PURPOSE: System Execution Flow]
        6.1 CALL Initialize_Database()
        6.2 W_Quality, W_Teamwork, W_Responsibility <-- Sidebar Sliders Input
        6.3 Mode <-- Sidebar Radio Input ("صفحه وضعیت ارزیابی کارکنان", "مدیریت پایگاه داده", "ورود دستی")
        6.4 IF Mode == "مدیریت پایگاه داده" THEN
                6.5 Display Database DataFrame
                6.6 New inputs (Name, Role, Exp, Quality, Teamwork, Responsibility, Skills) <-- Form Input
                6.7 IF Save Button Clicked THEN
                        6.8 CALL Manage_Database("Add_Update", ...)
                6.9 ENDIF
                6.10 IF Delete Button Clicked THEN
                        6.11 CALL Manage_Database("Delete", ...)
                6.12 ENDIF
        6.13 ELSE IF Mode == "صفحه وضعیت ارزیابی کارکنان" OR Mode == "ورود دستی" THEN
                6.14 IF Mode == "صفحه وضعیت ارزیابی کارکنان" THEN
                        6.15 Name_Input <-- Selectbox from DB Names
                        6.16 Load Employee Row Data from DB
                6.17 ELSE
                        6.18 Manual Inputs (Name, Role, Exp, Skills, Quality, Teamwork, Responsibility) <-- Input fields
                6.19 ENDIF
                6.20 IF Employee Data Found/Valid THEN
                        6.21 Display Employee Summary Info
                        6.22 IF Evaluate Button Clicked THEN
                                6.23 Team_Avg = MEAN(All numeric scores in DB)
                                6.24 Weighted_Average, Status = CALL Calculate_Performance_Weighted(...)
                                6.25 Display Metrics (Quality, Teamwork, Responsibility, Weighted_Average with Benchmark Difference)
                                6.26 Display Status with appropriate color/message (Success/Warning/Error)
                                6.27 AI_Report = CALL Generate_AI_Report(Name, Role, Exp, Skills, Weighted_Average, Status)
                                6.28 Display AI_Report inside Styled Box (".ai-output-box")
                                6.29 Word_Bytes = CALL Save_Word_Report(...)
                                6.30 Render Download Button for Word Report (.docx)
                        6.31 ENDIF
                6.32 ELSE
                        6.33 Display info message to select/enter employee and stop execution
                6.34 ENDIF
        6.35 ENDIF
6.36 ENDMAIN
"""