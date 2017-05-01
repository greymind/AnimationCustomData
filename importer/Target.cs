using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Xml;
using System.Xml.Serialization;

namespace Core.Pipeline
{
    public class Target
    {
        [XmlAttribute]
        public String Name;

        [XmlAttribute]
        public Single Weight;
    }
}
