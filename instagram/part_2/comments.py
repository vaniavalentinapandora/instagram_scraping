import requests, json, time, csv

query_hash = 'bc3296d1ce80a24b1b6e40b1e72903f5'
url = 'https://www.instagram.com/graphql/query'
end_cursor = ''
short_code = 'B7ZiihrnaZl'
count = 0
counter_file = 1
jumlah_per_file = 100

writer = csv.writer(open('comment_results/{} {}.csv'.format(short_code, counter_file), 'w', newline=''))
headers = ['User Name', 'Text']
writer.writerow(headers)
while 1:
    varibles = {"shortcode":short_code,"first":50}
    params = {
        'query_hash': query_hash,
    'variables': json.dumps(varibles)
    }
    r = requests.get(url, params=params).json()
    #print(r)
    try:
        users = r['data']['shortcode_media']['edge_media_to_parent_comment']['edges']
    except:
        print('Wait for 20 secs')
        time.sleep(30)
        continue

    #print(users)
    for user in users:
        if count % jumlah_per_file == 0 and count!=0:
            counter_file +=1
            writer = csv.writer(open('comment_results/{} {}.csv'.format(short_code, counter_file), 'w', newline=''))
            headers = ['User Name', 'Text']
            writer.writerow(headers)
        username = user['node']['owner']['username']
        text = user['node']['text']
        writer = csv.writer(open('comment_results/{} {}.csv'.format(short_code, counter_file), 'a', newline='', encoding='utf-8'))
        data = [username, text]
        writer.writerow(data)
        count+=1
        print(count, username, text)

    end_cursor = r['data']['shortcode_media']['edge_media_to_parent_comment']['page_info']['end_cursor']
    has_next_page = r['data']['shortcode_media']['edge_media_to_parent_comment']['page_info']['has_next_page']
    if has_next_page == False: break
    time.sleep(2)