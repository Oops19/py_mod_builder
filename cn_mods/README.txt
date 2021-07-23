---
# README

This readme may be opened with a markdown viewer for a better visual experience.

### WARNING
Never ever delete the `Mods` (or `Mods-old`) folder as it contains your current mods. If you are unsure make a backup of the `Mods` folder before using this archive.

Do never ever extract this folder into an exiting `Mods` folder. It may lead to duplicate mods and mods may stop working.

### Version
This build has been tested and is for __VERSION__.
It should work with older and newer TS4 versions.

# Updating
If you used this mod before updating is quite save.
If there are any file starting with `cn_` in `Mods/_cn_/` please delete them. Initial versions didn`t strip the prefix properly. This step needs to be done one time.
(This commend will be removed in 2021-08.)

1. Navigate to `%USERPROFILE%\Documents\Electronic Arts\The Sims 4\` (1)
2. Extract the ZIP file there. It will overwrite the existing mod versions.
Extracting `mod_documentation` and `README.txt` is optional.

# Fresh Installation
If you have issues getting started with mods of ColonolNutty or want a simple way to update them use this archive.
Make sure that you either start with a fresh `Mods` folder or that you remove ALL mods of ColonolNutty you have installed.

### Clean setup
Navigate to `%USERPROFILE%\Documents\Electronic Arts\The Sims 4\` (1) and rename `Mods` to `Mods-old` or a similar name.
Do not rename it to `Nods` as it will be used for the planned auto-updater.
Do not rename it to `Mods.AutoSort` as it will be used for the planned auto-sorter.

### Installation
1. Make sure that no single mod of ColonolNutty is installed.
2. Extract the Mods folder of this archive into the current folder. This will result in this folder structure:
`%USERPROFILE%\Documents\Electronic Arts\The Sims 4\Mods\cn\` (3) (planned feature / CC)
`%USERPROFILE%\Documents\Electronic Arts\The Sims 4\Mods\_cn_\` (4)
`%USERPROFILE%\Documents\Electronic Arts\The Sims 4\Mods\Animations\` (5) (planned feature / auto-sort)
`%USERPROFILE%\Documents\Electronic Arts\The Sims 4\Mods\Poses\` (6) (planned feature / auto-sort)
`%USERPROFILE%\Documents\Electronic Arts\The Sims 4\Mods\mod_data\` (7)
`%USERPROFILE%\Documents\Electronic Arts\The Sims 4\mod_documentation\` (8)

Verify that in the `Mods` folder the two folders `_cn_` and `mod_data` exist.

Start the game and verify that the mods are loaded and work as expected. Then you may use the 50/50 method to copy or move other mods from `Mods-old` to the new `Mods` folder.
Older and newer TS4 versions should also work but can't be tested.

Planned feature to auto-sort mods:
Store animations in `%USERPROFILE%\Documents\Electronic Arts\The Sims 4\Mods\Animations\` (5).
Store poses in `%USERPROFILE%\Documents\Electronic Arts\The Sims 4\Mods\Poses\` (6).

## Folders for Mac:
1) $HOME/Documents/Electronic Arts/The Sims 4/
2) $HOME/Documents/Electronic Arts/The Sims 4/Mods
3) $HOME/Documents/Electronic Arts/The Sims 4/Mods/cn/
4) $HOME/Documents/Electronic Arts/The Sims 4/Mods/_cn_/
5) $HOME/Documents/Electronic Arts/The Sims 4/Mods/Animations/
6) $HOME/Documents/Electronic Arts/The Sims 4/Mods/Poses/
7) $HOME/Documents/Electronic Arts/The Sims 4/Mods/mod_data/
8) $HOME/Documents/Electronic Arts/The Sims 4/mod_documentation/


# Addendum

Usually it is save to update to a new TS4 version for these mods. The mods inject into the TS4 code with a robust design.
If you use also other mods please check https://forums.thesims.com/en_US/categories/mods before updating TS4.

### Naming of the archive
All name parts are separated with `_`
The first part describes the author and the content (eg ColonolNully-Patreon).
The second part is the date the supported TS4 version has been released (eg 2021-07-20). It`s the same for Win and Mac while the TS4 version is usually different.
For mods which often get updates a shortname and the version number may be appended.

### Sources
Sources and often also source code and documentation for developers:

AutoSave
n/a (in future: https://github.com/ColonolNutty/Sims4MiscMods)

Change Motives
https://github.com/ColonolNutty/Sims4MiscMods

Custom Gender Settings
https://github.com/ColonolNutty/CustomGenderSettings

Custom Slider Framework
https://github.com/ColonolNutty/CustomSliderFramework

Offer Blood
https://github.com/ColonolNutty/Sims4MiscMods

Outfit Customization
https://github.com/ColonolNutty/OutfitCustomization

Sims 4 Community Library
https://github.com/ColonolNutty/Sims4CommunityLibrary

Sims 4 Control Menu
https://github.com/ColonolNutty/Sims4ControlMenu

Sims 4 Mod Settings Menu
https://github.com/ColonolNutty/Sims4ModSettingsMenu

### Source Code
To build the zip archive this code is used: https://github.com/Oops19/cn_mods/

Depending on the built archive a different configuration file may have been used.

---