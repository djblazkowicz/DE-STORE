using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DE_BusinessLayer
{
    public class Article
    {
        public int id { get; set; }
        public string Name { get; set; }
        public string Description { get; set; }
        public int Price { get; set; }
        public int Points { get; set; }
        public int Active { get; set; }
    }
}
