from OpenSSL import crypto
import os
import re
import yaml
from OpenSSL.crypto import TYPE_RSA, TYPE_DSA, FILETYPE_PEM, load_certificate_request, PKCS12, FILETYPE_ASN1, load_privatekey, X509Req


class Secure: 
    def __init__(self, ConfigFile):
        self.ConfigFile = ConfigFile
        CertConfig = self.ParseConfig()
        if CertConfig['CERT'].get('KeyType') == 'RSA':
            self.KeyType = TYPE_RSA
        elif CertConfig['CERT'].get('KeyType') == 'DSA':
            self.KeyType = TYPE_DSA
        self.CsrFile = CertConfig['CSR'].get('OldCsrFile')
        self.OldCsrFileType = CertConfig['CSR'].get('OldCsrFileType')
        self.BitLength = CertConfig['CERT'].get('BitLength')
        self.digestType = CertConfig['CERT'].get('digestType')
        self.CertDir = CertConfig['CERT'].get('CertDir')
        self.set_notBefore = CertConfig['CSR'].get('validfrom')
        self.set_notAfter = CertConfig['CSR'].get('validto')
        self.OldPrivateKey = CertConfig['REUSE'].get('OldPrivateKey')
        self.OldPrivateKeyType = CertConfig['REUSE'].get('OldPrivateKeyType')
        self.Certificate = CertConfig['REUSE'].get('Certificate')
        self.validfrom = CertConfig['CERT'].get('validfrom')
        self.validto = CertConfig['CERT'].get('validto')
        

    def ParseConfig(self):
        with open(self.ConfigFile) as Config:
            try:
                CertConfig = yaml.safe_load(Config)
            except Exception as ConfigException:
                print("Failed to read Configuration %s" %(ConfigException))
        return CertConfig
      
    def GetPrivateKey(self):
        if not self.OldPrivateKey:
            Key = crypto.PKey()
            Key.generate_key(self.KeyType, self.BitLength)
        else:
            with open(self.OldPrivateKey) as KeyFile:
                if self.OldPrivateKeyType == 'PEM':
                    Key = load_privatekey(FILETYPE_PEM, KeyFile.read())
                elif self.OldPrivateKeyType == 'DER':
                    Key = load_privatekey(FILETYPE_ASN1, KeyFile.read())
        return Key
                
    def CreateCsr(self, Key):
        if not self.CsrFile:
            CertConfig = self.ParseConfig()
            Csr = X509Req()
            Csr.get_subject().commonName = CertConfig['CSR'].get('commonName')
            Csr.get_subject().stateOrProvinceName = CertConfig['CSR'].get('stateOrProvinceName')
            Csr.get_subject().localityName = CertConfig['CSR'].get('localityName')
            Csr.get_subject().organizationName = CertConfig['CSR'].get('organizationName')
            Csr.get_subject().organizationalUnitName = CertConfig['CSR'].get('organizationalUnitName')
            Csr.get_subject().emailAddress = CertConfig['CSR'].get('emailAddress')
            Csr.get_subject().countryName = CertConfig['CSR'].get('countryName')
            Csr.set_pubkey(Key)
            Csr.sign(Key, self.digestType)
        else:
            with open(self.CsrFile) as CsrFile:
                if self.OldCsrFileType == 'PEM':
                    Csr = load_certificate_request(FILETYPE_PEM, CsrFile.read())
                elif self.OldCsrFileType == 'DER':
                    Csr = load_certificate_request(FILETYPE_ASN1, CsrFile.read())
                else:
                    raise TypeError("Unknown Certificate Type %s" %(self.OldCsrFileType))
        return Csr
    
    def CreateCert(self, Csr, Key):
        Cert = crypto.X509()
        Cert.get_subject().commonName = Csr.get_subject().commonName
        Cert.get_subject().stateOrProvinceName = Csr.get_subject().stateOrProvinceName
        Cert.get_subject().localityName = Csr.get_subject().localityName
        Cert.get_subject().organizationName = Csr.get_subject().organizationName
        Cert.get_subject().organizationalUnitName = Csr.get_subject().organizationalUnitName
        Cert.get_subject().emailAddress = Csr.get_subject().emailAddress
        Cert.get_subject().countryName = Csr.get_subject().countryName
        if self.validfrom and self.validto:
            Cert.set_notBefore(self.validfrom)
            Cert.set_notAfter(self.validto)
        Cert.set_pubkey(Key)
        Cert.sign(Key, self.digestType)
        return Cert
    
    def CreateP12(self, Key, Cert, p12File, passphrase=None):
        p12 = PKCS12()
        p12.set_certificate(Cert)
        p12.set_privatekey(Key)
        p12File.write(p12.export(passphrase = passphrase))
        
    
    def DumpKeyCertCsr(self):
        Key = self.GetPrivateKey()
        Csr = self.CreateCsr(Key)
        Cert = self.CreateCert(Csr, Key)
        cn = Csr.get_subject().commonName
        cn = re.sub(' +', '_', cn)
        
        #Files in PEM format
        PemKeyPath = os.path.join(self.CertDir, cn + "_pkey.pem")
        PemCsrPath = os.path.join(self.CertDir, cn + "_csr.pem")
        PemCertPath = os.path.join(self.CertDir, cn + "_cert.pem")
        if not self.OldPrivateKey:
            with open(PemKeyPath, "w") as fPemPrivKey:
                fPemPrivKey.write(crypto.dump_privatekey(FILETYPE_PEM, Key))
        if not self.CsrFile:
            with open(PemCsrPath, "w") as fPemcsr:
                fPemcsr.write(crypto.dump_certificate_request(FILETYPE_PEM, Csr))
        with open(PemCertPath, "w") as fPemcert:
            fPemcert.write(crypto.dump_certificate(FILETYPE_PEM, Cert))
            
        #Files in DER (a.k.a ASN1) format
        DerKeyPath = os.path.join(self.CertDir, cn + "_pkey.der")
        DerCsrPath = os.path.join(self.CertDir, cn + "_csr.der")
        DerCertPath = os.path.join(self.CertDir, cn + "_cert.der")
        if not self.OldPrivateKey:
            with open(DerKeyPath, "w") as fDerPrivKey:
                fDerPrivKey.write(crypto.dump_privatekey(FILETYPE_ASN1, Key))
        if not self.CsrFile:                
            with open(DerCsrPath, "w") as fDercsr:
                fDercsr.write(crypto.dump_certificate_request(FILETYPE_ASN1, Csr))
        with open(DerCertPath, "w") as fDercert:
            fDercert.write(crypto.dump_certificate(FILETYPE_ASN1, Cert))
            
        #Files in p12/PFX format
        P12CertPath = os.path.join(self.CertDir, cn + "_cert.p12")
        fP12cert = open(P12CertPath, "w")
        self.CreateP12(Key, Cert, fP12cert)
