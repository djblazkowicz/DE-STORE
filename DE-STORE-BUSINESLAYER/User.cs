using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DE_BusinessLayer
{
    public class User
    {
        public int id { get; set; }
        public int UserType { get; set; }
        public string Name { get; set; }
        public int Points { get; set; }
        public string Email { get; set; }
        public string Mobile { get; set; }
        public int Active { get; set; }
    }
}
