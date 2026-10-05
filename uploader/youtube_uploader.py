# -*- coding: utf-8 -*-
"""
Studio YouTube Uploader for Pocket FM Drama Pipeline:
- Authenticates using Google OAuth 2.0 Credentials (client_secrets.json & token files).
- Multi-channel support (switch dynamically between connected channels).
- High-speed resumable chunked upload with real-time percentage progress callback.
- Sets viral Title, SEO Description, Tags, Category, and Hindi language metadata.
- Automatically uploads high-CTR Climax 16:9 Thumbnail.
- Logs upload history.
"""

import os
import sys
import json
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("YouTubeUploader")

ROOT_DIR = Path("C:/Audio-automation")
CLIENT_SECRETS_FILE = ROOT_DIR / "client_secrets.json"
TOKENS_DIR = ROOT_DIR / "tokens"
TOKENS_DIR.mkdir(parents=True, exist_ok=True)
HISTORY_FILE = ROOT_DIR / "output" / "upload_history.json"

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly"
]


class YouTubeUploader:
    def __init__(self, channel_profile: str = "vibration"):
        self.profile = channel_profile.lower().strip()
        self.tokens_dir = TOKENS_DIR
        self.client_secrets_file = CLIENT_SECRETS_FILE

    def get_token_file(self) -> Path:
        return self.tokens_dir / f"token_{self.profile}.json"

    def get_authenticated_service(self):
        """Builds authenticated YouTube Data API v3 service from token file."""
        t_file = self.get_token_file()
        if not t_file.exists():
            # Check for any token file if specified profile doesn't exist
            available_tokens = list(self.tokens_dir.glob("token_*.json"))
            if available_tokens:
                t_file = available_tokens[0]
                self.profile = t_file.stem.replace("token_", "")
            else:
                raise FileNotFoundError(
                    f"No YouTube token found for channel '{self.profile}'. Please login via the dashboard first."
                )

        with open(t_file, "r", encoding="utf-8") as f:
            t_data = json.load(f)

        creds = Credentials.from_authorized_user_info(t_data)
        if not creds.valid:
            if creds.refresh_token:
                logger.info(f"Refreshing YouTube token for channel profile '{self.profile}'...")
                creds.refresh(Request())
                # Update saved token file with fresh access token
                t_data["token"] = creds.token
                with open(t_file, "w", encoding="utf-8") as f:
                    json.dump(t_data, f, indent=2, ensure_ascii=False)
            else:
                raise ValueError("YouTube credentials expired and no refresh token available. Re-login required.")

        return build("youtube", "v3", credentials=creds)

    def get_channel_info(self) -> Dict[str, Any]:
        """Fetches live channel statistics from YouTube API."""
        try:
            youtube = self.get_authenticated_service()
            res = youtube.channels().list(mine=True, part="snippet,statistics").execute()
            items = res.get("items", [])
            if not items:
                return {"connected": False, "error": "No channel found"}

            ch = items[0]
            snippet = ch.get("snippet", {})
            stats = ch.get("statistics", {})

            thumbnails = snippet.get("thumbnails", {})
            avatar_url = (
                thumbnails.get("high", {}).get("url")
                or thumbnails.get("medium", {}).get("url")
                or thumbnails.get("default", {}).get("url", "")
            )

            return {
                "connected": True,
                "profile": self.profile,
                "channel_id": ch.get("id", ""),
                "channel_title": snippet.get("title", ""),
                "custom_url": snippet.get("customUrl", ""),
                "description": snippet.get("description", ""),
                "thumbnail": avatar_url,
                "subscriber_count": stats.get("subscriberCount", "Hidden"),
                "video_count": stats.get("videoCount", "0"),
                "view_count": stats.get("viewCount", "0")
            }
        except Exception as e:
            logger.error(f"Error fetching channel info: {e}")
            return {"connected": False, "profile": self.profile, "error": str(e)}

    def upload_video(
        self,
        video_path: Path,
        title: str,
        description: str,
        tags: Optional[List[str]] = None,
        privacy_status: str = "public",
        category_id: str = "24",  # 24 = Entertainment, 1 = Film & Animation
        thumbnail_path: Optional[Path] = None,
        progress_callback: Optional[Callable[[int, int, int, str], None]] = None
    ) -> Dict[str, Any]:
        """
        Uploads a video to YouTube with chunked resumable upload and progress reporting.
        """
        video_path = Path(video_path)
        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")

        file_size = video_path.stat().st_size
        logger.info(f"Starting YouTube upload: '{title}' ({file_size / (1024 * 1024):.2f} MB) on channel '{self.profile}'")

        if progress_callback:
            progress_callback(0, 0, file_size, "Authenticating YouTube service...")

        youtube = self.get_authenticated_service()

        if isinstance(tags, str):
            clean_tags = [t.strip() for t in tags.split(",") if t.strip()]
        elif isinstance(tags, list):
            clean_tags = [str(t).strip() for t in tags if str(t).strip()]
        else:
            clean_tags = ["Hindi Audio Drama", "Pocket FM", "Kahani", "Desi Audio Stories"]

        body = {
            "snippet": {
                "title": title[:100],  # YouTube title max 100 chars
                "description": description[:5000],  # Max 5000 chars
                "tags": clean_tags[:50],
                "categoryId": str(category_id),
                "defaultLanguage": "hi",
                "defaultAudioLanguage": "hi"
            },
            "status": {
                "privacyStatus": privacy_status.lower(),
                "selfDeclaredMadeForKids": False
            }
        }

        # 5 MB upload chunk size for smooth progress
        chunk_size = 5 * 1024 * 1024
        media = MediaFileUpload(
            str(video_path),
            mimetype="video/mp4",
            chunksize=chunk_size,
            resumable=True
        )

        insert_request = youtube.videos().insert(
            part="snippet,status",
            body=body,
            media_body=media
        )

        if progress_callback:
            progress_callback(1, 0, file_size, "Uploading video chunks...")

        response = None
        while response is None:
            status, response = insert_request.next_chunk()
            if status:
                pct = int(status.progress() * 100)
                uploaded_bytes = status.resumable_progress
                total_bytes = status.total_size
                logger.info(f"  [YouTubeUploader] Upload progress: {pct}% ({uploaded_bytes / (1024*1024):.1f}/{total_bytes / (1024*1024):.1f} MB)")
                if progress_callback:
                    progress_callback(pct, uploaded_bytes, total_bytes, f"Uploading: {pct}%")

        video_id = response.get("id")
        if not video_id:
            raise RuntimeError(f"Upload failed, no video ID returned: {response}")

        logger.info(f"Video uploaded successfully! ID: {video_id}")

        # Set custom thumbnail if provided
        thumb_status = "none"
        if thumbnail_path and Path(thumbnail_path).exists():
            logger.info(f"Attaching custom Climax Thumbnail: {thumbnail_path.name}")
            if progress_callback:
                progress_callback(95, file_size, file_size, "Attaching custom 16:9 thumbnail...")
            try:
                thumb_mime = "image/png" if str(thumbnail_path).lower().endswith(".png") else "image/jpeg"
                youtube.thumbnails().set(
                    videoId=video_id,
                    media_body=MediaFileUpload(str(thumbnail_path), mimetype=thumb_mime)
                ).execute()
                thumb_status = "attached"
                logger.info("Custom thumbnail attached successfully!")
            except Exception as e:
                thumb_status = f"failed: {e}"
                logger.warning(f"Could not attach thumbnail (channel may need phone verification): {e}")

        result = {
            "status": "success",
            "video_id": video_id,
            "url": f"https://youtu.be/{video_id}",
            "studio_url": f"https://studio.youtube.com/video/{video_id}/edit",
            "title": title,
            "privacy": privacy_status,
            "thumbnail_status": thumb_status,
            "channel_profile": self.profile,
            "uploaded_at": datetime.now().isoformat()
        }

        if progress_callback:
            progress_callback(100, file_size, file_size, "Upload Complete! Published to YouTube.")

        self._save_history(result)
        return result

    def _save_history(self, record: Dict[str, Any]):
        HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
        history = []
        if HISTORY_FILE.exists():
            try:
                history = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
            except Exception:
                history = []
        history.insert(0, record)
        try:
            HISTORY_FILE.write_text(json.dumps(history, indent=2, ensure_ascii=False), encoding="utf-8")
        except Exception as e:
            logger.error(f"Failed to record upload history: {e}")
