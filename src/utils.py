import json
import os
import pprint
import datetime

import isodate

from helper.youtube_api_manual import youtube, printj


def get_chanel(channel_id: str) -> dict:
    """Возвращает информацию о канале в виде словаря"""
    channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
    return channel["items"][0]


def get_info_about_chanel(channel_id: str) -> tuple:
    """Получаем 7 нужных нам данных о канале"""
    formated_dictionary = get_chanel(channel_id)
    id_chanel = formated_dictionary["id"]
    title_chanel = formated_dictionary["snippet"]["title"]
    description_chanel = formated_dictionary["snippet"]["description"]
    url_chanel = "https://www.youtube.com/channel/" + channel_id
    subscriberCount_chanel = formated_dictionary["statistics"]["subscriberCount"]
    videoCount_chanel = formated_dictionary["statistics"]["videoCount"]
    viewCount_chanel = formated_dictionary["statistics"]["viewCount"]

    return id_chanel, title_chanel, description_chanel, url_chanel, subscriberCount_chanel,\
        videoCount_chanel, viewCount_chanel


def get_video_statistic(video_id: str) -> tuple:
    """Возвращает информацию о видео. название, колличество, url, колличество лайков и коментариев"""
    try:
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=video_id
                                               ).execute()

        video_title = video_response['items'][0]['snippet']['title']
        view_count = video_response['items'][0]['statistics']['viewCount']
        video_url = "https://youtu.be/" + video_id
        like_count = video_response['items'][0]['statistics']['likeCount']
        comment_count = video_response['items'][0]['statistics']['commentCount']
        return video_title, view_count, video_url, like_count, comment_count

    except IndexError:
        return (None,) * 5


def get_video_statistic_by_playlist_id(video_id: str, playlist_id: str) -> tuple or None:
    """Возвращает информацию о видео. название, колличество, url,
    колличество лайков и коментариев используя id плэйлиста и видео
    """
    playlist_response = youtube.playlistItems().list(playlistId=playlist_id,
                                                     part='contentDetails',
                                                     maxResults=50,
                                                     ).execute()

    video_ids = [video['contentDetails']['videoId'] for video in playlist_response['items']]
    if video_id in video_ids:
        return get_video_statistic(video_id)
    return None


def get_playlist_info(playlist_id: str) -> tuple:
    """
    функция возвращает ссылку на плэйлист и название самого плэйлиста по id плэйлиста
    """
    playlist_url = "https://www.youtube.com/playlist?list=" + playlist_id
    playlist_title = ""
    playlist_videos = youtube.playlistItems().list(playlistId=playlist_id,
                                                   part='snippet',
                                                   maxResults=50,
                                                   ).execute()

    channel_id = playlist_videos["items"][0]["snippet"]["channelId"]
    playlists = youtube.playlists().list(channelId=channel_id,
                                         part='contentDetails,snippet',
                                         maxResults=50,
                                         ).execute()

    for playlist in playlists['items']:
        if playlist["id"] == playlist_id:
            playlist_title = playlist["snippet"]["title"]
            break
        else:
            playlist_title = None
    return playlist_url, playlist_title


def get_duration_all_videos(playlist_id: str) -> datetime.timedelta:
    """Получаем длительность всех видео плэйлиста"""
    playlist_videos = youtube.playlistItems().list(playlistId=playlist_id,
                                                   part='contentDetails',
                                                   maxResults=50,
                                                   ).execute()

    video_ids = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
    video_response = youtube.videos().list(part='contentDetails,statistics',
                                           id=','.join(video_ids)
                                           ).execute()

    total_duration = datetime.timedelta()
    for video in video_response['items']:
        # YouTube video duration is in ISO 8601 format
        iso_8601_duration = video['contentDetails']['duration']
        duration = isodate.parse_duration(iso_8601_duration)
        total_duration += duration

    return total_duration


def get_best_video(playlist_id: str) -> str:
    """Возвращает самое популярное видео плейлиста по количеству лайков"""
    url_best_video = "Нет информации"
    playlist_response = youtube.playlistItems().list(playlistId=playlist_id,
                                                     part='contentDetails',
                                                     maxResults=50,
                                                     ).execute()
    best_like = 0
    for video in playlist_response['items']:
        video_id = video['contentDetails']['videoId']
        # достаем количество лайков из кортежа
        like_counts = int(get_video_statistic(video_id)[3])

        if like_counts >= best_like:
            best_like = like_counts
            # достаем ссылку на видео из кортежа
            url_best_video = get_video_statistic(video_id)[2]

    return url_best_video


