# Greymind Animation Custom Data
Animation custom data manager with Maya exporter and C# importer

# Features
Creates a custom data node on objects in Maya that holds:
* Animation clip information - name, min frame, max frame
* First-person camera mount
* Character forward
* Grenade launch mount
* Idle animation name
* Scale
* Joint names - chest, neck, left toe, right toe

# Installation
Place the `CustomDataExporter.py` and `Common.py` files in `Documents\maya\<maya version>\scripts` folder.

# Usage

## Export
To invoke this script, use the following commands in the python mode of the script editor:
```
import CustomDataExporter as Cde
reload(Cde)
Cde.Run()
```
You may middle-mouse drag these lines to the shelf to create a shortcut toolbar button.

## Import
Copy all the files to your project and use the `Save` and `Load` functions in `CustomData`.

# Greymind Sequencer
You might also want the sequencer tool to manage animations. You can get it from [https://github.com/greymind/Sequencer](https://github.com/greymind/Sequencer)

# Team
* [Balakrishnan (Balki) Ranganathan](http://greymind.com)

# License
* MIT
