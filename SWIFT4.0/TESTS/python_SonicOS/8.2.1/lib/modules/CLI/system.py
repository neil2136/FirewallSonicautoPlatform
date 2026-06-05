from urllib.request import quote
from runner.settings import logger
import os
import execjs
from modules.CLI.system import StatusCli
from modules.CLI.system import LicenseCli
from modules.CLI.system import AdminCli
from modules.CLI.system import SNMPCli
from modules.CLI.system import CertificateCli
from modules.CLI.system import TimeCli
from modules.CLI.system import ScheduleCli
from modules.CLI.system import SettingCli
from modules.CLI.system import PacketmonitorCli
from modules.CLI.system import PacketreplayCli
from modules.CLI.system import DiagnosticsCli
from modules.CLI.system import RestartCli
from modules.CLI.system import LegalinforCli

''' ========= System Menu =========
    Created by Vera. sgao@sonicwall.com
    Status
    License
    Administration
    SNMP
    Certificates
    Time
    Schedules
    Settings
    Packet Monitor
    Packet Replay
    Diagnostics
    Restart
    Legal Information
'''

class StatusCli(StatusCli):
    ''' StatusCli '''

        

class LicenseCli(LicenseCli):
    ''' LicenseCli '''
#    def cryptojs_aes_encrypt(
#        self,
#        timestamp,
#        serial,
#        name='auto_email@sonicwall.com',
#        password='automation',
#        iv_str='f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff'):
#
#        logger.info(f"{timestamp}, {serial}, {name}, {password}")
#        js = """const h = require('crypto-js');
#            encrypt = function(timestamp, serial, name, password, iv_str) {
#                let usr = name;
#                if (usr.length > 5) {
#                  usr = usr.substring(0, 6);
#                }
#                const psk = 'V#N8=a7q&2Qq@9l3$)';
#                const key = `${usr}${psk}`;
#
#                // --------------- addPadding function -------------------
#                const padLen = 7 - (password.length % 8);
#                console.log(padLen);
#                const bytes = new Uint8Array(password.length + padLen + 1);
#                const padBytes = new Uint8Array(padLen);
#                for (let k = 0; k < padLen; k++) { // eslint-disable-line
#                  // ========= getRandomInt function ==============
#                  padBytes[k] = Math.floor(Math.random() * 127);
#                  // ========= getRandomInt function end ==========
#                }
#
#                for (let j = 0; j < password.length; j++) { // eslint-disable-line
#                  bytes[j] = password.charCodeAt(j);
#                }
#
#                for (let i = password.length, n = 0; i < (password.length + padLen); i++, n++) {
#                  // eslint-disable-line
#                  bytes[i] = padBytes[n];
#                }
#
#                bytes[password.length + padLen] = padLen;
#
#                // ========= binArrayToString function =============
#                let str = '';
#                for (let i = 0; i < bytes.length; i++) { // eslint-disable-line
#                  str += String.fromCharCode(bytes[i]);
#                }
#                // str is encypted pass
#                // ========= binArrayToString function end =========
#                // --------------- addPadding function end ---------------
#
#                const cipher = h.TripleDES.encrypt(str, h.enc.Utf8.parse(key), {
#                  mode: h.mode.ECB,
#                  padding: h.pad.NoPadding,
#                });
#
#                // console.log(`${name} <==> ${password} <==> ${ cipher.toString() }`);
#                const encryptedPwd = cipher.toString();
#
#                const timeHex = timestamp.toString(16)
#                .padStart(20, '0');
#                const sharedSecret = `${serial}${timeHex}`;
#                // console.log(sharedSecret);
#                const message = `${name}$$$${encryptedPwd}`;
#
#                // TODO: will revisit this
#                const iv = h.enc.Hex.parse(iv_str);
#                const secret = h.enc.Hex.parse(sharedSecret);
#
#                return  h.AES.encrypt(message, secret, { iv: iv, padding: h.pad.ZeroPadding }).toString(h.format.Hex);
#                // eslint-disable-line
#              };
#        """
#        ctx = execjs.compile(js, cwd=os.environ['PYTHON_COMMON_HOME']+'/tools')
#        res = ctx.call('encrypt',timestamp, serial, name, password, iv_str)
#        return res


class AdminCli(AdminCli):
    ''' AdminCli '''


class SNMPCli(SNMPCli):
    ''' SNMPCli '''


class CertificateCli(CertificateCli):
    ''' CertificateCli '''


class TimeCli(TimeCli):
    ''' TimeCli '''


class ScheduleCli(ScheduleCli):
    ''' ScheduleCli '''


class SettingCli(SettingCli):
    ''' SettingCli '''


class PacketmonitorCli(PacketmonitorCli):
    ''' PacketmonitorCli '''


class PacketreplayCli(PacketreplayCli):
    ''' No CLI support at present '''


class DiagnosticsCli(DiagnosticsCli):
    ''' DiagnosticsCli '''


class RestartCli(RestartCli):
    ''' RestartCli '''


class LegalinforCli(LegalinforCli):
    ''' No CLI support at present '''

