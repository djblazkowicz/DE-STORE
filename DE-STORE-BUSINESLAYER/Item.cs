using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DE_BusinessLayer
{
    public class Item
    {
        public int id { get; set; }
        public int Article { get; set; }
        /*
         * status 1 = availalbe stock
         * status 2 = checked out pending
         * status 3 = on hold (payment pending)
         * status 4 = sold
         */
        public int Status { get; set; }
        public int Store { get; set; }
        public int StockTransfer { get; set; }
        public string Name { get; set; }
        public int Price { get; set; }


        public int GetID()
        {
            return id;
        }

        public void SetStatus(int newStatus)
        {
            Status = newStatus;
        }

        public Item(int itemid, int itemarticle, int itemstatus, int itemstore, int itemstocktransfer, string itemname)
        {
            id = itemid;
            Article = itemarticle;
            Status = itemstatus;
            Store = itemstore;
            StockTransfer = itemstocktransfer;
            Name = itemname;
        }
    }
}
