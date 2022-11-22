fx_version 'cerulean'
game 'gta5'

author 'VIRUXE'
description 'This resource finds all the vehicles by their folder name, processes the name and adds vehicle names to the game.'
repository 'https://github.com/VIRUXE/fivem-vehicle_loader/'

client_script 'client.lua' -- Mainly just asks the server for the vehicle names and loads them into the game
server_script 'Server.net.dll' -- Finds out what vehicles exist in the resource, stores and sends them to the client

files {
    '**/*.meta'
}

data_file 'HANDLING_FILE'          '**/handling.meta'
data_file 'VEHICLE_METADATA_FILE'  '**/vehicles.meta'
data_file 'CARCOLS_FILE'           '**/carcols.meta'
data_file 'VEHICLE_VARIATION_FILE' '**/carvariations.meta'
data_file 'VEHICLE_LAYOUTS_FILE'   '**/vehiclelayouts.meta'
data_file 'VEHICLE_SHOP_DLC_FILE'  '**/dlctext.meta'
data_file 'CARCONTENTUNLOCKS_FILE' '**/carcontentunlocks.meta'