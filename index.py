import sys
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError


def upload_file(dbx, local_file_path, dropbox_file_path):
    with open(local_file_path, 'rb') as f:
        # We use WriteMode=overwrite to make sure that the settings in the file
        # are changed on upload
        print("Uploading " + local_file_path + " to Dropbox as " + dropbox_file_path + "...")
        try:
            dbx.files_upload(f.read(), dropbox_file_path, mode=WriteMode('overwrite'))
        except ApiError as err:
            # This checks for the specific error where a user doesn't have
            # enough Dropbox space quota to upload this file
            if (err.error.is_path() and
                    err.error.get_path().reason.is_insufficient_space()):
                sys.exit("ERROR: Cannot upload; insufficient space.")
            elif err.user_message_text:
                print(err.user_message_text)
                sys.exit()
            else:
                print(err)
                sys.exit()

def sharing_dropbox_file(dbx, dropbox_file_path, receiver_email_list=[], message = "pioneeringdev shared this file.", access_level = 'viewer', add_message_as_comment = True):
    members = []
    # create list of MemberSelectors using receviers' email list.
    for receiver_email in receiver_email_list:
        members.append(dropbox.sharing.MemberSelector("email", receiver_email))

    dbx.sharing_add_file_member(file = dropbox_file_path, members = members, custom_message = message, quiet=False, access_level=dropbox.sharing.AccessLevel(access_level, None), add_message_as_comment = add_message_as_comment)


if __name__ == '__main__':

    TOKEN = '<my dropbox app token>'
    dbx = dropbox.Dropbox(TOKEN)

    # Check for an access token
    if (len(TOKEN) == 0):
        sys.exit("ERROR: Looks like you didn't add your access token. ")

    # Create an instance of a Dropbox class, which can make requests to the API.
    print("Creating a Dropbox object...")
    dbx = dropbox.Dropbox(TOKEN)

    # Check that the access token is valid
    try:
        dbx.users_get_current_account()
    except AuthError as err:
        sys.exit("ERROR: Invalid access token; try re-generating an "
            "access token from the app console on the web.")

    local_file_path = '/Volumes/data/test.pdf';
    dropbox_file_path = '/test.pdf'
    # Create a backup of the current settings file
    upload_file(dbx, local_file_path, dropbox_file_path)
    receiver_email_list = [
            "rumenslavov89@mail.bg",
            "carlag@hyperiondev.com"
    ]
    sharing_dropbox_file(dbx, dropbox_file_path, receiver_email_list = receiver_email_list, message = "pioneering shared this.", access_level = 'viewer', add_message_as_comment = True)


    print("Done!")
