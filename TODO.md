# TODO:
- work on the CandaGUI interface. This may help decide on many other structure decitions threwout the project.
- convert this to trello?
- readme?
- analysis routines?
- better logger
- USE PYLINT!!!


##### Panda module:
 - find out what the hell is up with Panda.can_recv()'s second return.
 - probaably wouldent hurt to see if there is documentation
   - might wana throw some doc strings in there maybe officaly 

##### CandaGUI:
 - panda connect startup screen
 - interface (probably decide on how that looks idono) [message id list with Names and values]
  - 8x8 binary square of the data of the selected id
 - make a child class of Datainfo to handle each data item output and have the stream distribute the data by id
 - malti bus support?
 - bit/nyb/byte/2byte delta indication (with sensativity)
 - frame frequency counter

##### DataInfo class
 - complete testing
 - prep to be a good parent
 - decide how to handle fractional (via DataInfo.maltiplyer) numbers and text output in relation to bin and hex values