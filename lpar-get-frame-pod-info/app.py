import os
import ssl
import string
import requests
from flask import Flask, request

accountsecret = open("/var/secret/vmwareaccount/vmwareaccount", "r")
account = accountsecret.readline().strip()
passwordsecret = open("/var/secret/vmwarepassword/vmwarepassword", "r")
password = passwordsecret.readline().strip()

app = Flask(__name__)

# simple route to ensure function spins from web browser
@app.route('/')
def default():
    return "Please specify parameters"

# The route used when calling the function
@app.route('/getFramePodInfo', methods=['POST'])

def getFramePodInfo():
    json_req = request.get_json(force=True)
    theFrame = json_req['frame']
    # attribArray = json_req['attributes']
    # note: in this conversion from UCS Director javascript, effort was made to preserve
    #       all Will Wyman's tedius collection of storage data relationships.
    #       This function could easily be expanded to return any frame attributes specified at runtime.
    #       Only 3 of these attributes are required at this time.

    # T1
    if theFrame == "<Frame>6001":
        PODname = "T1 DB"

        MDSprimary = "DC_AIX@STGTCSOM1206" # stgtcsom1206
        MDSpriamryReportID = "4"
        MDSpriamryVSAN = "DC_AIX@STGTCSOM1206@140"
        MDSprimaryVSANzone = "STGTCSOM1206140"
        MDSprimaryZoneName = "_STGNTAP1203_A"
        MDSprimaryZoneSet = "STGTCSOM1206140TCC1_AIX_FABRIC_A"

        MDSsecondary = "DC_AIX@STGTCSOM1207" #stgtcsom1207
        MDSsecondaryReportID = "3"
        MDSsecondaryVSAN = "DC_AIX@STGTCSOM1207@141"
        MDSsecondaryVSANzone = "STGTCSOM1207141"
        MDSsecondaryZoneName = "_STGNTAP1203_D"
        MDSsecondaryZoneSet = "STGTCSOM1207141TCC1_AIX_FABRIC_B"

        ARRAYnameSVM = "DC_AIX@DC_AIX@<IP-Addr>@t1aix-fc" 
        ARRAYreportID = "DC_AIX@DC_AIX@<IP-Addr>@t1aix-fc" 
        ARRAYstoragePriPorts = ["STGTNTAP1203_02_2A","STGTNTAP1203_02_10A","STGTNTAP1203_01_2A","STGTNTAP1203_01_10A","STGTNTAP1203_04_2A","STGTNTAP1203_03_10A","STGTNTAP1203_03_2A","STGTNTAP1203_04_10A"]
        ARRAYstorageSecPorts = ["STGTNTAP1203_02_10D","STGTNTAP1203_01_2D","STGTNTAP1203_01_10D","STGTNTAP1203_02_2D","STGTNTAP1203_03_2D","STGTNTAP1203_04_2D","STGTNTAP1203_04_10D","STGTNTAP1203_03_10D"]

        FRAMEvioServers = ["<VIO-Server>6001","<VIO-Server>6002","<VIO-Server>6003","<VIO-Server>6004","<VIO-Server>6005","<VIO-Server>6006"]
        FRAMEhmc = "<HMC-Server>7001"
        wfaSVM = "t1aix-fc"
        wfaArray = "stgtntap1203"
        wfaServer = "<WFA-Server>"
        vio1 = "<VIO-Server>6001"
        vio2 = "<VIO-Server>6002"
        vio3 = "<VIO-Server>6003"
        vio4 = "<VIO-Server>6004"

    elif theFrame == "<Frame>6002":
        PODname = "T1 DB"

        MDSprimary = "DC_AIX@STGTCSOM1206" # stgtcsom1206
        MDSpriamryReportID = "4"
        MDSpriamryVSAN = "DC_AIX@STGTCSOM1206@140"
        MDSprimaryVSANzone = "STGTCSOM1206140"
        MDSprimaryZoneName = "_STGNTAP1203_A"
        MDSprimaryZoneSet = "STGTCSOM1206140TCC1_AIX_FABRIC_A"

        MDSsecondary = "DC_AIX@STGTCSOM1207" # stgtcsom1207
        MDSsecondaryReportID = "3"
        MDSsecondaryVSAN = "DC_AIX@STGTCSOM1207@141"
        MDSsecondaryVSANzone = "STGTCSOM1207141"
        MDSsecondaryZoneName = "_STGNTAP1203_D"
        MDSsecondaryZoneSet = "STGTCSOM1207141TCC1_AIX_FABRIC_B"

        ARRAYnameSVM = "DC_AIX@DC_AIX@<IP-Addr>@t1aix-fc" 
        ARRAYreportID = "DC_AIX@DC_AIX@<IP-Addr>@t1aix-fc" 
        ARRAYstoragePriPorts = ["STGTNTAP1203_04_10B","STGTNTAP1203_03_2B","STGTNTAP1203_03_10B","STGTNTAP1203_02_2B","STGTNTAP1203_02_10B","STGTNTAP1203_01_2B","STGTNTAP1203_04_2B","STGTNTAP1203_01_10B"]
        ARRAYstorageSecPorts = ["STGTNTAP1203_01_10C","STGTNTAP1203_04_2C","STGTNTAP1203_02_10C","STGTNTAP1203_04_10C","STGTNTAP1203_01_2C","STGTNTAP1203_03_2C","STGTNTAP1203_03_10C","STGTNTAP1203_02_2C"]

        FRAMEvioServers = ["<VIO-Server>6001","<VIO-Server>6002","<VIO-Server>6003","<VIO-Server>6004","<VIO-Server>6005","<VIO-Server>6006"]
        FRAMEhmc = "<HMC-Server>7001"
        wfaSVM = "t1aix-fc"
        wfaArray = "stgtntap1203"
        wfaServer = "<WFA-Server>"
        vio1 = "<VIO-Server>6001"
        vio2 = "<VIO-Server>6002"
        vio3 = "<VIO-Server>6003"
        vio4 = "<VIO-Server>6004"
    elif theFrame == "<Frame>6003":
        PODname = "T1 DB"

        MDSprimary = "DC_AIX@STGTCSOM1206" # stgtcsom1206
        MDSpriamryReportID = "4"
        MDSpriamryVSAN = "DC_AIX@STGTCSOM1206@140"
        MDSprimaryVSANzone = "STGTCSOM1206140"
        MDSprimaryZoneName = "_STGNTAP1203_A"
        MDSprimaryZoneSet = "STGTCSOM1206140TCC1_AIX_FABRIC_A"

        MDSsecondary = "DC_AIX@STGTCSOM1207" #stgtcsom1207
        MDSsecondaryReportID = "3"
        MDSsecondaryVSAN = "DC_AIX@STGTCSOM1207@141"
        MDSsecondaryVSANzone = "STGTCSOM1207141"
        MDSsecondaryZoneName = "_STGNTAP1203_D"
        MDSsecondaryZoneSet = "STGTCSOM1207141TCC1_AIX_FABRIC_B"

        ARRAYnameSVM = "DC_AIX@DC_AIX@<IP-Addr>@t1aix-fc" 
        ARRAYreportID = "DC_AIX@DC_AIX@<IP-Addr>@t1aix-fc" 
        ARRAYstoragePriPorts = ["STGTNTAP1203_04_10B","STGTNTAP1203_03_2B","STGTNTAP1203_03_10B","STGTNTAP1203_02_2B","STGTNTAP1203_02_10B","STGTNTAP1203_01_2B","STGTNTAP1203_04_2B","STGTNTAP1203_01_10B"]
        ARRAYstorageSecPorts = ["STGTNTAP1203_01_10C","STGTNTAP1203_04_2C","STGTNTAP1203_02_10C","STGTNTAP1203_04_10C","STGTNTAP1203_01_2C","STGTNTAP1203_03_2C","STGTNTAP1203_03_10C","STGTNTAP1203_02_2C"]

        FRAMEvioServers = ["<VIO-Server>6001","<VIO-Server>6002","<VIO-Server>6003","<VIO-Server>6004","<VIO-Server>6005","<VIO-Server>6006"]
        FRAMEhmc = "<HMC-Server>7001"
        wfaSVM = "t1aix-fc"
        wfaArray = "stgtntap1203"
        wfaServer = "<WFA-Server>"
        vio1 = "<VIO-Server>6001"
        vio2 = "<VIO-Server>6002"
        vio3 = "<VIO-Server>6003"
        vio4 = "<VIO-Server>6004"
    # T1 LAB
    elif theFrame == "<Frame>8001":
        PODname = "T1 DB"

        MDSprimary = "DC_AIX@STGTCSOM1206" # stgtcsom1206
        MDSpriamryReportID = "4"
        MDSpriamryVSAN = "DC_AIX@STGTCSOM1206@140"
        MDSprimaryVSANzone = "STGTCSOM1206140"
        MDSprimaryZoneName = "_STGNTAP1203_A"
        MDSprimaryZoneSet = "STGTCSOM1206140TCC1_AIX_FABRIC_A"

        MDSsecondary = "DC_AIX@STGTCSOM1207" #stgtcsom1207
        MDSsecondaryReportID = "3"
        MDSsecondaryVSAN = "DC_AIX@STGTCSOM1207@141"
        MDSsecondaryVSANzone = "STGTCSOM1207141"
        MDSsecondaryZoneName = "_STGNTAP1203_D"
        MDSsecondaryZoneSet = "STGTCSOM1207141TCC1_AIX_FABRIC_B"

        ARRAYnameSVM = "DC_AIX@DC_AIX@<IP-Addr>@t1aix-fc" 
        ARRAYreportID = "DC_AIX@DC_AIX@<IP-Addr>@t1aix-fc" 
        ARRAYstoragePriPorts = ["STGTNTAP1203_02_2A","STGTNTAP1203_02_10A","STGTNTAP1203_01_2A","STGTNTAP1203_01_10A","STGTNTAP1203_04_2A","STGTNTAP1203_03_10A","STGTNTAP1203_03_2A","STGTNTAP1203_04_10A"]
        ARRAYstorageSecPorts = ["STGTNTAP1203_02_10D","STGTNTAP1203_01_2D","STGTNTAP1203_01_10D","STGTNTAP1203_02_2D","STGTNTAP1203_03_2D","STGTNTAP1203_04_2D","STGTNTAP1203_04_10D","STGTNTAP1203_03_10D"]

        FRAMEvioServers = ["<VIO-Server>6001","<VIO-Server>6002"]
        FRAMEhmc = "<HMC-Server>7001"
        wfaSVM = "t1aix-fc"
        wfaArray = "stgtntap1203"
        wfaServer = "<WFA-Server>"
        vio1 = "<VIO-Server>8001"
        # vio2 = "labframe_rootvg"
        vio2 = "<VIO-Server>8002"
    # T3
    elif theFrame == "<Frame>G2001":
        PODname = "T3 DB"

        # "POD@addressUsedForDiscovery"
        MDSprimary = "<VMWare-Cluster_DB@stgtcsom3206" # stgtcsom3206
        MDSpriamryReportID = "23"
        # "POD@addressUsedForDiscovery@VSANid"
        MDSpriamryVSAN = "<VMWare-Cluster_DB@stgtcsom3206@340"
        MDSprimaryVSANzone = "stgtcsom3206340"
        MDSprimaryZoneName = "_STGNTAP3203_A"
        # "addressUsedForDiscoveryprimaryZoneSetNAme"
        MDSprimaryZoneSet = "stgtcsom3206340TCC3_AIX_FABRIC_A"

        MDSsecondary = "<VMWare-Cluster_DB@stgtcsom3207"  #stgtcsom3207
        MDSsecondaryReportID = "24"
        MDSsecondaryVSAN = "<VMWare-Cluster_DB@stgtcsom3207@341"
        MDSsecondaryVSANzone = "stgtcsom3207341"
        MDSsecondaryZoneName = "_STGNTAP3203_B"
        MDSsecondaryZoneSet = "stgtcsom3207341TCC3_AIX_FABRIC_B"
        ARRAYnameSVM = "NA"
        ARRAYreportID = "NA"

        ARRAYstoragePriPorts = ["STGTNTAP3203_01_2A","STGTNTAP3203_02_2A","STGTNTAP3203_03_2A","STGTNTAP3203_04_2A","STGTNTAP3203_01_10A","STGTNTAP3203_02_10A","STGTNTAP3203_03_10A","STGTNTAP3203_04_10A"]
        ARRAYstorageSecPorts = ["STGTNTAP3203_01_2D","STGTNTAP3203_02_2D","STGTNTAP3203_03_2D","STGTNTAP3203_04_2D","STGTNTAP3203_01_10D","STGTNTAP3203_02_10D","STGTNTAP3203_03_10D","STGTNTAP3203_04_10D"]
        FRAMEvioServers = ["<VIO-Server>2001","<VIO-Server>2002","<VIO-Server>2003","<VIO-Server>2004","<VIO-Server>2005","<VIO-Server>2006"]
        FRAMEhmc = "<HMC-Server>3001"
        wfaSVM = "t3aix-fc"
        wfaArray = "stgtntap3203"
        wfaServer = "<WFA-Server>"
        vio1 = "<VIO-Server>2001"
        vio2 = "<VIO-Server>2002"
        vio3 = "<VIO-Server>2003"
        vio4 = "<VIO-Server>2004"
    elif theFrame == "<Frame>2002":
        PODname = "T3 DB"

        # "POD@addressUsedForDiscovery"
        MDSprimary = "<VMWare-Cluster_DB@stgtcsom3206" # stgtcsom3206
        MDSpriamryReportID = "23"
        # "POD@addressUsedForDiscovery@VSANid"
        MDSpriamryVSAN = "<VMWare-Cluster_DB@stgtcsom3206@340"
        MDSprimaryVSANzone = "stgtcsom3206340"
        MDSprimaryZoneName = "_STGNTAP3203_A"
        # "addressUsedForDiscoveryprimaryZoneSetNAme"
        MDSprimaryZoneSet = "stgtcsom3206340TCC3_AIX_FABRIC_A"

        MDSsecondary = "<VMWare-Cluster_DB@stgtcsom3207" # stgtcsom3207
        MDSsecondaryReportID = "24"
        MDSsecondaryVSAN = "<VMWare-Cluster_DB@stgtcsom3207@341"
        MDSsecondaryVSANzone = "stgtcsom3207341"
        MDSsecondaryZoneName = "_STGNTAP3203_B"
        MDSsecondaryZoneSet = "stgtcsom3207341TCC3_AIX_FABRIC_B"
        ARRAYnameSVM = "NA"
        ARRAYreportID = "NA"

        ARRAYstoragePriPorts = ["STGTNTAP3203_01_2B","STGTNTAP3203_02_2B","STGTNTAP3203_03_2B","STGTNTAP3203_04_2B","STGTNTAP3203_01_10B","STGTNTAP3203_02_10B","STGTNTAP3203_03_10B","STGTNTAP3203_04_10B"]
        ARRAYstorageSecPorts = ["STGTNTAP3203_01_2C","STGTNTAP3203_02_2C","STGTNTAP3203_03_2C","STGTNTAP3203_04_2C","STGTNTAP3203_01_10C","STGTNTAP3203_02_10C","STGTNTAP3203_03_10C","STGTNTAP3203_04_10C"]
        FRAMEvioServers = ["<VIO-Server>2001","<VIO-Server>2002","<VIO-Server>2003","<VIO-Server>2004","<VIO-Server>2005","<VIO-Server>2006"]
        FRAMEhmc = "<HMC-Server>3001"
        wfaSVM = "t3aix-fc"
        wfaArray = "stgtntap3203"
        wfaServer = "<WFA-Server>"
        vio1 = "<VIO-Server>2001"
        vio2 = "<VIO-Server>2002"
        vio3 = "<VIO-Server>2003"
        vio4 = "<VIO-Server>2004"
    elif theFrame == "<Frame>2003":
        PODname = "T3 DB"

        # "POD@addressUsedForDiscovery"
        MDSprimary = "<VMWare-Cluster_DB@stgtcsom3206" # stgtcsom3206
        MDSpriamryReportID = "23"
        #"POD@addressUsedForDiscovery@VSANid"
        MDSpriamryVSAN = "<VMWare-Cluster_DB@stgtcsom3206@340"
        MDSprimaryVSANzone = "stgtcsom3206340"
        MDSprimaryZoneName = "_STGNTAP3203_A"
        # "addressUsedForDiscoveryprimaryZoneSetNAme"
        MDSprimaryZoneSet = "stgtcsom3206340TCC3_AIX_FABRIC_A"

        MDSsecondary = "<VMWare-Cluster_DB@stgtcsom3207" #stgtcsom3207
        MDSsecondaryReportID = "24"
        MDSsecondaryVSAN = "<VMWare-Cluster_DB@stgtcsom3207@341"
        MDSsecondaryVSANzone = "stgtcsom3207341"
        MDSsecondaryZoneName = "_STGNTAP3203_B"
        MDSsecondaryZoneSet = "stgtcsom3207341TCC3_AIX_FABRIC_B"
        ARRAYnameSVM = "NA"
        ARRAYreportID = "NA"

        ARRAYstoragePriPorts = ["STGTNTAP3203_01_2B","STGTNTAP3203_02_2B","STGTNTAP3203_03_2B","STGTNTAP3203_04_2B","STGTNTAP3203_01_10B","STGTNTAP3203_02_10B","STGTNTAP3203_03_10B","STGTNTAP3203_04_10B"]
        ARRAYstorageSecPorts = ["STGTNTAP3203_01_2C","STGTNTAP3203_02_2C","STGTNTAP3203_03_2C","STGTNTAP3203_04_2C","STGTNTAP3203_01_10C","STGTNTAP3203_02_10C","STGTNTAP3203_03_10C","STGTNTAP3203_04_10C"]
        FRAMEvioServers = ["<VIO-Server>2001","<VIO-Server>2002","<VIO-Server>2003","<VIO-Server>2004","<VIO-Server>2005","<VIO-Server>2006"]
        FRAMEhmc = "<HMC-Server>3001"
        wfaSVM = "t3aix-fc"
        wfaArray = "stgtntap3203"
        wfaServer = "<WFA-Server>"
        vio1 = "<VIO-Server>2001"
        vio2 = "<VIO-Server>2002"
        vio3 = "<VIO-Server>2003"
        vio4 = "<VIO-Server>2004"
    # B1
    elif theFrame == "<Frame>2001":
        PODname = "B1 DB"

        # "POD@addressUsedForDiscovery"
        MDSprimary = "<VMWare-Cluster_DB@<VSAN>6"
        MDSpriamryReportID = "9"
        # "POD@addressUsedForDiscovery@VSANid"
        MDSpriamryVSAN = "<VMWare-Cluster_DB@<VSAN>6@540"
        MDSprimaryVSANzone = "<VSAN>6540"
        MDSprimaryZoneName = "_STGNTAP5203_A"
        # "addressUsedForDiscoveryprimaryZoneSetNAme"
        MDSprimaryZoneSet = "<VSAN>6540BCC1_AIX_FABRIC_A"

        MDSsecondary = "<VMWare-Cluster_DB@<VSAN>7"
        MDSsecondaryReportID = "10"
        MDSsecondaryVSAN = "<VMWare-Cluster_DB@<VSAN>7@541"
        MDSsecondaryVSANzone = "<VSAN>7541"
        MDSsecondaryZoneName = "_STGNTAP5203_B"
        MDSsecondaryZoneSet = "<VSAN>7541BCC1_AIX_FABRIC_B"
        ARRAYnameSVM = "NA"
        ARRAYreportID = "NA"

        ARRAYstoragePriPorts = ["STGBNTAP5203_01_2A","STGBNTAP5203_02_2A","STGBNTAP5203_03_2A","STGBNTAP5203_04_2A","STGBNTAP5203_01_10A","STGBNTAP5203_02_10A","STGBNTAP5203_03_10A","STGBNTAP5203_04_10A"]
        ARRAYstorageSecPorts = ["STGBNTAP5203_01_2C","STGBNTAP5203_02_2C","STGBNTAP5203_03_2C","STGBNTAP5203_04_2C","STGBNTAP5203_01_10C","STGBNTAP5203_02_10C","STGBNTAP5203_03_10C","STGBNTAP5203_04_10C"]
        FRAMEvioServers = ["<VIO-Server>2001","<VIO-Server>2002","<VIO-Server>2003","<VIO-Server>2004","<VIO-Server>2005","<VIO-Server>2006"]
        FRAMEhmc = "<HMC-Server>3001"
        wfaSVM = "b1aix-fc"
        wfaArray = "stgbntap5203"
        wfaServer = "<WFA-Server>"
        vio1 = "<VIO-Server>2001"
        vio2 = "<VIO-Server>2002"
        vio3 = "<VIO-Server>2003"
        vio4 = "<VIO-Server>2004"
    elif theFrame == "<Frame>2002":
        PODname = "B1 DB"

        # "POD@addressUsedForDiscovery"
        MDSprimary = "<VMWare-Cluster_DB@<VSAN>6"
        MDSpriamryReportID = "9"
        # "POD@addressUsedForDiscovery@VSANid"
        MDSpriamryVSAN = "<VMWare-Cluster_DB@<VSAN>6@540"
        MDSprimaryVSANzone = "<VSAN>6540"
        MDSprimaryZoneName = "_STGNTAP5203_A"
        # "addressUsedForDiscoveryprimaryZoneSetNAme"
        MDSprimaryZoneSet = "<VSAN>6540BCC1_AIX_FABRIC_A"

        MDSsecondary = "<VMWare-Cluster_DB@<VSAN>7"
        MDSsecondaryReportID = "10"
        MDSsecondaryVSAN = "<VMWare-Cluster_DB@<VSAN>7@541"
        MDSsecondaryVSANzone = "<VSAN>7541"
        MDSsecondaryZoneName = "_STGNTAP5203_B"
        MDSsecondaryZoneSet = "<VSAN>7541BCC1_AIX_FABRIC_B"
        ARRAYnameSVM = "NA"
        ARRAYreportID = "NA"

        ARRAYstoragePriPorts = ["STGBNTAP5203_01_2B","STGBNTAP5203_02_2B","STGBNTAP5203_03_2B","STGBNTAP5203_04_2B","STGBNTAP5203_01_10B","STGBNTAP5203_02_10B","STGBNTAP5203_03_10B","STGBNTAP5203_04_10B"]
        ARRAYstorageSecPorts = ["STGBNTAP5203_01_2D","STGBNTAP5203_02_2D","STGBNTAP5203_03_2D","STGBNTAP5203_04_2D","STGBNTAP5203_01_10D","STGBNTAP5203_02_10D","STGBNTAP5203_03_10D","STGBNTAP5203_04_10D"]
        FRAMEvioServers = ["<VIO-Server>2001","<VIO-Server>2002","<VIO-Server>2003","<VIO-Server>2004","<VIO-Server>2005","<VIO-Server>2006"]
        FRAMEhmc = "<HMC-Server>3001"
        wfaSVM = "b1aix-fc"
        wfaArray = "stgbntap5203"
        wfaServer = "<WFA-Server>"
        vio1 = "<VIO-Server>2001"
        vio2 = "<VIO-Server>2002"
        vio3 = "<VIO-Server>2003"
        vio4 = "<VIO-Server>2004"
    elif theFrame == "<Frame>2003":
        PODname = "B1 DB"

        # "POD@addressUsedForDiscovery"
        MDSprimary = "<VMWare-Cluster_DB@<VSAN>6"
        MDSpriamryReportID = "9"
        # "POD@addressUsedForDiscovery@VSANid"
        MDSpriamryVSAN = "<VMWare-Cluster_DB@<VSAN>6@540"
        MDSprimaryVSANzone = "<VSAN>6540"
        MDSprimaryZoneName = "_STGNTAP5203_A"
        # "addressUsedForDiscoveryprimaryZoneSetNAme"
        MDSprimaryZoneSet = "<VSAN>6540BCC1_AIX_FABRIC_A"

        MDSsecondary = "<VMWare-Cluster_DB@<VSAN>7"
        MDSsecondaryReportID = "10"
        MDSsecondaryVSAN = "<VMWare-Cluster_DB@<VSAN>7@541"
        MDSsecondaryVSANzone = "<VSAN>7541"
        MDSsecondaryZoneName = "_STGNTAP5203_B"
        MDSsecondaryZoneSet = "<VSAN>7541BCC1_AIX_FABRIC_B"
        ARRAYnameSVM = "NA"
        ARRAYreportID = "NA"

        ARRAYstoragePriPorts = ["STGBNTAP5203_01_2B","STGBNTAP5203_02_2B","STGBNTAP5203_03_2B","STGBNTAP5203_04_2B","STGBNTAP5203_01_10B","STGBNTAP5203_02_10B","STGBNTAP5203_03_10B","STGBNTAP5203_04_10B"]
        ARRAYstorageSecPorts = ["STGBNTAP5203_01_2D","STGBNTAP5203_02_2D","STGBNTAP5203_03_2D","STGBNTAP5203_04_2D","STGBNTAP5203_01_10D","STGBNTAP5203_02_10D","STGBNTAP5203_03_10D","STGBNTAP5203_04_10D"]
        FRAMEvioServers = ["<VIO-Server>2001","<VIO-Server>2002","<VIO-Server>2003","<VIO-Server>2004","<VIO-Server>2005","<VIO-Server>2006"]
        FRAMEhmc = "<HMC-Server>3001"
        wfaSVM = "b1aix-fc"
        wfaArray = "stgbntap5203"
        wfaServer = "<WFA-Server>"
        vio1 = "<VIO-Server>2001"
        vio2 = "<VIO-Server>2002"
        vio3 = "<VIO-Server>2003"
        vio4 = "<VIO-Server>2004"
    else:
        print( "frame '" + theFrame + "' is not defined as a condition")

    rtn = '{"wfaSVM":"' +  str(wfaSVM) + '","wfaArray":"' + str(wfaArray) + '","FRAMEvioServers":['
    for vioSvr in FRAMEvioServers:
        rtn += '"' + str(vioSvr) + '",'
    rtn = rtn[:-1]
    rtn += ']}'
    return rtn

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))
