local debug = GetConvar('sv_lan', '0') == '1'

TriggerServerEvent('veh-load:vehicles') -- Triggers the server to send us the vehicle names

RegisterNetEvent('veh-load:vehicles', function (vehicles) -- Receives the vehicle names from the server
    if debug then print('Received vehicle names from server:\n' .. json.encode(vehicles, { indent = true })) end

    if not vehicles then return end -- If the server didn't send us any vehicles, don't do anything

    local loaded = 0 -- Counter for how many vehicles we've loaded
    for gameName, name in pairs(vehicles) do
        if debug then print(('Loading vehicle: "%s" (%s)'):format(name, gameName)) end
        AddTextEntry(tostring(gameName), name)
        loaded = loaded + 1
    end

    print(loaded .. (loaded > 1 and ' vehicles' or ' vehicle') .. ' loaded.')
end)