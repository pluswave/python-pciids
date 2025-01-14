import os


class Vendor:
    """
    Class for vendors. This is the top level class
    for the devices belong to a specific vendor.
    self.devices is the device dictionary
    subdevices are in each device.
    """
    def __init__(self, vendorStr):
        """
        Class initializes with the raw line from pci.ids
        Parsing takes place inside __init__
        """
        self.ID = vendorStr.split()[0]
        self.name = vendorStr.replace("%s " % self.ID,"")
        self.devices = {}

    def addDevice(self, deviceStr):
        """
        Adds a device to self.devices
        takes the raw line from pci.ids
        """
        s = deviceStr.strip()
        devID = s.split()[0]
        if devID in self.devices:
            pass
        else:
            self.devices[devID] = Device(deviceStr)

    def report(self):
        print( self.ID, self.name)
        for id, dev in self.devices.items():
            dev.report()

class Device:
    def __init__(self, deviceStr):
        """
        Class for each device.
        Each vendor has its own devices dictionary.
        """
        s = deviceStr.strip()
        self.ID = s.split()[0]
        self.name = s.replace("%s  " % self.ID,"")
        self.subdevices = {}

    def report(self):
        print("\t%s\t%s" % (self.ID, self.name))
        for subID, subdev in self.subdevices.items():
            subdev.report()

    def addSubDevice(self, subDeviceStr):
        """
        Adds a subvendor, subdevice to device.
        Uses raw line from pci.ids
        """
        s = subDeviceStr.strip()
        spl = s.split()
        subVendorID  = spl[0]
        subDeviceID  = spl[1]
        subDeviceName = s.split("  ")[-1]
        devID = "%s:%s" % (subVendorID,subDeviceID)
        self.subdevices[devID] = SubDevice(subVendorID,subDeviceID,subDeviceName)

class SubDevice:
    """
    Class for subdevices.
    """
    def __init__(self, vendor, device, name):
        """
        Class initializes with vendorid, deviceid and name
        """
        self.vendorID = vendor
        self.deviceID = device
        self.name = name

    def report(self):
        print( "\t\t%s\t%s\t%s" % (self.vendorID, self.deviceID,self.name))

class PCIIds:
    """
    Top class for all pci.ids entries.
    All queries will be asked to this class.
    PCIIds.vendors["0e11"].devices["0046"].subdevices["0e11:4091"].name  =  "Smart Array 6i"
    """
    def __init__(self):
        """
        Prepares the directories.
        Checks local data file.
        Tries to load from local, if not found, downloads from web
        """
        self.vendors = {}
        self.contents = None
        self.loadLocal()
        self.parse()

            
    def reportVendors(self):
        """Reports the vendors
        """
        for vid, v in self.vendors.items():
            print( v.ID, v.name)

    def report(self, vendor = None):
        """
        Reports everything for all vendors or a specific vendor
        PCIIds.report()  reports everything
        PCIIDs.report("0e11") reports only "Compaq Computer Corporation"
        """
        if vendor != None:
            self.vendors[vendor].report()
        else:
            for vID, v in self.vendors.items():
                v.report()

    def findDate(self, content):
        for l in content:
            if l.find("Date:") > -1:
                return l.split()[-2].replace("-", "")
        return None

    def parse(self):
        if len(self.contents) < 1:
            print( "system pci.ids not found" )
        else:
            vendorID = ""
            deviceID = ""
            for l in self.contents:
                if l[0] == "#":
                    continue
                elif len(l.strip()) == 0:
                    continue
                else:
                    if l.find("\t\t") == 0:
                        self.vendors[vendorID].devices[deviceID].addSubDevice(l)
                    elif l.find("\t") == 0:
                        deviceID = l.strip().split()[0]
                        self.vendors[vendorID].addDevice(l)
                    else:
                        vendorID = l.split()[0]
                        self.vendors[vendorID] = Vendor(l)

    def getLatest(self):        
        self.readLocal()


    def readLocal(self):
        """
        Reads the local file
        """
        self.contents = open("/usr/share/misc/pci.ids").readlines()

    def loadLocal(self):
        self.readLocal()


if __name__ == "__main__":
    id = PCIIds()
    #id.reportVendors()
