api_key = None
if __name__ == '__main__':
    api_key = input("Enter your API key: ")
    if api_key:
        with open('data/api_key.txt', 'w') as f:
            f.write(api_key)