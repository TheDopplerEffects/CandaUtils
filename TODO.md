# TODO:
- **work on the CandaGUI interface**
- **convert this to trello?**
- readme?
- routines for automating information detection? int/bool detection? update int/bool information with new data?
- better logger
- USE PYLINT!!!
- **dockstrings!!!!**

##### Canout:
 - rename
 - **implement DBC_reader**
 - ~~implement time reading on logger and Canout~~
 - message frequency counter

##### Panda module:
 - ~~find out what the hell is up with Panda.can_recv()'s second return.~~ probably a checksum but dosn't matter
 - ~~probaably wouldent hurt to see if there is documentation~~ None
   - **might wana throw some doc strings in there maybe officaly**
 - ~~allow message filtering at a lower level in the panda function~~ Done

##### CandaGUI:
 - **!!!!!!!!!!!BETTER FUCKING NAMES AND IDS!!!!!!!!!**
 - **panda connect startup screen**
 - AppJar SUCKS when it comes to syle options. this Is probably a good time to use a alternate GUI package ima go with Qt
 - ~~debug selection~~ **continue this**
 - interface (probably decide on how that looks idono)
   - 8x8 binary square of the data of the selected id
   - list of massages with a sublist of its signals
   - message selection expands/opens on a frame for editing and monipulating messages
   - Bar at top for most functions ex: add message, add signal, output styles 
     - ~~find a icon pack~~ (attribute Author!!!!!)
     	- <div>Icons made by <a href="https://www.flaticon.com/authors/kiranshastry" title="Kiranshastry">Kiranshastry</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
 - **implement DBC reading and formatting with DBC_reader**
 - malti bus support?
 - (may not be needed delay)maltiprocessing to replace thread
 - bit/nyb/byte/2byte delta indication (with sensativity)
 - ~~convert value display to be frequincy locked and write every output once per update~~
   - (may not be needed delay)make a buffer/lock to allow removing of massages missed by the main display loop. This may leave the message retrieving process open for logging?
 - frame frequency counter
 - (delay wait will external logger is finished)can logging

 - Issues
   - Meters update slowly and cause preformance issues
   - Connecting to panda prevents updating subwindow connection status Fix: send Connection to a thread
   - ~~Panda keeps filling up update queue buffer~~ remove queue all together but this is a quick fix and probably error prone 

##### ~~DataInfo class~~ Depricating

##### DBC_Reader:
### replace DataInfo with DBC_Reader
 - ~~DBC file parser~~
 - ~~signal class containing signal~~ info and decoder
   - **add abuility to change endian order**
   - **add sigh change**
   - add function binding to decode
     - 'singal.bind( func )' to bind a function and 'signal.execute(missageData)'
   - think about better names
 - ~~Message class containing message name and size + decoder~~ 
