import csv
from googleapiclient.discovery import build

api_key = "AIzaSyC_Jb4CAmXEeAaSRrFVEl4LBSvjKIFKVHA"
youtube = build('youtube', 'v3', developerKey=api_key)
dataRequired = ['lofi', 'Study with me']
for i in dataRequired:
    request = youtube.search().list(
        part="snippet",
        maxResults=100,
        q=f'{i}',
        type="video"
    )
    response = request.execute()

    with open(f'{i}.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t',
                            quoting=csv.QUOTE_ALL, quotechar='"')
        writer.writerow(['Title', 'Channel', 'Views', 'Comments'])
        for item in response['items']:
            videoId = item['id']['videoId']
            video_data = youtube.videos().list(
                part="snippet,statistics", id=videoId).execute()
            title = video_data['items'][0]['snippet']['title']
            channel = video_data['items'][0]['snippet']['channelTitle']
            view = video_data['items'][0]['statistics']['viewCount']
            comment = video_data['items'][0]['statistics'].get(
                'commentCount', 0)
            writer.writerow(
                [title, channel, view, comment])

    # with open(f'{i} search_results.json', 'w') as f:
    #     json.dump(response, f)
