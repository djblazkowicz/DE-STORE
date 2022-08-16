using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DE_BusinessLayer
{
    public class Store
    {
        public int id { get; set; }
        public string Name { get; set; }
        public string Address { get; set; }
        public int manager { get; set; }


        public Store(int storeid, string storeName, string storeAddress, int storemanager)
        {
            id = storeid;
            Name = storeName;
            Address = storeAddress;
            manager = storemanager;
        }

        public void ChangeManager(int manager_id)
        {
            id = manager_id;
        }

        public override string ToString()
        {
            string output = id + "," + Name + "," + Address + "," + manager;
            return output;
        }
    }
}
