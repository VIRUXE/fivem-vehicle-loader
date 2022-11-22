using CitizenFX.Core;
using System;

namespace Server
{
    class Vehicle : ServerScript
    {
        public string GameName;
        public string Brand;
        public string Model;

        public Vehicle(string GameName, string Brand, string Model)
        {
            this.GameName = GameName;
            this.Brand = Brand;
            this.Model = Model;
        }

        public string GetFullName() => $"{Brand} - {Model}";
    }
}