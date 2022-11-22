using System;
using System.Collections.Generic;
using System.Linq;
using System.IO;

using CitizenFX.Core;
using static CitizenFX.Core.Native.API;

namespace Server
{
    public class Main : ServerScript
    {
        readonly private bool debug = GetConvar("sv_lan", "0") == "true";

        private List<Vehicle> vehicles = new();

        public Main()
        {
            if (debug) Debug.WriteLine("Debugging is enabled.");

            Debug.WriteLine("Compiling Vehicle data...");

            string resourcePath = GetResourcePath(GetCurrentResourceName());
            string streamFolder = $"{resourcePath}/stream";

            foreach (var vehicleFolderPath in Directory.GetDirectories(streamFolder).Where(directory => directory.Contains("-")))
            {
                var vehicleFolder = Path.GetFileName(vehicleFolderPath);
                
                if(debug) Debug.WriteLine("Found vehicle folder: " + vehicleFolder);
                
                // We first check if there is an .yft file inside this folder to make sure we actually have a vehicle folder
                string yftFile = Directory.GetFiles(vehicleFolderPath).Where(file => file.EndsWith(".yft")).FirstOrDefault();

                if (string.IsNullOrEmpty(yftFile))
                {
                    if (debug) Debug.WriteLine($"Folder '{vehicleFolder}' does not contain a .yft file, skipping...");
                    continue; // We don't have a vehicle file to get the game name from, so we skip this folder
                }
                else
                {
                    // Get our parts from the folder name
                    string[] folderParts = vehicleFolder.Split('-');
                    string gameName = new FileInfo(yftFile).Name.Replace(".yft", "");
                    string brand = folderParts[0].Substring(0, 1).ToUpper() + folderParts[0].Substring(1);
                    string name = string.Join(" ", folderParts[1].Split('_').Select(word => word.Substring(0, 1).ToUpper() + word.Substring(1)));

                    if (debug) Debug.WriteLine("Found yft file: " + gameName);

                    Vehicle vehicle = new Vehicle(gameName, brand, name);
                    
                    this.vehicles.Add(vehicle);

                    if(debug) Debug.WriteLine($"-> Added '{vehicle.GetFullName()}' to the vehicle list.");
                }
            }
            Debug.WriteLine("* Finished compiling vehicle data. Vehicles compiled: " + vehicles.Count);

            // Register an event handler called veh-loader:vehicles so we can send the vehicle list to the client
            EventHandlers["veh-load:vehicles"] += new Action<Player>(([FromSourceAttribute] player) =>
            {
                if (debug) Debug.WriteLine($"Sending vehicle list to '{player.Name}'");

                // Create an empty array called vehicleList to contain the contents in the 'vehicles' list using the game name as a key
                var vehicleList = new Dictionary<string, string>();
                foreach (var vehicle in vehicles) vehicleList.Add(vehicle.GameName, vehicle.GetFullName());

                // Can't seem to figure out how to make this one work
                //var vehicleList = vehicles.Select(vehicle => new Array { vehicle.GameName, vehicle.GetFullName() }).ToArray();

                // Send the vehicle list to the client as a serialized object
                player.TriggerEvent("veh-load:vehicles", vehicleList);
            });
        }
    }
}
