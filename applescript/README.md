## Modify the applescript path in omnifocus.task-fetcher.plist 
## Use launchctl to load and test it.

    launchctl load -w Library/LaunchAgents/omnifocus.task-fetcher.plist 
    launchctl start -w Library/LaunchAgents/omnifocus.task-fetcher

## If you change the plist file, you should first unload it:

    launchctl unload -w Library/LaunchAgents/omnifocus.task-fetcher.plist

## and then load it again.
