using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DE_BusinessLayer
{
    public class PurchaseOrder
    {
        public int id { get; set; }
        public int Status { get; set; }
        public int PaymentMethod{ get; set; }
        public string Date { get; set; }
        public int User { get; set; }
    }
}
