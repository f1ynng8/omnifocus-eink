property beginTaskPerspectiveName : "待办事项"
property dueTaskPerspectiveName : "今日截止"
property beginTaskFile : "<file path>" -- it's like "macOS::Users:<yourname>:Project:calender-omnifocus:bgeintask.ini"
property dueTaskFile : "<file path>" 
property scpCmd : "<scp cmd string>" -- it's like  "scp -i /Users/MyName/key /Users/MyName/Project/calender-omnifocus/*.ini MyName@IP:/opt/calendar/bin/tasks/"

on run {}
	set readyTaskList to {}
	tell application "OmniFocus"
		tell front document window of default document to set its perspective name to beginTaskPerspectiveName
		tell content of front document window of default document to set taskList to (value of every leaf)
		set currentTime to short date string of (current date) & " " & time string of (current date)
		my WriteStringToFile(("[Info]" & "
"), beginTaskFile, false)
		my WriteStringToFile(("Last update time=" & currentTime & "
"), beginTaskFile, true)
		my WriteStringToFile(("[Tasks]" & "
"), beginTaskFile, true)
		repeat with theTask in taskList
			set deferDateString to defer date of theTask as string
			set dueDateString to (due date of theTask) as string
			if (deferDateString is not "missing value") then
				set deferTime to text 17 thru 21 of deferDateString
			else
				set deferTime to "null"
			end if
			if (dueDateString is not "missing value") then
				set dueTime to text 17 thru 21 of dueDateString
			else
				set dueTime to "null"
			end if
			my WriteStringToFile((id of theTask & "=" & name of theTask & "|" & deferTime & "|" & dueTime & "
"), beginTaskFile, true)
		end repeat
		
		tell front document window of default document to set its perspective name to dueTaskPerspectiveName
		tell content of front document window of default document to set taskList to (value of every leaf)
		my WriteStringToFile(("[Info]" & "
"), dueTaskFile, false)
		my WriteStringToFile(("Last update time=" & currentTime & "
"), dueTaskFile, true)
		my WriteStringToFile(("[Tasks]" & "
"), dueTaskFile, true)
		repeat with theTask in taskList
			set deferDateString to defer date of theTask as string
			set dueDateString to (due date of theTask) as string
			if (deferDateString is not "missing value") then
				set deferTime to text 17 thru 21 of deferDateString
			else
				set deferTime to "null"
			end if
			if (dueDateString is not "missing value") then
				set dueTime to text 17 thru 21 of dueDateString
			else
				set dueTime to "null"
			end if
			my WriteStringToFile((id of theTask & "=" & name of theTask & "|" & deferTime & "|" & dueTime & "
"), dueTaskFile, true)
		end repeat
	end tell
	do shell script (scpCmd)
end run

on GetTaskFromPerspectiveAndWriteToFile(PerspectiveName, FileName)
	try
	end try
end GetTaskFromPerspectiveAndWriteToFile

on WriteStringToFile(this_data, target_file, append_data) -- (string to write, file path as string, boolean status append or not)
	try
		set the target_file to the target_file as text
		set the open_target_file to ¬
			open for access file target_file with write permission
		if append_data is false then ¬
			set eof of the open_target_file to 0
		write this_data to the open_target_file starting at eof as «class utf8»
		close access the open_target_file
		return true
	on error
		try
			close access file target_file
		end try
		return false
	end try
end WriteStringToFile
