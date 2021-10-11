import os
import binascii

def form(size):
    """manditory"""

    __ref = "464f524d|01820062|41494646"

    ckID = "464f524d" # "FORM"
    ckSize = binascii.hexlify((size+54).to_bytes(4, byteorder = 'big')).decode()
    formType = "41494646" #"AIFF"

    return f"{ckID}{ckSize}{formType}".encode("utf8")

def comm():
    """manditory"""
    __ref = "34f4d4d|00000012|0002|00608000|0010|400eac44000000000000"

    ckID = "434f4d4d"  #"COMM" 4
    ckSize = "00000012" # 00000012 4 (18)
    numChannels = "0001" # 0002 2 (2)
    numSampleFrames = "00608000" #00608000 4 (n)
    sampleSize = "0010" #0010 2 (16)
    sampleRate = "400eac44000000000000" #400eac44000000000000 10 (44100.00)
                  
    return f"{ckID}{ckSize}{numChannels}{numSampleFrames}{sampleSize}{sampleRate}".encode("utf8")
    
def inst():
    """optional"""

    __ref = "494e5354|00000014|3c|00|00|7f|00|7f|0000|0000|0000|0000|0000|0000|0000"

    ckID = "494e5354" #"INST"
    ckSize = "00000014" #00000014 4 (20)
    baseNote = "3c" # 2 (60)
    detune = "00" # 2 (0)
    lowNote = "00" # 2 (0)
    highNote = "7f" # 2 (127)
    lowVelocity = "00" # 2 (0)
    highVelocity = "7f" # 2 (127)
    gain = "0000" # 4  (0)
    sustainLoop_playMode = "0000" # 4 (0)
    sustainLoop_beginLoop = "0000" # 4 (0)
    sustainLoop_endLoop = "0000" # 4 (0)
    releaseLoop_playMode = "0000" # 4 (0)
    releaseLoop_beginLoop = "0000" # 4 (0)
    releaseLoop_endLoop = "0000" # 4 (0)

    return f"{ckID}{ckSize}{baseNote}{detune}{lowNote}{highNote}{lowVelocity}{highVelocity}{gain}{sustainLoop_playMode}{sustainLoop_beginLoop}{sustainLoop_endLoop}{releaseLoop_playMode}{releaseLoop_beginLoop}{releaseLoop_endLoop}".encode("utf8")

def mark():

    """optional"""
    __ref = "4d41524b|00000002|0000"

    ckID = "4d41524b" # "MARK"
    ckSize = "00000002" # 4 (2)
    numMarkers = "0000" # 2 (0)

    return f"{ckID}{ckSize}{numMarkers}".encode("utf8")

def appl():
    """Optional"""

    __ref = "4150504c|00000006|6175464d|0000"

    ckID = "4150504c" # "APPL"
    ckSize = "00000006" # "00000006" 4 (6)
    applicationSignature = "6175464d" # "6175464d" 4 ("auFM")  
    applicationData = "0000" # "0000" 2 (0)

    return f"{ckID}{ckSize}{applicationSignature}{applicationData}".encode("utf8")

def ssnd(un_headed_size_bytes):
    """manditory"""
    ref ="53534e44|005fba08|00000000|00000000"
    ckID = "53534e44" # "SSND"
    ckSize = binascii.hexlify(un_headed_size_bytes.to_bytes(4, byteorder = 'big')).decode()
    offset = "00000000" # "00000000" 4 (0)
    blockSize = "00000000" # 00000000" 4 (0)
    return f"{ckID}{ckSize}{offset}{blockSize}".encode("utf8")

def make_header(un_headed_size_bytes):
    header = b""
    header += form(un_headed_size_bytes)
    header += comm()
    ### optional
    # header += inst()
    # header += mark()
    # header += appl()
    header += ssnd(un_headed_size_bytes)
    return (binascii.unhexlify(header))


def process_folder(folder_name, dest_folder):
    folder = os.path.join(root, folder_name)
    dest = os.path.join(root, dest_folder, folder_name)
    if not os.path.exists(dest):
        os.makedirs(dest)

    for f_name in os.listdir(folder):
        f = os.path.join(folder, f_name)

        file_size = os.path.getsize(f)
        print (f"{f_name} - {file_size} bytes")

        header = make_header(file_size)

        with open(f, 'rb') as data:
            new_data = header+data.read()
        new_fname = f.replace(folder, dest)
        with open(new_fname, "wb") as outfile:
            outfile.write(new_data)


### root folder for project (must contain content being processed in a child folder
root = r'c:\collections\my_aiff_project'

### this is a list of all the folders you want to process. AIFF files being worked must be only children in folder 
folders_to_process = ["my_collection_of_not_working_aiff_files"]

### this folder will be put in the collection root and contain the worked files
destination_for_headed_files = r"my_headed_aiff_files"

for my_folder in folders_to_process:
    process_folder(my_folder, destination_for_headed_files)
