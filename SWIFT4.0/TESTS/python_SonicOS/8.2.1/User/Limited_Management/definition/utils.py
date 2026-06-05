
#Check group memberships for the limit local user, include case 1, 2.
def user_member_check(output, gpname, username):
    checkresult = False
    try:
        for gpnum in output['user']['local']['group']:
            if gpnum['name'] == gpname:
                for gpmember in gpnum['member']:
                    if gpmember['name'] == username:
                        checkresult = True
    except:
        logger.error('Get the local user status failed !')
    return checkresult