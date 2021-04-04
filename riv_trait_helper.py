from sims4.resources import Types, get_resource_key
import sims4.commands
import services
import sims4.tuning.instance_manager # contains class InstanceManager, of which traitim is an instance
import traceback
from sims4.localization import TunableLocalizedString, TunableLocalizedStringFactory
from sims4.hash_util import unhash
import random
from traits.traits import TraitType

# doing json thing
import json
import os
from pathlib import Path

# getting sim infos
from sims.sim_info import SimInfo
import sims.sim_info_manager

traitim = services.get_instance_manager(Types.TRAIT) # trait instance manager
traits64bit = [] # this list will have traits with 64bit IDs
traits32bit = [] # this list will have traits with 32bit IDs
traits64tmp = [] # this list will have the entries to remove from the .json file

# aim of this command: list all traits with 64 bit IDs
@sims4.commands.Command('64bit', command_type=sims4.commands.CommandType.Live)
def list_64bit_traits(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    output('going through traits in ' + str(traitim) + '...')
    try:
        for trait in traitim.types:
            trait_long = str(trait)
            trait_id = trait_long[10:-20] + trait_long[19:-10]
            # '00000000!abcdefab'cdefabcd'cb5fddc7'
            # -> abcdefabcdefabcd (string)
            trait_hex = int('0x' + trait_id, 16)
            # -> 0xabcdefabcdefabcd (number)
            # middle 16 digits (the ID) as a hexadecimal integer
            # int(string, base); hex just has it saved as 0x...
            actual_trait = traitim.get(get_resource_key(trait, Types.TRAIT))
            if actual_trait.trait_type == TraitType.PERSONALITY: # if the trait is a personality (CAS) trait
                if trait_hex > 0xffffffff: # this has a 64 bit ID
                    trait_tuple = (actual_trait, trait_hex)
                    # .display_name() on the first one for localised string
                    # no idea how to turn this hash into the actual string,,,
                    traits64bit.append(trait_tuple)
                    #output(str(trait_tuple[0]))
                else: # this has a 32 bit ID (i.e. it works!)
                        # middle 16 digits (the ID) as a hexadecimal integer
                        # int(string, base); hex just has it saved as 0x...
                    trait_tuple = (actual_trait, trait_hex)
                    traits32bit.append(trait_tuple)
        output('number of traits with 32bit IDs (safe): ' + str(len(traits32bit)) + ', including ' + str(random.choice(traits32bit)[0]))
        output('')  # leave this blank if translating
        for trait_tuple in traits32bit:
            output(str(trait_tuple))
        output('') # leave this blank if translating
        output('number of traits with 64bit IDs: ' + str(len(traits64bit)) + ', including ' + str(random.choice(traits64bit)[0]))
        output('') # leave this blank if translating
        for trait_tuple in traits64bit:
            output(str(trait_tuple))
        if len(traits64bit) > 0:
            output('traits with 64bit IDs found! you\'ll want to replace all of the above with updated versions.')
            file_dir = Path(__file__).resolve().parent.parent
            file_name = '64bit_traits.json'
            file_path = os.path.join(file_dir, file_name)
            if not os.path.isfile(file_path):
                output('enter 64bit_export to make the .json file with the sims and traits with 64bit IDs')
        else:
            output('no traits with 64bit IDs found! (you\'re all good - you only need this mod if you wanna swap traits later)')
    except:
        output(traceback.format_exc())

@sims4.commands.Command('64bit_export', command_type=sims4.commands.CommandType.Live)
def export_64bit_traits(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    file_dir = Path(__file__).resolve().parent.parent
    file_name = '64bit_traits.json'
    file_path = os.path.join(file_dir, file_name)

    if not os.path.isfile(file_path): # file does not exist, create
        # get that list
        output('exporting a list of (sim_id, old_trait_name, old_trait_id)...')
        export_list = []
        for trait_tuple in traits64bit:
            for sim in services.sim_info_manager().get_all():
                old_trait = trait_tuple[0]
                trait_id = trait_tuple[1]
                if sim.has_trait(old_trait):
                    export_list.append((sim.sim_id, str(old_trait), trait_id))
        output('found ' + str(len(export_list)) + ' instances that need to be replaced')

        # put the list in a json file
        with open(file_path, 'w') as json_file:
            json.dump(export_list, json_file)
        output('the sim ID and trait info has been exported to 64bit_traits.json!')
        output('to use this list, quit the game, replace the trait files, go back into this save, and run 64bit_replace')
    else: # file exists, update
        with open(file_path, 'r') as json_file:
            old_list = json.load(json_file)
        old_len = str(len(old_list))
        output('updating the .json file...')
        new_list = []
        for tuple_boi in old_list:
            if not tuple_boi in traits64tmp:
                new_list.append(tuple_boi) # put in the new list if it's in the old list and wasn't fixed this time
        new_len = str(len(new_list))
        with open(file_path, 'w') as json_file:
            json.dump(new_list, json_file)
        output('updated the .json file - gone from ' + old_len + ' to ' + new_len + ' entries!')

@sims4.commands.Command('32bit_export', command_type=sims4.commands.CommandType.Live)
def export_32bit_traits(_connection=None):
    output = sims4.commands.CheatOutput(_connection)

    # get that list
    output('exporting a list of (sim_id, trait_name, trait_id)...')
    export_list = []
    for trait_tuple in traits32bit:
        for sim in services.sim_info_manager().get_all():
            old_trait = trait_tuple[0]
            trait_id = trait_tuple[1]
            if sim.has_trait(old_trait):
                export_list.append((sim.sim_id, str(old_trait), trait_id))
    output('found ' + str(len(export_list)) + ' instances')

    # put the list in a json file
    file_dir = Path(__file__).resolve().parent.parent
    file_name = '32bit_traits.json'
    file_path = os.path.join(file_dir, file_name)
    # https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
    with open(file_path, 'w') as json_file:
        json.dump(export_list, json_file)
    output('the sim ID and trait info has been exported to 32bit_traits.json!')

@sims4.commands.Command('64bit_replace', command_type=sims4.commands.CommandType.Live)
def replace_64bit_traits(_connection=None):
    output = sims4.commands.CheatOutput(_connection)
    traits_list = []

    # with 32bit in the game, and 64bit_traits.json...
    output('attempting to swap trait pairs (where you have the 32bit in your mods folder, and 64bit_traits.json...)')
    file_dir = Path(__file__).resolve().parent.parent
    file_name = '64bit_traits.json'
    file_path = os.path.join(file_dir, file_name)
    if os.path.isfile(file_path):
        with open(file_path, 'r') as json_file:
            export_list = json.load(json_file)
        for tuple_boi in export_list:
            sim_id = tuple_boi[0]
            str_trait = tuple_boi[1]
            old_id = tuple_boi[2]
            for new_tuple_boi in traits32bit:
                new_trait = new_tuple_boi[0]
                if str(new_trait) == str_trait: # this is the one we wanna replace
                    sim = services.sim_info_manager().get(sim_id).sim_info # get the sim(info)
                    #old_trait = traitim.get(get_resource_key(old_id, Types.TRAIT))
                    #sim.remove_trait(old_trait) # not needed anymore bc old_trait will be in .json
                    sim.add_trait(new_trait)
                    output('trait replaced for {} {}: {}'.format(sim.first_name, sim.last_name, str_trait))
                    traits64tmp.append(tuple_boi)
                    traits_list = list(set(traits_list + [str_trait])) # only adds if new
                    break
        instances_replaced = len(traits64tmp)
        traits_replaced = len(traits_list)
        output('replaced all possible traits ({} traits, {} instances) - enter 64bit_export to remove these records from 64bit_traits.json'.format(str(traits_replaced), str(instances_replaced)))
    else:
        output('you don\'t have 64bit_traits.json (enter 64bit_export if you want to create this)')

@sims4.commands.Command('64bit_replace_id', command_type=sims4.commands.CommandType.Live)
def swap_traits(old_id: int, new_id: int, _connection=None):
    output = sims4.commands.CheatOutput(_connection)
    try:
        old_trait = traitim.get(get_resource_key(old_id, Types.TRAIT))
    except:
        old_trait = None
    new_trait = traitim.get(get_resource_key(new_id, Types.TRAIT))

    if not old_trait == None: # replace in game
        output('the old trait is still in the game! please use 64bit_export, quit, then remove the file(s) for the old trait')
    else: # replace from .json file
        output('the old trait is not in the game anymore. looking for .json file...')
        file_dir = Path(__file__).resolve().parent.parent
        file_name = '64bit_traits.json'
        file_path = os.path.join(file_dir, file_name)
        if os.path.isfile(file_path):
            sims_to_add_trait_to = []
            with open(file_path, 'r') as json_file:
                export_list = json.load(json_file)
            for tuple_boi in export_list:
                sim_id = tuple_boi[0]
                str_trait = tuple_boi[1]
                list_id = tuple_boi[2]
                if list_id == old_id:
                    sim = services.sim_info_manager().get(sim_id).sim_info  # get the sim(info)
                    sims_to_add_trait_to.append(sim)
                    break  # can go to next old_tuple_boi
            for sim in sims_to_add_trait_to:
                sim.add_trait(new_trait)
                output('trait replaced for {} {}: {}'.format(sim.first_name, sim.last_name, str_trait))
            output('replaced old traits with new ones - enter 64bit_export to update 64bit_traits.json')
        else:
            output('you don\'t have 64bit_traits.json (enter 64bit_export if you want to create this)')

    # also doesn't work:
    # for trait in traitim.types:
    # trait.id
    # trait.value
    # trait.name
    # trait.value()
    # trait.trait_id

    # doesn't work:
    # output(type(traitim))
    # output(str(type(traitim)))
    # for trait in traitim:
    # for trait in traitim.values:
    # for trait in traitim.values():
    # for trait in traitim.traits:
    # for trait in traitim.traits():
    # for trait in traitim.instances:
    # for trait in traitim.instances():