# trait-replacer-helper
source code for my trait replacer mod at https://rivforthesesh.itch.io/trait-replacer

# Changing an ID

If you have a trait that is no longer being updated and all you need for that is a new 32bit trait ID, look at this tutorial from zero: https://www.patreon.com/posts/tutorial-custom-31937410

# Using my trait replacer

To get started, please BACK UP YOUR SAVE, and make sure you do not remove the old trait files before starting, since the information on which sim has which trait will be lost, and my mod won't be any help.

This mod will create one new file in the same folder as the .ts4script called **64bit_traits.json**, which keeps a list of sim IDs and traits that have 64bit IDs, so the mod knows which ones to replace. When you update this file, it will only remove sim-trait pairs from the list that have been replaced in game (by this mod) - if you have multiple saves, you'll want to move this elsewhere when you try to replace traits in another save, since this file is specific to one save only. Once you're happy that you've taken out all 64bit traits and replaced them with 32bit traits, you can delete it.

- start the game and load into a lot
- open the console with ctrl+shift+C
- run 64bit to get the lists of 64bit and 32bit personality traits, and output these lists to the console (i struggled a bit accessing the localised strings, and the display name of a trait might be repeated anyway, so this is.. not formatted beautifully. despite this, it should be clear enough)
- run 64bit_export to make the file 64bit_traits.json in the same folder as the .ts4script - this will contain a list in the form [[sim_id, trait_name, old_trait_id],...], where the sim with sim_id has the trait trait_name with 64bit ID old_trait_id
- quit the game (saving is optional, because nothing has changed in the game)
- replace old file(s) in your Mods folder with the new file(s)
- reload the game and run 64bit again
- run 64bit_replace again. this will go through all of the entries in the .json file, and if it encounters one with the same name as a trait with a 32bit ID, then it will apply that 32bit ID to the sim
- run 64bit_export again to update 64bit_traits.json
- play the game!
- if you find any more updated traits later, just move/delete the .json file if needed and redo this section from the start

# What if the new trait has a different name?

This mod decides if two traits are the same by looking at their name within the game, but there are two workarounds for this: the first is a separate command with which you just enter two trait IDs, for the old trait to remove and the new trait to add. For every sim that had the trait with the first ID (and this info is saved in the .json file), it will add the trait with the second ID to that sim.

- enter 64bit_replace_id 1234 5678, where 1234 is the new ID and 5678 is the old ID.
- all sims with trait with ID 1234 will have it replaced by the trait with ID 5678
- if the old trait is not in the game but you have a .json file that says that sim had the trait with ID 1234, then they'll gain trait with ID 5678 - you'll want to run 64bit_export again in this case to update it afterwards
- save and quit
- remove old versions of replaced traits if you still have them in your Mods folder

Note about IDs: I know it works with base 10 (numbers as we know them - no letters, and does not start with 0x). Base 16 ones might work, e.g. entering 0x4d2 0x162e for this specific example, but I'd recommend going with base 10 anyway (you can use https://www.rapidtables.com/convert/number/hex-to-decimal.html to convert hex(16) to dec(10)).

The other workaround is just changing the trait name in the .json file to the new trait name! There's an extra command - 32bit_export - which is the exact same as creating a new 64bit_export file except it does the 32bit ones instead. This comes in handy for seeing the trait name (<class 'sims4.tuning.instances.TRAITNAME'>) and the new ID for use in either of these workarounds.
