using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Xml;
using System.Xml.Serialization;
using System.IO;
using Microsoft.Xna.Framework;

namespace Core.Pipeline
{
    public class CustomData
    {
        #region Data

        [XmlIgnore]
        public Boolean NameSpecified { get { return !String.IsNullOrEmpty(Name); } }
        [XmlAttribute]
        public String Name = String.Empty;

        [XmlIgnore]
        public Boolean ValueSpecified { get { return !String.IsNullOrEmpty(Value); } }
        [XmlAttribute]
        public String Value = String.Empty;

        [XmlIgnore]
        public Boolean MayaTypeSpecified { get { return !String.IsNullOrEmpty(MayaType); } }
        [XmlAttribute]
        public String MayaType = String.Empty;

        [XmlIgnore]
        public Boolean PositionSpecified { get { return !Position.IsZero(); } }
        public XmlVector3 Position = XmlVector3.Zero;

        [XmlIgnore]
        public Boolean RotationSpecified { get { return !Rotation.IsZero(); } }
        public XmlVector3 Rotation = XmlVector3.Zero;

        [XmlIgnore]
        public Boolean ScaleSpecified { get { return !Scale.IsOne(); } }
        public XmlVector3 Scale = XmlVector3.One;

        [XmlIgnore]
        public Boolean TargetListSpecified { get { return TargetList.Count > 0; } }
        public List<Target> TargetList = new List<Target>();

        [XmlIgnore]
        public Boolean CustomDataCollectionSpecified { get { return CustomDataCollection.Count > 0; } }
        public List<CustomData> CustomDataCollection = new List<CustomData>();

        #endregion

        [XmlIgnore]
        public String Path;

        [XmlIgnore]
        public Matrix Transform
        {
            get
            {
                return Scale.ToScaleMatrix() * Rotation.ToRotationMatrix() * Position.ToTranslationMatrix();
            }
        }

        public CustomData() { }

        #region Load/Save

        public static void Save(ref CustomData customData)
        {
            var serializer = new XmlSerializer(typeof(CustomData));
            var writer = new StreamWriter(customData.Path);
            serializer.Serialize(writer, customData);
            writer.Close();
        }

        public static void Load(ref CustomData customData)
        {
            String customDataPath = customData.Path;
            if (File.Exists(customDataPath))
            {
                var deserializer = new XmlSerializer(typeof(CustomData));
                var reader = new StreamReader(customDataPath);
                customData = (CustomData)deserializer.Deserialize(reader);
                customData.Path = customDataPath;
                reader.Close();
            }
        }

        #endregion

        public CustomData this[string nodeName]
        {
            get
            {
                return GetCustomData(nodeName);
            }
            set
            {
                CustomData customData = GetCustomData(nodeName);
                customData = value;
            }
        }

        public CustomData GetCustomData(string nodeName)
        {
            if (Name == nodeName)
            {
                return this;
            }

            if (CustomDataCollection != null)
            {
                CustomData result = null;
                foreach (var customData in CustomDataCollection)
                {
                    result = customData.GetCustomData(nodeName);

                    if (result != null)
                    {
                        return result;
                    }
                }
            }

            return null;
        }

        public Target GetTargetSafe(int index)
        {
            if (index < TargetList.Count)
            {
                return TargetList[index];
            }
            else
            {
                return new Target();
            }
        }

    }
}
