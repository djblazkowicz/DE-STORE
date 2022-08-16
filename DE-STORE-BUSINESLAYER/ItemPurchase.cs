using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DE_BusinessLayer
{
    class ItemPurchase
    {
        public int id { get; set; }
        public int PurchaseOrder { get; set; }
        public int Item { get; set; }
        public int Name { get; set; }
    }
}
