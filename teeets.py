from dota2.api import opendota

if __name__ == '__main__':
    file = open("/Volumes/MacintoshHD2/Shanks_Files/Shanks_Repo/dota2-recommonder/load.txt", "r")
    file2 = open('fecthed.txt', 'w')
    for player in file.read().split('\n'):
        print(player.split('#')[0])
        data = opendota.get_best_hero(player.split('#')[0])
        file2.write(player + '$$__$$' + str(data))
        file2.write('\n')

    file2.close()
