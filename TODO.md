# TODO:
- work on the CandaGUI interface. This may help decide on many other structure decitions threwout the project.
- **convert this to trello?**
- readme?
- analysis routines?
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
  - debug selection
 - interface (probably decide on how that looks idono) [message id list with Names and values]
  - 8x8 binary square of the data of the selected id
 - **implement DBC reading and formatting with DBC_reader**
 - malti bus support?
 - maltiprocessing to replace thread
 - bit/nyb/byte/2byte delta indication (with sensativity)
 - convert value display to be frequincy locked and write every output once per update
  - make a buffer/lock to allow removing of massages missed by the main display loop. This may leave the message retrieving process open for logging?
 - frame frequency counter
   - Issues
    - Meters update slowly and cause preformance issues
    - ~~Panda keeps filling up update queue buffer~~ remove queue all together but this is a quick fix and probably error prone 
 - can Logging

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
 - 
