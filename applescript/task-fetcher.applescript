property beginTaskPerspectiveName : "待办事项"
property dueTaskPerspectiveName : "今日截止"
property taskFile : "path to task.ini" -- like macOS:Users:<your name>:task.ini
property scpCmd : "<scp command>" like "scp -i key task.ini username@Raspberry PI IP:/opt/calendar-omnifocus/tasks/"

on run {}
	if not ((do shell script "ping -o -t 1 <Raspberry PI IP>" & "&>/dev/null && echo yes || echo no") as boolean) then
		return "Raspberry Pi off-line"
	end if
	tell application "System Events"
		set activeApp to name of first application process whose frontmost is true
		if "OmniFocus" is in activeApp then
			return "Omnifocus is active"
		end if
	end tell
	tell application "OmniFocus"
		set lastSyncTime to last sync date of default document as string
		set allLines to paragraphs of (read file taskFile as «class utf8»)
		set Line2 to item 2 of allLines as text
		set lastSyncTimeWithKey to "Last sync time=" & lastSyncTime
		if (lastSyncTimeWithKey is equal to Line2) then
			return "not changed"
		end if
		tell front document window of default document to set its perspective name to beginTaskPerspectiveName
		tell content of front document window of default document to set taskList to (value of every leaf)
		--set currentTime to short date string of (current date) & " " & time string of (current date)
		my WriteStringToFile(("[Info]" & "
"), taskFile, false)
		my WriteStringToFile(("Last sync time=" & lastSyncTime & "
"), taskFile, true)
		my WriteStringToFile(("[BeginTasks]" & "
"), taskFile, true)
		repeat with theTask in taskList
			set deferDateString to defer date of theTask as string
			set dueDateString to (due date of theTask) as string
			if (deferDateString is not "missing value") then
				set deferTime to text of deferDateString
			else
				set deferTime to "null"
			end if
			if (dueDateString is not "missing value") then
				set dueTime to text of dueDateString
			else
				set dueTime to "null"
			end if
			my WriteStringToFile((id of theTask & "=" & name of theTask & "|" & deferTime & "|" & dueTime & "
"), taskFile, true)
		end repeat
		
		tell front document window of default document to set its perspective name to dueTaskPerspectiveName
		tell content of front document window of default document to set taskList to (value of every leaf)
		my WriteStringToFile(("[DueTasks]" & "
"), taskFile, true)
		repeat with theTask in taskList
			set deferDateString to defer date of theTask as string
			set dueDateString to (due date of theTask) as string
			if (deferDateString is not "missing value") then
				--	set deferTime to text 16 thru 20 of deferDateString
				set deferTime to text of deferDateString
			else
				set deferTime to "null"
			end if
			if (dueDateString is not "missing value") then
				set dueTime to text of dueDateString
			else
				set dueTime to "null"
			end if
			my WriteStringToFile((id of theTask & "=" & name of theTask & "|" & deferTime & "|" & dueTime & "
"), taskFile, true)
		end repeat
	end tell
	do shell script (scpCmd)
end run

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
	on error errStr number errorNumber
		try
			close access file target_file
		end try
		error errStr number errorNumber
		return false
	end try
end WriteStringToFile
