from configparser import ConfigParser

def setup(config_path):
    configur = ConfigParser()
    configur.read(config_path)

    user_name = configur.get('default', 'user_name')
    email = configur.get('default', 'email_address')

    while True:
        print('you are in setup mode')
        user_name = input('Enter user name: ')
        print("Would you like to provide Email, for Gmail mail send only")
        print("This will only use to send email. I am not asking for password.")
        ch = input("Type y/Y to YES or anything else to NO: ")
        if ch.lower() == 'y':
            email_id = input("Enter your Email ID: ")
            if email_id != '':
                email = email_id
                break
        else:
            break

    configur.set('default', 'user_name', user_name)
    configur.set('default', 'email_address', email)

    with open(config_path, 'w') as configfile:  # save
        configur.write(configfile)

    print("Setup Completed")

