Attribute VB_Name = "NewMacros"
Sub Spelling_Correction()
'
' Spelling_Correction Macro
'
'

Dim Sugg As SpellingSuggestions
Dim AddSpace As String
Dim file_num As Integer

'Turn off Settings for Optimization
    Application.ScreenUpdating = False

    'Get directory to scan the files and retrieve first file
    directory = "F:\ManyFiles_cp1252\8\"
    current_file = Dir(directory & "*.txt")
    'Set current_file = ActiveDocument
    
    ' while a file is returned for DIR-function above
    Do While current_file <> ""
        ' e.g. test = "C:\Users\llangholf\Desktop\Files\test.txt"
        test = directory & current_file
        
        ' open the selected file for Word
        my_doc = Documents.Open(test, Encoding:=msoEncodingWestern, Visible:=False)
        Set oDoc = Documents(my_doc)
        
        'split file content into single words
        single_words = Split(oDoc.Content, vbCrLf) 'vbCrLf == \n

        ' Loop over all words in string
        For Counter = 0 To UBound(single_words)
            oDoc.Activate
            ' Get suggestions and check if written incorrectly
            On Error Resume Next
            Set Sugg = Application.GetSpellingSuggestions(single_words(Counter))
            
            ' If the SpellCheck returns False
            Dim correct As Boolean
            correct = Application.CheckSpelling(single_words(Counter))
            If Not correct Then
                If Sugg.Count <> 0 Then 'if suggestion available
                    corrected_word = Sugg(1).Name
                    single_words(Counter) = corrected_word 'assign the corrected version to word
                End If 'suggestion count-if
            End If 'spellchecking correct-if
        
        Next 'Loop counter for the words
        
        Content = Join(single_words, vbCrLf) 're-join string again
        
        ' get only index number of file
        filename_components = Split(current_file, ".")
        file_index = filename_components(0)
        Debug.Print (file_index)
        
        ' WRITE CORRECTED FILE'
        ' make file name
        file_name = "F:\ManyFiles_cp1252\Word_8\" & file_index & "_word.txt"
        
        'open file for output
        Open file_name For Output As #1
            Print #1, Content ' Print because Write had " " around text
        Close #1
        
        current_file = Dir() 'loop over files in directory
    Loop 'Loop files
    
    Application.ScreenUpdating = True
    
    
End Sub


Sub CloseAll()
' Close all open files

    Application.ScreenUpdating = False

    Do Until Documents.Count = 0
        Documents(1).Close SaveChanges:=wdDoNotSaveChanges
    Loop
    



End Sub
