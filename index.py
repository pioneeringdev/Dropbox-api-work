import sys
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

def upload_resume(dbx, local_file_path, dropbox_file_path):
    with open(local_resume_file_path, 'rb') as f:
        # We use WriteMode=overwrite to make sure that the settings in the file
        # are changed on upload
        print("Uploading " + local_resume_file_path + " to Dropbox as " + dropbox_resume_file_path + "...")
        try:
            dbx.files_upload(f.read(), dropbox_resume_file_path, mode=WriteMode('overwrite'))
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

if __name__ == '__main__':

    TOKEN = ''
    dbx = dropbox.Dropbox(TOKEN)
    local_resume_file_path = '';
    dropbox_resume_file_path = '/test.pdf'
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

    # Create a backup of the current settings file
    upload_resume(dbx, local_resume_file_path, dropbox_resume_file_path)

    # # Change the user's file, create another backup
    # change_local_file("updated")
    # backup()
    #
    # # Restore the local and Dropbox files to a certain revision
    # to_rev = select_revision()
    # restore(to_rev)

    print("Done!")
