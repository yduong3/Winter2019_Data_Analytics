Sub StockData()

    ' --------------------------------------------
    ' LOOP THROUGH ALL SHEETS
    ' --------------------------------------------
    For Each ws In Worksheets
    
        ' Set an initial variable for holding value for summary table
        Dim Ticker As String

        Dim Total_Stock_Volume As Double
        Total_Stock_Volume = 0

        Dim Year_Open As Double
        Year_Open = ws.Cells(2, 3).Value
        
        Dim Year_Close As Double

        Dim Yearly_Change As Double

        Dim Percent_Change As Double

        ' Keep track of the location for each ticker symbol in the summary table
        Dim Summary_Table_Row As Double
        Summary_Table_Row = 2

        ' Add Header for summary table
        ws.Cells(1, 9).Value = "Ticker"
        ws.Cells(1, 10).Value = "Yearly Change"
        ws.Cells(1, 11).Value = "Percent Change"
        ws.Cells(1, 12).Value = "Total Stock Volume"

        ' Determine the Last Row 
        LastRow = ws.Cells(Rows.Count, 1).End(xlUp).Row

        ' Loop through stock data
        For i = 2 To LastRow

            ' Check if we are still within the same ticker symbol, if it is not...
            If ws.Cells(i + 1, 1).Value <> ws.Cells(i, 1).Value Then

                ' Set the Ticker
                Ticker = ws.Cells(i, 1).Value
                ws.Cells(Summary_Table_Row, 9).Value = Ticker

                ' Set Year Close
                Year_Close = ws.Cells(i, 6).Value

                ' Calculate yearly change
                Yearly_Change = Year_Close - Year_Open
                ws.Cells(Summary_Table_Row, 10).Value = Yearly_Change
                ws.Cells(Summary_Table_Row, 10).NumberFormat = "0.00"

                ' Calculate percent change
                If (Year_Open = 0 And Year_Close = 0) Then
                    Percent_Change = 0
                ElseIf (Year_Open = 0 And Year_Close <> 0) Then
                    Percent_Change = 1
                Else
                    Percent_Change = Yearly_Change / Year_Open
                    ws.Cells(Summary_Table_Row, 11).Value = Percent_Change
                    ws.Cells(Summary_Table_Row, 11).NumberFormat = "0.00%"
                End If

                ' Add to the Total Stock Volume
                Total_Stock_Volume = Total_Stock_Volume + ws.Cells(i, 7).Value
                ws.Cells(Summary_Table_Row, 12).Value = Total_Stock_Volume 

                ' Add one to the summary table row
                Summary_Table_Row = Summary_Table_Row + 1

                ' Reset 
                Total_Stock_Volume = 0
                Year_Open = Cells(i + 1, 3)

                ' If the cell immediately following a row is the same brand...
            Else

                ' Add to the Total Stock Volume
                Total_Stock_Volume = Total_Stock_Volume + ws.Cells(i, 7).Value

            End If
        
        Next i

        ' Determine the Last Row of Yearly Change per WS
        LastRow_YC = ws.Cells(Rows.Count, 9).End(xlUp).Row
        
        ' Set the Cell Colors
        For j = 2 To LastRow_YC

            If (ws.Cells(j, 10).Value > 0 Or ws.Cells(j, 10).Value = 0) Then
                ws.Cells(j, 10).Interior.ColorIndex = 10

            ElseIf ws.Cells(j, 10).Value < 0 Then
                ws.Cells(j, 10).Interior.ColorIndex = 3
            
            End If
        
        Next j

        ' Add Header for performance table
        ws.Cells(2, 15).Value = "Greatest % Increase"
        ws.Cells(3, 15).Value = "Greatest % Decrease"
        ws.Cells(4, 15).Value = "Greatest Total Volumn"
        ws.Cells(1, 16).Value = "Ticker"
        ws.Cells(1, 17).Value = "Value"

        ' Determine the Last Row for ticker
        LastRow_ticker = ws.Cells(Rows.Count, 9).End(xlUp).Row

        ' Loop through preformance stock data
        For i = 2 To LastRow_ticker

            'Look through each row to find min and max value
            If ws.Cells(i, 11).Value = Application.WorksheetFunction.Max(WS.Range("K2:K" & LastRow_ticker)) Then
                ws.Range("P2").Value = ws.Cells(i, 9).value
                ws.Range("Q2").value = ws.Cells(i, 11).value
                ws.Range("Q2").NumberFormat = "0.00%"

            ElseIf ws.Cells(i, 11).value = Application.WorksheetFunction.Min(WS.Range("K2:K" & LastRow_ticker)) Then
                ws.Range("P3").Value = ws.Cells(i, 9).value
                ws.Range("Q3").value = ws.Cells(i, 11).value
                ws.Range("Q3").NumberFormat = "0.00%"

            ElseIf ws.Cells(i, 12).value = Application.WorksheetFunction.Max(WS.Range("L2:L" & LastRow_ticker)) Then
                ws.Range("P4").Value = ws.Cells(i, 9).value
                ws.Range("Q4").value = ws.Cells(i, 12).value

            End if

        Next i

        'Autofit table columns
        ws.Columns("I:L").EntireColumn.Autofit
        ws.Columns("O:Q").EntireColumn.Autofit

    Next ws

End Sub
