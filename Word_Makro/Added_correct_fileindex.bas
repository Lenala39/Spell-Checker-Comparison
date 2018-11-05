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

    'Get directory to scan the files and Retrieve first file
    directory = "C:\Users\llangholf\Desktop\Files_to_process\"
    current_file = Dir(directory & "*.txt")
    'Set current_file = ActiveDocument
    
    ' while a file is returned for DIR-function above
    Do While current_file <> ""
        ' e.g. test = "C:\Users\llangholf\Desktop\Files\test.txt"
        test = directory & current_file
        
        ' open the selected file for Word
        my_doc = Documents.Open(test, Encoding:=msoEncodingCentralEuropean, Visible:=False)
        Set oDoc = Documents(my_doc)
        
        'split file content into single words
        single_words = Split(oDoc.Content, " ")

        ' Loop over all words in string
        For Counter = 0 To UBound(single_words)
            oDoc.Activate
            ' Get suggestions and check if written incorrectly
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
        
        Content = Join(single_words, " ") 're-join string again
        
        filename_components = Split(current_file, ".")
        file_index = filename_components(0)
        Debug.Print (file_index)
        
        ' WRITE CORRECTED FILE'
        'open file for output'
        file_name = directory & "Word\" & file_index & "_word.txt"
        
        Open file_name For Output As #1
            Print #1, Content ' Print because Write had " " around text
        Close #1

        
        current_file = Dir() 'loop over files in directory
    Loop 'Loop files
    
    Application.ScreenUpdating = True
End Sub
