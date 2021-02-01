from fomc.FOMCClient import FOMCClient

if __name__ == '__main__':
    fomc_client = FOMCClient()
    print(fomc_client.get_all_materials())
