import sys
sys.path.insert(1, '../../colab-cli/colab_cli')
import cli_new
import gdrive_authentication


def main():
    print('test')
    #gdrive_authentication.colab_gdrive_auth()

    gdrive_authentication.drive_auth()
    print('oops')


if __name__ == "__main__":
    main()
