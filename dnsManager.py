import glob
import json


class dnsManager:
    """
        use build response function to return response string
    """
    zonedata = None
    def __init__(self, data, zone_file):

        self.load_zones(zone_file)
        self.data = data

    def load_zones(self, zone_file):
        jsonzone = {}
        zonefiles = glob.glob(f'{zone_file}*.zone')
        for zone in zonefiles:
            with open(zone) as zonedata:
                data = json.load(zonedata)
                zonename = data["$origin"]
                jsonzone[zonename] = data
        self.zonedata = jsonzone

    def get_flags(self, flags):
        """
            manage flag part
            question: can value of variables like QR, AA be changed?
        """
        byte1 = flags[:1]
        byte2 = flags[1:]
        bin1 = bin(int.from_bytes(byte1, byteorder='big'))[2:].zfill(8)
        bin2 = bin(int.from_bytes(byte2, byteorder='big'))[2:].zfill(8)
        QR = AA = '1'
        Opcode = bin1[1:5]
        TC = RD = RA = '0'
        Z = '000'
        RCODE = '0000'
        return int(QR + Opcode + AA + TC + RD, 2).to_bytes(1, byteorder='big') + \
               int(RA + Z + RCODE, 2).to_bytes(1, byteorder='big')

    def get_question_domain(self, question):
        """
            manage question part
        """
        # in this part, for the length of DN it provides a dec num in the beginning
        len_name = int(question[0])
        name = ''
        for index in range(len_name):
            name += chr(question[1 + index])
        len_suffix = int(question[len_name + 1])
        suffix = ''
        for index in range(len_suffix):
            suffix += chr(question[2 + len_name + index])
        # print(suffix, name)
        question_type = question[len_name + len_suffix + 3:len_name + len_suffix + 5]
        # print(question_type)
        # notice that combination of name and suffix should correspond to the data in zone file
        # difference: directly return DN without changing it to a list
        return name + '.' + suffix + '.', question_type, question[
                                                         :len_name + len_suffix + 3]

    def get_zone(self, domain):
        return self.zonedata[domain]

    def get_recs(self, data):
        domain, question_type, ini_code = self.get_question_domain(data)
        qt = ''
        if question_type == b'\x00\x01':
            qt = 'a'
        zone = self.get_zone(domain)
        return zone[qt], qt, domain, ini_code

    def build_question(self, rectype, ini_code):
        qbytes = ini_code

        if rectype == 'a':
            qbytes += (1).to_bytes(2, byteorder='big')

        qbytes += (1).to_bytes(2, byteorder='big')

        return qbytes

    def rectobytes(self, rectype, recttl, recval):

        rbytes = b'\xc0\x0c'  # works for simple DNS server

        if rectype == 'a':
            rbytes = rbytes + bytes([0]) + bytes([1])

        rbytes = rbytes + bytes([0]) + bytes([1])

        rbytes += int(recttl).to_bytes(4, byteorder='big')

        if rectype == 'a':
            rbytes = rbytes + bytes([0]) + bytes([4])

            for part in recval.split('.'):
                # part corresponding to one piece of ipv4
                rbytes += bytes([int(part)])
        return rbytes

    def build_response(self, data):
        Transaction_ID = data[:2]
        TID = ''
        # index of byte type data represents dec format of one bit
        # print('data:', data)
        for byte in Transaction_ID:
            # print(byte, hex(byte))
            TID += hex(byte)[2:]
        # print("TID:", TID)

        flags = self.get_flags(data[2:4])
        # print('flags:', flags)

        QCOUNT = b'\x00\x01'
        records, rectype, domain_name, ini_code = self.get_recs(data[12:])
        ANCOUNT = len(records).to_bytes(2, byteorder='big')

        # Nameserver Count
        NSCOUNT = (0).to_bytes(2, byteorder='big')

        # Additonal Count
        ARCOUNT = (0).to_bytes(2, byteorder='big')

        dnsheader = Transaction_ID + flags + QCOUNT + ANCOUNT + NSCOUNT + ARCOUNT

        # Create DNS body
        dnsbody = b''

        dnsquestion = self.build_question(rectype, ini_code)
        print(dnsquestion)

        for record in records:
            dnsbody += self.rectobytes(rectype, record["ttl"], record["value"])

        return dnsheader + dnsquestion + dnsbody
