import os
import errno
from os import walk

def createIni(MODS_DIR, HOME_DIR, IGNORE_MODS):
    RESOURCE_MAP = [
        {
            'filename': 'sResourceStartUpArchiveList',
            'mods': [
                'BakaFile - Main.ba2',
                'IconTag.ba2',
                'IconSortingRatmonkeys.ba2',
                'MMM - Country Roads.ba2',
                            'ImpUlt.ba2',
                            'Quizzless Apalachia.ba2'
                ],
            'default_mods': [
                'SeventySix - Interface.ba2',
                'SeventySix - Localization.ba2',
                'SeventySix - Shaders.ba2',
                'SeventySix - Startup.ba2'
                ],
            'found_mods': []
        },
        {
            'filename': 'sResourceArchiveList2',
            'mods': [
                'ShowHealth.ba2',
                'MoreWhereThatCameFrom.ba2',
                'Prismatic_Lasers_76_Lightblue.ba2',
                'OptimizedSonar.ba2',
                'Silentchameleon.ba2',
                'CleanPip.ba2',
                'classicFOmus_76.ba2',
                'nootnoot.ba2',
                'MenuMusicReplacer.ba2',
                'BullBarrel.ba2',
                            'EVB76NevernudeFemale - Meshes.ba2',
                            'EVB76NevernudeFemale - Textures.ba2',
                            'EVB76NevernudeMale - Meshes.ba2',
                            'EVB76NevernudeMale - Textures.ba2',
                            'EVB76 - Meshes.ba2',
                            'EVB76 - Textures.ba2',
                            'EVB76Nevernude - Meshes.ba2',
                            'EVB76Nevernude - Textures.ba2',
                            'BoxerShorts.ba2',
                            'MaleUnderwear.ba2',
                            'FemaleUnderwear.ba2',
                            'PerkLoadoutManager.ba2'
                ],
            'default_mods': [
                'SeventySix - Animations.ba2',
                'SeventySix - EnlightenInteriors.ba2',
                'SeventySix - GeneratedTextures.ba2',
                'SeventySix - EnlightenExteriors01.ba2',
                'SeventySix - EnlightenExteriors02.ba2'
                ],
            'found_mods': []
        },
        {
            'filename': 'sResourceIndexFileList',
            'mods': [
                'UHDmap.ba2',
                'EnhancedBlood - Textures.ba2',
                'EnhancedBlood - Meshes.ba2',
                'MapMarkers.ba2',
                'Radiant_Clouds.ba2',
                'SpoilerFreeMap.ba2',
                ],
            'default_mods': [
                'SeventySix - Textures01.ba2',
                'SeventySix - Textures02.ba2',
                'SeventySix - Textures03.ba2',
                'SeventySix - Textures04.ba2',
                'SeventySix - Textures05.ba2',
                'SeventySix - Textures06.ba2'
                ],
            'found_mods': []
        },
        {
            'filename': 'sResourceArchive2List',
            'mods': [
                'PerkLoadoutManager.ba2',
                'ChatMod.ba2',
            ],
            'default_mods': [
                            'SeventySix - 00UpdateMain.ba2',
                            'SeventySix - 01UpdateMain.ba2',
                            'SeventySix - 00UpdateStream.ba2',
                            'SeventySix - 01UpdateStream.ba2',
                            'SeventySix - 00UpdateTextures.ba2',
                            'SeventySix - 01UpdateTextures.ba2',
                            'SeventySix - MeshesExtra.ba2',
                            'SeventySix - 02UpdateMain.ba2',
                            'SeventySix - 03UpdateMain.ba2',
                            'SeventySix - 04UpdateMain.ba2',
                            'SeventySix - 02UpdateStream.ba2',
                            'SeventySix - 03UpdateStream.ba2',
                            'SeventySix - 04UpdateStream.ba2',
                            'SeventySix - 02UpdateTextures.ba2',
                            'SeventySix - 03UpdateTextures.ba2',
                            'SeventySix - 04UpdateTextures.ba2',
                            'SeventySix - GeneratedMeshes.ba2',
                            'SeventySix - StaticMeshes.ba2',
                            'SeventySix - 05UpdateMain.ba2',
                            'SeventySix - 06UpdateMain.ba2',
                            'SeventySix - 07UpdateMain.ba2',
                            'SeventySix - 05UpdateStream.ba2',
                            'SeventySix - 07UpdateStream.ba2',
                            'SeventySix - 05UpdateTextures.ba2',
                            'SeventySix - 06UpdateTextures.ba2',
                            'SeventySix - 07UpdateTextures.ba2'
                ],
            'found_mods': []
        },
    ]
    FILENAME = 'Fallout76Custom.ini'
    HOME_DIR = HOME_DIR + "\\" + FILENAME

    SR_2LIST_INDEX = 3
    # Create any missing folders
    if not os.path.exists(os.path.dirname(HOME_DIR)):
        try:
            os.makedirs(os.path.dirname(HOME_DIR))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    # Open the Custom.ini file for writing
#    CUSTOM_INI_FILE = open(HOME_DIR, "w+")
    CUSTOM_INI_FILE = open(os.path.dirname(os.path.abspath(__file__)) + "\\" + FILENAME, "w+")

    # write the section header to the file
    CUSTOM_INI_FILE.write("[Archive]\r\n")

    # Loop through the resource map and add mods to the correct places
    for (dirpath, dirnames, filenames) in walk(MODS_DIR):
        for file in filenames:
            # Make sure the file is not an official file (starts with "SeventySix")
            # and is a ba2 (file extension)
            if (file[0:10] != 'SeventySix' and file[-4:].lower() == '.ba2' and file not in IGNORE_MODS):
                FOUND = False
                for RESOURCE in RESOURCE_MAP:
                    if file in RESOURCE['mods']:
                        RESOURCE['found_mods'].append(file)
                        FOUND = True

                # If a mod doesn't appear in the one of the other mod lists, add it to the default
                if not FOUND:
                    RESOURCE_MAP[SR_2LIST_INDEX]['found_mods'].append(file)
        break

    # Loop through the resource map and add the correct lines to the ini file
    for RESOURCE in RESOURCE_MAP:
        if RESOURCE['found_mods']:
            # [TODO] Get the array intersection of the `mods` to the found mods
            # to make a sorted list based on what's in the map
            FOUND = frozenset(RESOURCE['found_mods'])
            MODS = RESOURCE['mods']
            MOD_LIST = [mod for mod in MODS if mod in FOUND]
            MOD_LIST = ', ' + ', '.join(MOD_LIST)

            # Get any mods that don't show up in the mods list (for the default list)
            DIFF_LIST = [item for item in FOUND if item not in MODS]
            if DIFF_LIST:
                DIFF_LIST.sort()
                DIFF_LIST = ', ' + ', '.join(DIFF_LIST)
            else:
                DIFF_LIST = ''

            # Make the default list a string
            DEFAULT_MODS = ', '.join(RESOURCE['default_mods'])

            CUSTOM_INI_FILE.write(
                RESOURCE['filename'] + " = %s\r\n"
                % (DEFAULT_MODS + MOD_LIST + DIFF_LIST)
            )

    CUSTOM_INI_FILE.close()

def findModFiles(MODS_DIR):
    mods_found = []

    for (dirpath, dirnames, filenames) in walk(MODS_DIR):
        for file in filenames:
            if (file[0:10] != 'SeventySix' and file[-4:].lower() == '.ba2'):
                mods_found.append(file)
        break

    
    return mods_found
