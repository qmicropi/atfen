import binascii
from cryptography.fernet import Fernet, InvalidToken
import cryptography.exceptions as cryptexc
import cryptography.hazmat.primitives.asymmetric.x25519 as x25519
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
import base64
import customtkinter as tk
from tkinter import filedialog
import binascii
import os

class Window(tk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Atfen")
        self.geometry("500x350")

        self.private_key = x25519.X25519PrivateKey.generate()
        self.public_key = self.private_key.public_key()
        self.public_bytes = self.public_key.public_bytes(encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)
        self.bsfb = base64.urlsafe_b64encode(self.public_bytes).decode('utf-8')

        self.filepath = None
        
        self.active_color = "#1f6aa5"
        self.inactive_color = "#353c41"

        self.fram = tk.CTkFrame(self)
        self.fram.grid_columnconfigure(1, weight=1)
        self.pbsfl = tk.CTkLabel(self.fram, text=self.bsfb)
        self.cpbutton = tk.CTkButton(self.fram, text="Copy your Public Key", command=self.copypkey)
        self.pbsfl.grid(row=0, column=0)
        self.cpbutton.grid(row=0, column=1, sticky="ew")
        self.fram.pack(fill="x")

        self.framt = tk.CTkFrame(self)
        self.framt.grid_columnconfigure(1, weight=1)
        self.peerlabel = tk.CTkLabel(self.framt, text="Peer's Public Key:")
        self.peerentry = tk.CTkEntry(self.framt, width=350)
        self.peerlabel.grid(row=0, column=0)
        self.peerentry.grid(row=0, column=1, sticky="ew")
        self.framt.pack(fill="x")

        self.tabs = tk.CTkFrame(self)
        self.tabs.grid_columnconfigure(1, weight=1)
        self.tabs.grid_columnconfigure(0, weight=1)
        self.filetabb = tk.CTkButton(self.tabs, text="File Encryption", command=lambda: self.changetab('file'))
        self.texttabb = tk.CTkButton(self.tabs, text="Text Encryption", command=lambda: self.changetab('text'), fg_color=self.inactive_color)
        self.filetabb.grid(row=0, column=0, sticky="ew")
        self.texttabb.grid(row=0, column=1, sticky="ew")
        self.tabs.pack(fill="x")

        self.fileframe = tk.CTkFrame(self)

        self.pickfframe = tk.CTkFrame(self.fileframe)
        self.pickfframe.columnconfigure(1, weight=1)
        self.pickfile = tk.CTkButton(self.pickfframe, text="Pick a file", command=self.pickafile)
        self.pickedfile = tk.CTkEntry(self.pickfframe, state="disabled")
        self.pickfile.grid(column=0, row=0)
        self.pickedfile.grid(column=1, row=0, sticky="ew")
        self.pickfframe.pack(fill="x")

        self.fedb = tk.CTkFrame(self.fileframe)
        self.fedb.grid_columnconfigure(1, weight=1)
        self.fedb.grid_columnconfigure(0, weight=1)
        self.fileeb = tk.CTkButton(self.fedb, text="Encrypt", command=lambda: self.fileende('encrypt'))
        self.filedb = tk.CTkButton(self.fedb, text="Decrypt", command=lambda: self.fileende('decrypt'))
        self.fileeb.grid(row=0, column=0, sticky="ew")
        self.filedb.grid(row=0, column=1, sticky="ew")
        self.fedb.pack(fill="x")

        self.fileframe.pack(fill="both", expand=True, pady=10)

        self.textframe = tk.CTkFrame(self)
        self.texttoed = tk.CTkTextbox(self.textframe)
        self.texttoed.pack(fill='x')

        self.tedb = tk.CTkFrame(self.textframe)
        self.tedb.grid_columnconfigure(1, weight=1)
        self.tedb.grid_columnconfigure(0, weight=1)
        self.texteb = tk.CTkButton(self.tedb, text="Encrypt", command=lambda: self.textende('encrypt'))
        self.textdb = tk.CTkButton(self.tedb, text="Decrypt", command=lambda: self.textende('decrypt'))
        self.texteb.grid(row=0, column=0, sticky="ew")
        self.textdb.grid(row=0, column=1, sticky="ew")
        self.tedb.pack(fill="x")

        
    def copypkey(self):
        try:
            self.clipboard_clear()
            self.clipboard_append(self.bsfb)
            self.cpbutton.after(0, lambda: self.cpbutton.configure(text="Copied!"))
            self.cpbutton.after(500, lambda: self.cpbutton.configure(text="Copy your Public Key"))
        except Exception as e:
            msg = str(e) if str(e) else "Unknown cryptographic error has occured."
            self.errorbox(msg)
    
    def errorbox(self, error: str):
        w = tk.CTkToplevel()
        w.title("Error!")
        lab = tk.CTkLabel(w, text="Something went wrong!")
        lab.pack(pady=20)
        textbox = tk.CTkTextbox(w, width=500, height=250, wrap='word')
        textbox.pack()
        textbox.insert('1.0', error)
        textbox.configure(state="disabled")
        clb = tk.CTkButton(w, text="Ok", command=lambda: w.destroy())
        clb.pack(pady=10)
    
    def successbox(self, success: str):
        w = tk.CTkToplevel()
        w.title("Success!")
        lab = tk.CTkLabel(w, text="Completed successfully!")
        lab.pack(pady=20)
        textbox = tk.CTkTextbox(w, width=500, height=250, wrap='word')
        textbox.pack()
        textbox.insert('1.0', success)
        textbox.configure(state="disabled")
        clb = tk.CTkButton(w, text="Ok", command=lambda: w.destroy())
        clb.pack(pady=10)
    
    def changetab(self, whic):
        try:
            self.filetabb.configure(
                fg_color=self.active_color if whic == "file" else self.inactive_color
            )
            self.texttabb.configure(
                fg_color=self.active_color if whic == "text" else self.inactive_color
            )

            if whic == "file":
                if self.textframe.winfo_ismapped():
                    self.textframe.pack_forget()
                self.fileframe.pack(fill="both", expand=True, pady=10)
            else:
                if self.fileframe.winfo_ismapped():
                    self.fileframe.pack_forget()
                self.textframe.pack(fill="both", expand=True, pady=10)

        except Exception as e:
            msg = str(e) if str(e) else "Unknown cryptographic error has occured."
            self.errorbox(msg)
    
    def pickafile(self):
        file = filedialog.askopenfilename()
        self.pickedfile.configure(state="normal")
        self.pickedfile.delete('0', tk.END)
        self.pickedfile.insert('0', file)
        self.pickedfile.configure(state="disabled")
        self.filepath = file
    
    def derive(self):
        privateKey = self.private_key
        peerPublicKeyB64encoded = self.peerentry.get()
        if peerPublicKeyB64encoded == "" or not peerPublicKeyB64encoded:
            self.errorbox("Your peer's public key entry is empty. Please provide your peer's public key.")
            return 1

        try:
            peerPublicKeyBytescheck = base64.urlsafe_b64decode(peerPublicKeyB64encoded)
            peerPublicKeycheck = x25519.X25519PublicKey.from_public_bytes(peerPublicKeyBytescheck)
        except (ValueError, binascii.Error):
            self.errorbox("Your peer's public key is invalid. Please check if you have entered the key correctly or if your peer gave you a correct one.")
            return 1
        except Exception as e:
            msg = str(e) if str(e) else "Unknown cryptographic error has occured."
            self.errorbox(msg)
            return 1

        peerPublicKeyBytes = base64.urlsafe_b64decode(peerPublicKeyB64encoded)
        peerPublicKey = x25519.X25519PublicKey.from_public_bytes(peerPublicKeyBytes)

        try:
            sharedKey = privateKey.exchange(peerPublicKey)
            derived_key = HKDF(
                algorithm=hashes.SHA256(),
                length=32,
                salt=None,
                info=b'Information'
            ).derive(sharedKey)
            urlsafeBase64enocdedKey = base64.urlsafe_b64encode(derived_key)
            return urlsafeBase64enocdedKey
        except Exception as e:
            msg = str(e) if str(e) else "Unknown cryptographic error has occured."
            self.errorbox(msg)
    
    def textende(self, operation):
        try:
            key = self.derive()
            if not key or key == 1:
                return
            f = Fernet(key)
            text = self.texttoed.get("1.0", tk.END)
            data = f.encrypt(text.encode('utf-8')).decode('utf-8') if operation == "encrypt" else f.decrypt(text.encode('utf-8')).decode('utf-8')
            self.texttoed.delete('1.0', tk.END)
            self.texttoed.insert('1.0', data)
        except InvalidToken:
            self.errorbox('Tried to decrypt using invalid key. Are you sure this data was encrypted with your public key?')
        except Exception as e:
            msg = str(e) if str(e) else "Unknown cryptographic error has occured. It is possible that you have tried to decrypt a non-encrypted text, or the data wasn't encrypted with your public key."
            self.errorbox(msg)
    
    def fileende(self, operation):
        if not self.filepath:
            self.errorbox("No file picked. Please pick a file.")
            return
        try:
            key = self.derive()
            if not key or key == 1:
                return
            f = Fernet(key)
            with open(file=self.filepath, mode='rb') as p:
                predata = p.read()
            
            afterdata = f.encrypt(predata) if operation == "encrypt" else f.decrypt(predata)
            filename, extname = os.path.splitext(self.filepath)

            with open(file=f"{filename}.encrypted{extname}" if operation == "encrypt" else f"{filename.removesuffix('.encrypted')}.decrypted{extname}", mode='wb') as a:
                a.write(afterdata)
            self.successbox("Successfully encrypted the file." if operation == "encrypt" else "Successfully decrypted the file.")
        except InvalidToken:
            self.errorbox('Tried to decrypt using invalid key. Are you sure this data was encrypted with your public key?')
        except Exception as e:
            msg = str(e) if str(e) else "Unknown cryptographic error has occured. It is possible that you have tried to decrypt a non-encrypted file, or the data wasn't encrypted with your public key."
            self.errorbox(msg)

        

if __name__ == "__main__":
    window = Window()
    window.mainloop()
