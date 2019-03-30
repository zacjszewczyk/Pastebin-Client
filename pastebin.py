#!/usr/bin/python

# Class: Pastes
# Purpose: Provide access to a given user's Pastebin data
class Pastes:
    # Import libraries. Use built-in name mangling to
    # obfuscate imports.
    from sys import exit as __exit
    import requests as __req

    # Method: __init__
    # Purpose: Enumerate the user's Pastebin account
    # Parameters:
    # - key: Developer key (String)
    # - username: Username of the target user (String)
    # - password: Password of the target user (String)
    def __init__(self,key,username,password):
        # Make developer key available to methods
        self.key = key
        
        # Dictionary for pastes, with title as key and
        # paste values in a sub-dictionary
        # pastes[past title] = 
        # { paste_private: (0 = public, 1 = unlisted, 2 = private),
        #   paste_date: creation date,
        #   paste_format_short: syntax highlighting,
        #   paste_title: paste title,
        #   paste_expire_date: expiration date,
        #   paste_format_long: syntax highlighting,
        #   paste_size: paste size,
        #   paste_key: GUID for paste,
        #   paste_hits: number of hits,
        #   paste_url: url to paste }
        __items = {}

        # Collect the api_user_key
        __r = self.__req.post("https://pastebin.com/api/api_login.php", data={'api_dev_key':key,'api_user_name':username,'api_user_password':password})

        # Error checking for api_user_key query
        if ("Bad API request" in __r.text):
            print "ERROR: Bad response getting api_user_key."
            self.__exit(1)

        # Return the API user key and make it available to methods
        __api_user_key = __r.text.strip()
        self.ukey = __api_user_key

        # Get all pastes
        __r = self.__req.post("https://pastebin.com/api/api_post.php",data={'api_dev_key':key,'api_user_key':__api_user_key,'api_option':'list'})

        # Error checking for list of pastes
        if (("No pastes found." in __r.text) or ("Bad API request" in __r.text)):
            print "ERROR: Bad response getting pastes."
            self.__exit(1)

        # Turn the response into a "Pastes" data structure
        for __item in __r.text.replace("<paste>", "").strip().split("</paste>"):
            # Create a dictionary for paste attributes
            __data = {}
            __item = __item.strip() # Clear extra formatting
            # Discard empty paste entries
            if (len(__item) == 0):
                continue

            # Parse keys and values for the paste attributes.
            # Save the information in the "data" dictionary.
            for __field in __item.split('\n'):
                __fields = __field.strip()[:-1].split(">")
                __fields[0] = __fields[0][1:]
                __fields[1] = __fields[1].split("<")[0]
                __data[__fields[0]] = __fields[1]

            # Create a new entry in the pastes data structure, with
            # an individual paste's name as the key and a dictionary
            # of its attributes as the value.
            __items[__data["paste_title"]] = __data

        # Make the items variable available to methods in the class
        self.__items = __items

    # Method: getTitles
    # Purpose: Return an array containing all titles of user's pastes
    # Parameters:
    # - self: The class namespace (Object)
    def getTitles(self):
        return self.__items.keys()

    # Method: getPasteInfo
    # Purpose: Return attributes for a given paste
    # Parameters:
    # - self: The class namespace (Object)
    # - title: Title of the target note (String)
    def getPasteInfo(self, title):
        if (title not in self.__items.keys()):
            return "ERROR: Bad note request"
        return self.__items[title]

    def getPasteKey(self, title):
        return self.__items[title]["paste_key"]

    # Method: getPasteContent
    # Purpose: Return the content of a given paste
    # Parameters:
    # - self: The class namespace (Object)
    # - title: Title of the target note (String)
    def getPasteContent(self, title):
        # print self.getPasteKey(title)
        __r = self.__req.post("https://pastebin.com/api/api_raw.php",data={'api_dev_key':self.key,'api_user_key':self.ukey,'api_paste_key':self.getPasteKey(title),'api_option':'show_paste'})
        return __r.text

### -- ^- Methods, Code -v -- ###

if (__name__ == "__main__"):
    # Get Pastes data structure
    dev_key = ""
    username = ""
    password = ""
    pastes = Pastes(dev_key,username,password)

    print "Paste Information"
    print "================="
    while True:
        print "##. Title"
        i = 1
        opts = {}
        for each in pastes.getTitles():
            if (i < 10):
                print "0"+str(i)+".",each
            else:
                print i,". ",each
            opts[i] = each
            i += 1
        print

        user_input = raw_input("Select a paste by name or number, or enter \"exit\" to quit: ")

        if (user_input == "exit"):
            break
        elif (user_input.isdigit()):
            user_input = int(user_input)
            if (user_input not in opts.keys()):
                print "ERROR: Bad selection."
                continue
            result = opts[user_input],pastes.getPasteInfo(opts[user_input])
        else:
            result = user_input,pastes.getPasteInfo(user_input)

        while True:
            print "i: View attributes for '%s'" % result[0]
            print "d: Download content of '%s'" % result[0]
            user_input = raw_input("Enter selection: ")

            if ((user_input.isdigit()) or (len(user_input) > 1)):
                print "ERROR: Bad input."
                continue

            if (user_input == "i"):
                print "Information for '%s'" % (result[0])
                for key in result[1]:
                    print "    "+key+":",result[1][key]
                print
                break
            elif (user_input == "d"):
                print
                print "# BEGIN PASTE CONTENT #"
                print
                print pastes.getPasteContent(result[0])
                print
                print "# END PASTE CONTENT #"
                print
                break
            else:
                print "ERROR: Bad selection."