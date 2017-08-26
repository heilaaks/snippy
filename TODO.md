## TODO
   - [ ] Add import functionality from json and yaml files.
   - [ ] Add tests for console and file outputs to verify list handling in tags and links.
   - [ ] Update documents
   - [ ] Add support for cutting log string with low logging levels. Long lines are nasty and meant for debugging.
   - [ ] Avoid string formatting when passing the log string to logger. Pass just the parameters for performance.
   - [ ] Add text log what was done. The default log level is error so no logs at all. A bit more info is better.
   - [ ] Refactor database tests to use dictionary format for the test rows.

## DONE
   - [x] Add support for categories that allow grouping snippets into larger groups.
   - [x] Add command line option --debug to elevate the debug level and set the default level to error.
   - [x] Support text format export on top of yaml and json.
   - [x] Support multiline command snippets.
   - [x] Support input from editor.
   - [x] Change tags to behave like links in exported yaml and json files. Keep console output of tags as string.
   - [x] Fixed argument testing and printing for tags and find arguments
