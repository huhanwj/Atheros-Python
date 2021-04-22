import numpy as np
import os
from timeit import default_timer

class ath:
    def __init__(self, file, nr, nt, tones, pl_len):
        self.file = file
        self.nr_num = nr
        self.nt_num = nt
        self.tones = tones
        self.pl_len = pl_len
        if not os.path.isfile(file):
            raise Exception("Error: File does not exist!\n")
    def read(self, endian = "litte"):
        f = open(self.file, 'rb')
        if f is None:
            f.close()
            return -1
        file_len = os.path.getsize(self.file)
        self.timestamp = np.zeros([file_len//420])
        self.csi_len = np.zeros([file_len//420], dtype=np.int_)
        self.tx_channel = np.zeros([file_len//420], dtype=np.int_)
        self.err_info = np.zeros([file_len//420], dtype=np.int_)
        self.noise_floor = np.zeros([file_len//420], dtype=np.int_)
        self.Rate = np.zeros([file_len//420], dtype=np.int_)
        self.bandWidth = np.zeros([file_len//420], dtype=np.int_)
        self.num_tones = np.zeros([file_len//420], dtype=np.int_)
        self.nr = np.zeros([file_len//420], dtype=np.int_)
        self.nc = np.zeros([file_len//420], dtype=np.int_)
        self.rssi = np.zeros([file_len//420], dtype=np.int_)
        self.rssi_1 = np.zeros([file_len//420], dtype=np.int_)
        self.rssi_2 = np.zeros([file_len//420], dtype=np.int_)
        self.rssi_3 = np.zeros([file_len//420], dtype=np.int_)
        self.payload_len = np.zeros([file_len//420], dtype=np.int_)
        self.csi = np.zeros([file_len//420, self.tones, self.nr_num, self.nt_num], dtype=np.complex128)
        self.payload = np.zeros([file_len//420, self.pl_len], dtype=np.int_)
        cur = 0
        count = 0
        while (cur < file_len - 4):
            field_len = int.from_bytes(f.read(2), byteorder = endian)
            cur += 2
            if (cur + field_len) > file_len:
                break
            self.timestamp[count] = int.from_bytes(f.read(8), byteorder=endian)
            cur += 8
            self.csi_len[count] = int.from_bytes(f.read(2), byteorder=endian)
            cur += 2
            self.tx_channel[count] = int.from_bytes(f.read(2), byteorder=endian)
            cur += 2
            self.err_info[count] = int.from_bytes(f.read(1), byteorder=endian)
            cur += 1
            self.noise_floor[count] = int.from_bytes(f.read(1), byteorder=endian)
            cur += 1
            self.Rate[count] = int.from_bytes(f.read(1), byteorder=endian)
            cur += 1
            self.bandWidth[count] = int.from_bytes(f.read(1), byteorder=endian)
            cur += 1
            self.num_tones[count] = int.from_bytes(f.read(1), byteorder=endian)
            cur += 1
            self.nr[count] = int.from_bytes(f.read(1), byteorder=endian)
            cur += 1
            self.nc[count] = int.from_bytes(f.read(1), byteorder=endian)
            cur += 1
            self.rssi[count] = int.from_bytes(f.read(1), byteorder=endian)
            cur += 1
            self.rssi_1[count] = int.from_bytes(f.read(1), byteorder=endian)
            cur += 1
            self.rssi_2[count] = int.from_bytes(f.read(1), byteorder=endian)
            cur += 1
            self.rssi_3[count] = int.from_bytes(f.read(1), byteorder=endian)
            cur += 1
            self.payload_len[count] = int.from_bytes(f.read(2), byteorder=endian)
            cur += 2
            c_len = self.csi_len[count]
            if c_len > 0:
                csi_buf = f.read(c_len)
                self.csi[count] = self.__read_csi(csi_buf, self.nr[count], self.nc[count], self.num_tones[count])
                cur += c_len
            else:
                self.csi[count] = None

            pl_len = self.payload_len[count]
            pl_stop = min(pl_len, self.pl_len, 0)
            if pl_len > 0:
                self.payload[count, :pl_stop] = bytearray(f.read(pl_len))[:pl_stop]
                cur += pl_len
            else:
                self.payload[count, :pl_stop] = 0

            if (cur + 420 > lens):
                count -= 1
                break
            count += 1


        self.timestamp = self.timestamp[:count]
        self.csi_len = self.csi_len[:count]
        self.tx_channel = self.tx_channel[:count]
        self.err_info = self.err_info[:count]
        self.noise_floor = self.noise_floor[:count]
        self.Rate = self.Rate[:count]
        self.bandWidth = self.bandWidth[:count]
        self.num_tones = self.num_tones[:count]
        self.nr = self.nr[:count]
        self.nc = self.nc[:count]
        self.rssi = self.rssi[:count]
        self.rssi_1 = self.rssi_1[:count]
        self.rssi_2 = self.rssi_2[:count]
        self.rssi_3 = self.rssi_3[:count]
        self.payload_len = self.payload_len[:count]
        self.csi = self.csi[:count]
        self.payload = self.payload[:count]

        f.close()
        
