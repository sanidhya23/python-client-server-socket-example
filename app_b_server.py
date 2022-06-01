from multiprocessing.connection import Listener

# Cache to store the value for comparision
CACHED_SSID_DICT = {}

class AccessPoint:
    """Class for storing Access Points"""

    def __init__(self, ssid, snr, channel):
        self.ssid = ssid
        self.snr = snr
        self.channel = channel
      
    def __eq__(self, other):
        return self.ssid == other.ssid \
            and self.snr == other.snr \
            and self.channel == other.channel

    def __str__(self):
        return "SSID {0} snr {1}, channel {2}".format(self.ssid, self.snr, self.channel)

    def get_attribute_diff(self, other):
        """Compare attribute values from another object"""
        message = []
        for attrname in ['ssid', 'snr', 'channel']:
            if getattr(self, attrname) != getattr(other, attrname):
                if message:
                    message.append(',')

                message.append("{0} has changed from {1} to {2}".format(attrname, 
                                                            getattr(self, attrname), 
                                                            getattr(other, attrname)
                                                        ))
        
        if message:
            message = " ".join(message)
            message = "{0}: {1}".format(self.ssid, message)        
        return message


class GeneralUtil:
    """Class for general utility function"""

    def create_obj_list(msg):
        """Parse json into list of objects"""
        new_ssid_dict = {}
        for ssid_dict in msg:
            ssid = AccessPoint(ssid=ssid_dict['ssid'], snr=ssid_dict['snr'], channel=ssid_dict['channel'])
            new_ssid_dict[ssid_dict['ssid']] = ssid
        return new_ssid_dict

    def update_cache(ssid_dict):
        global CACHED_SSID_DICT
        CACHED_SSID_DICT = ssid_dict
    

if __name__ == '__main__':
    # Start server and wait for incoming connections
    listener = Listener(('localhost', 6000), authkey=b'secret-password')

    while True:
        conn = listener.accept()
        print("Client {} connected".format(listener.last_accepted))

        while True:
            # Read data sent by client
            msg = conn.recv()
            
            # Get json converted in to dict of objects, where ssid is key
            received_ssid_dict = GeneralUtil.create_obj_list(msg['access_points']) 
            
            # Initialise cache for initial run
            if not CACHED_SSID_DICT:
                GeneralUtil.update_cache(received_ssid_dict)
                print("Initialised cache with following values:")
                
                for ssid in received_ssid_dict.values():
                    print(ssid)

                continue # Skip further execution as all values are added
            
            # Check if cached and new dict are same
            if CACHED_SSID_DICT == received_ssid_dict:  
                print("Same data has been received, skipping..")
                # print(ssid_dict)
            else:
                new_ssid_keys = set(received_ssid_dict.keys())
                cached_ssid_keys = set(CACHED_SSID_DICT.keys())
                ssid_added = list(new_ssid_keys - cached_ssid_keys)
                ssid_removed = list(cached_ssid_keys - new_ssid_keys)
                ssid_existing = list(cached_ssid_keys & new_ssid_keys)
                
                # Update existing values
                for ssid in ssid_existing:
                    if CACHED_SSID_DICT[ssid] == received_ssid_dict[ssid]:
                        pass
                    else:
                        attribute_difference = CACHED_SSID_DICT[ssid].get_attribute_diff(received_ssid_dict[ssid])
                        if attribute_difference:
                            print("Updated: {0}".format(attribute_difference))
                
                for ssid in ssid_added:
                    print("Added: {0}".format(received_ssid_dict[ssid]))

                for ssid in ssid_removed:
                    print("Removed: {0}".format(CACHED_SSID_DICT[ssid]))

                # Rewrite cache
                GeneralUtil.update_cache(received_ssid_dict)
    # Terminate the server
    listener.close()