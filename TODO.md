## TODO
   - [ ] Make delete to work with the snippet digest instead of database rown number.
   - [ ] Add docker container for the project.
   - [ ] Add tests for console and file outputs to verify list handling in tags and links.
   - [ ] Update documents
   - [ ] Add support for cutting log string with low logging levels. Long lines are nasty and meant for debugging.
   - [ ] Avoid string formatting when passing the log string to logger. Pass just the parameters for performance.
   - [ ] Add text log what was done. The default log level is error so no logs at all. A bit more info is better.
   - [ ] Add update job.
   - [ ] Add default values from optional arguments to editor template.
   - [ ] Using UTF-8 currently. Check if Unicode would be possible for example with vi editor input.

## DONE
   - [x] Added hashes to identify snippets.
   - [x] Changed database tests to use dictionary format.
   - [x] Changed command line arguments to be more suitable for resolve cases as well.
   - [x] Added import functionality from json and yaml files.
   - [x] Added support for categories that allow grouping snippets into larger groups.
   - [x] Added command line option --debug to elevate the debug level and set the default level to error.
   - [x] Added text format export on top of yaml and json.
   - [x] Added multiline command snippets.
   - [x] Added input from editor.
   - [x] Changed tags to behave like links in exported yaml and json files. Keep console output of tags as string.
   - [x] Fixed argument testing and printing for tags and find arguments
