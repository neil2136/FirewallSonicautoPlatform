import re
from runner.settings import logger
class AntiSpamCLI():
    """Anti spam cli class"""
    def __init__(self, fw):
        self.fw = fw
    def show_anti_spam_config(self,*kwargs):
        """
        example:-
        command="allow-list","reject-list"
        output=antispam.show_anti_spam_config(*commands)
        """
        supported_commands=" " , "allow-list" , "reject-list" , "status" , "statistics"
        commands = [" "]
        for command in kwargs:
            if  command in supported_commands :
                commands.append("show anti-spam " + command)
            else:
                logger.error("'"+command+"'" + " is not a supported command ")
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output

    def config_settings(self,tag=0,**kwargs):
        """

        """
        commands = [" ","configure","anti-spam"]
        for command in kwargs.keys():
            if command in ["definite-phishing","definite-spam","definite-virus","likely-phishing","likely-spam","likely-virus"] :
                commands.append("action " + command + " " + kwargs[command])

            if  command in ["allow-list", "reject-list"]:
                commands.append(command+ " " +"name " + kwargs[command] )

            if command in ["allow-list_fqdn","allow-list_host","allow-list_range", "reject-list_fqdn","reject-list_host","reject-list_range","probe_interval","probe_timeout","mail-server_public","mail-server_private","mail-server_port"]:
                splited_commend=re.split("_",command)
                commands.append(splited_commend[0]+ " "+ splited_commend[1] +" " + kwargs[command] )
                if splited_commend[0] in ["allow-list","reject-list"]:
                    commands.append("yes")

            if command in ["system-detection","destination-mail-address-as-junk-store"]:
                if kwargs[command] == True:
                    commands.append(command)
                # else:
                #     commands.append("no "+ command)
            if command in ["enable"]:
                if kwargs[command] == True:
                    commands.append(command)
                else:
                    commands.append(command)
                    commands.append("yes")
                    commands.append("destination-mail-server"+" public "+kwargs[command]["destination-mail-server"]["public"]+" private "+kwargs[command]["destination-mail-server"]["private"]+" zone "+kwargs[command]["destination-mail-server"]["zone"]+" port "+kwargs[command]["destination-mail-server"]["port"])
                    commands.append("commit")
                    commands.append("cancel")

            if command in ["service-down","junk-store-ip","failure-threshold","success-threshold"]:
                commands.append(command + " " + kwargs[command] )

            if command in ["junk-box"]:
                commands.append("junk-box " + "down " + kwargs[command] )
        for command in ['commit','exit', 'exit']:
            commands.append(command)
            result = self.fw.do_cli_commands(commands, tag=tag)    
            return result


    def del_config(self,tag=0,**kwargs):
        """

        """
        commands = [" ","configure","anti-spam"]
        for command in kwargs.keys():
            if  command in ["allow-list", "reject-list"]:
                commands.append("no " + command+ " " +"name " + kwargs[command] )

            if command in ["allow-list_fqdn","allow-list_host","allow-list_range", "reject-list_fqdn","reject-list_host","reject-list_range","mail-server_public","mail-server_private","mail-server_port"]:
                splited_commend=re.split("_",command)
                if splited_commend[0] in ["allow-list","reject-list"]:
                    commands.append("no " + splited_commend[0]+ " "+ splited_commend[1] +" " + kwargs[command] )
                else:
                    commands.append("no " + splited_commend[0]+ " "+ splited_commend[1] )
            if command in ["system-detection","destination-mail-address-as-junk-store","enable"]:
                if kwargs[command] == False:
                    commands.append("no "+ command)


        for command in ['commit','exit']:
            commands.append(command)
        result = self.fw.do_cli_commands(commands, tag=tag)                 
        return result
               
class RblCli():
    def __init__(self, fw):
        self.fw=fw
    def show_rbl_config(self,*kwargs):
        """
        example:-
        """
        supported_commands=" " , "blacklist" , "service" , "services" , "statistics" , "whitelist"
        commands = [" "]
        for command in kwargs:
            if  command in supported_commands :
                commands.append("show rbl " + command)
            else:
                if str(type(command)) == "<class 'list'>":
                    commands.append("show rbl " + command[0])
                    for i in range (1 ,len(command)):
                        commands[-1]=commands[-1] + " " + command[i]
                else:
                    logger.error("'"+str(command)+"'" + " is not a supported command ")
        output = self.fw.do_cli_commands(commands, tag=1)[1]
        return output

    def config_settings(self,tag=0,**kwargs):
        """

        """
        commands = [" ","configure","rbl"]
        for command in kwargs.keys():
            if command in "enable":
                if kwargs[command]:
                    commands.append(command)
                else:
                    commands.append("no "+command)
            if  command in ["blacklist", "whitelist"]:
                commands.append(command+ " " +"name " + kwargs[command] )

            if command in ["whitelist_fqdn","whitelist_host","whitelist_range", "blacklist_fqdn","blacklist_host","blacklist_range"]:
                splited_commend=re.split("_",command)
                commands.append(splited_commend[0]+ " " )
                for i in range(1,len(splited_commend)):
                    commands[-1]=commands[-1]+(splited_commend[i]+ " ")
                commands[-1]=commands[-1]+ (kwargs[command] )
                if splited_commend[0] in ["whitelist","blacklist"]:
                    commands.append("yes")

            if command in ["service","dns"]:
                if len(kwargs[command]) ==1:
                    commands.append(command+" " + kwargs[command][0 ])
                else:
                    commands.append(command+" " + kwargs[command][0])
                    for i in range (1 ,len(kwargs[command])):
                        commands.append(" " + kwargs[command][i])
                # splited_commend=re.split("_",kwargs[command])
                # commands.append(command+ " " )
                # for i in range(0,len(splited_commend)-1):
                #     commands[-1]=commands[-1]+(splited_commend[i]+ " ")
                # if splited_commend[1] != "enable":
                #     commands.append(splited_commend[-1])
            # if str(type(kwargs[command])) == "<class 'list'>":
            #     print("dddddddddddddddddddddddd")
            #     print(kwargs[command])
            #     commands.append(command)
            #     for i in range (0 ,len(kwargs[command])):
            #         commands[-1]=commands[-1] + " " + kwargs[command][i]
            # if kwargs[command] == True:
            #     commands.append(command)
            # #if kwargs[command] == False:
            #     commands.append("no " + command)

                
        for command in ['commit','exit', 'exit']:
            commands.append(command)
            result = self.fw.do_cli_commands(commands, tag=tag)    
            return result

    def delete_config(self,tag=0,**kwargs):
        """

        """
        commands = [" ","configure","rbl"]
        for command in kwargs.keys():
            if  command in ["blacklist", "whitelist"]:
                commands.append("no " + command+ " " +"name " + kwargs[command] )
        if command in ["service","dns"]:
                if len(kwargs[command]) ==1:
                    commands.append("no "+command+" " + kwargs[command][0 ])
                else:
                    commands.append(command+" " + kwargs[command][0])
                    for i in range (1 ,len(kwargs[command])):
                        commands.append("no "+ kwargs[command][i])

        for command in ['commit','exit', 'exit']:
                commands.append(command)
                result = self.fw.do_cli_commands(commands, tag=tag)    
                return result