use launchctl to load and test it.

    launchctl load -w Library/LaunchAgents/omnifocus.task-fetcher.plist 
    launchctl start -w Library/LaunchAgents/omnifocus.task-fetcher

if you change the plist file, you should first unload it:

    launchctl unload -w Library/LaunchAgents/omnifocus.task-fetcher.plist

and then load it again.
