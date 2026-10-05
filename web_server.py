# -*- coding: utf-8 -*-
"""
Pocket FM Audio Drama Studio - Web Dashboard & YouTube Upload Hub
Provides:
1. Google OAuth 2.0 Channel Login & Multi-Channel Switcher
2. Live Channel Stats (Subscribers, Videos, Avatar, Handle)
3. Story Video & AI Climax Thumbnail Preview & Metadata Editor
4. Real-Time YouTube Upload with Live Progress Bar
5. Custom Video Upload & Upload History Log
"""

import os
import sys
import json
import uuid
import logging
import threading
from pathlib import Path
from typing import Dict, Any, List, Optional
from pydantic import BaseModel

from fastapi import FastAPI, Request, Query, Body, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse, FileResponse
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("StudioServer")

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"

ROOT_DIR = Path("C:/Audio-automation")
sys.path.append(str(ROOT_DIR))

from uploader.youtube_uploader import YouTubeUploader

CLIENT_SECRETS_FILE = ROOT_DIR / "client_secrets.json"
TOKENS_DIR = ROOT_DIR / "tokens"
TOKENS_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_DIR = ROOT_DIR / "config"
OUTPUT_DIR = ROOT_DIR / "output"
MASTERS_DIR = OUTPUT_DIR / "masters"
FRONTEND_DIR = ROOT_DIR / "frontend"
HISTORY_FILE = OUTPUT_DIR / "upload_history.json"
OAUTH_STATES_FILE = TOKENS_DIR / "oauth_pending_states.json"

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.readonly"
]

app = FastAPI(title="Pocket FM Drama Studio - YouTube Hub")

# Global Active Channel & Upload Tasks State
ACTIVE_CHANNEL_FILE = CONFIG_DIR / "active_channel.txt"
UPLOAD_TASKS: Dict[str, Dict[str, Any]] = {}


def get_active_channel() -> str:
    if ACTIVE_CHANNEL_FILE.exists():
        try:
            return ACTIVE_CHANNEL_FILE.read_text(encoding="utf-8").strip() or "vibration"
        except Exception:
            pass
    tokens = list(TOKENS_DIR.glob("token_*.json"))
    if tokens:
        return tokens[0].stem.replace("token_", "")
    return "default"


def set_active_channel(channel_id: str):
    ACTIVE_CHANNEL_FILE.parent.mkdir(parents=True, exist_ok=True)
    ACTIVE_CHANNEL_FILE.write_text(channel_id.strip(), encoding="utf-8")


def get_oauth_states() -> Dict[str, Any]:
    if OAUTH_STATES_FILE.exists():
        try:
            return json.loads(OAUTH_STATES_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def save_oauth_states(states: Dict[str, Any]):
    try:
        OAUTH_STATES_FILE.write_text(json.dumps(states, indent=2), encoding="utf-8")
    except Exception as e:
        logger.error(f"Failed to persist oauth states: {e}")


# --- FRONTEND ROUTE ---
@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return HTMLResponse(content=index_file.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>Pocket FM Studio Frontend is loading...</h1>", status_code=200)


# --- MEDIA SERVING FOR LOCAL PREVIEWS ---
@app.get("/media/file")
async def serve_local_media(path: str = Query(...)):
    p = Path(path)
    if not p.exists() or not p.is_file():
        raise HTTPException(status_code=404, detail="Media file not found")
    media_type = "video/mp4" if p.suffix.lower() == ".mp4" else ("image/png" if p.suffix.lower() == ".png" else "image/jpeg")
    return FileResponse(p, media_type=media_type)


# --- CHANNELS & AUTH APIS ---
@app.get("/api/channels/status")
async def get_channels_status():
    active_profile = get_active_channel()
    token_files = list(TOKENS_DIR.glob("token_*.json"))
    channels = []

    for tf in token_files:
        prof = tf.stem.replace("token_", "")
        try:
            uploader = YouTubeUploader(prof)
            info = uploader.get_channel_info()
            info["is_active"] = (prof == active_profile)
            channels.append(info)
        except Exception as e:
            channels.append({
                "connected": False,
                "profile": prof,
                "channel_title": prof.capitalize(),
                "error": str(e),
                "is_active": (prof == active_profile)
            })

    return {
        "active_channel": active_profile,
        "channels": channels,
        "total_connected": len([c for c in channels if c.get("connected")])
    }


@app.post("/api/channels/switch")
async def switch_channel(channel: str = Body(..., embed=True)):
    clean_ch = channel.lower().strip()
    set_active_channel(clean_ch)
    logger.info(f"Switched active upload channel to: {clean_ch}")
    return {"status": "success", "active_channel": clean_ch}


@app.get("/api/auth/login")
async def auth_login(profile: Optional[str] = Query(None)):
    if not CLIENT_SECRETS_FILE.exists():
        return JSONResponse({"error": "client_secrets.json is missing in C:/Audio-automation"}, status_code=500)

    # Use exact callback URL matching client_secrets.json redirect configuration
    redirect_uri = "http://localhost:8000/api/channels/oauth2callback"

    flow = Flow.from_client_secrets_file(
        str(CLIENT_SECRETS_FILE),
        scopes=SCOPES,
        redirect_uri=redirect_uri
    )
    auth_url, state = flow.authorization_url(
        prompt="consent",
        access_type="offline",
        include_granted_scopes="true"
    )

    states = get_oauth_states()
    states[state] = {
        "profile": (profile or f"channel_{int(uuid.uuid4().hex[:6], 16)}").lower().strip(),
        "verifier": getattr(flow, "code_verifier", None)
    }
    save_oauth_states(states)
    logger.info(f"Initiated Google OAuth for profile '{states[state]['profile']}'")

    return RedirectResponse(auth_url)


@app.get("/api/channels/oauth2callback")
async def oauth2_callback(code: str = Query(None), state: str = Query(None), error: str = Query(None)):
    if error:
        return HTMLResponse(f"""
        <html><body style="background:#090d16;color:#fff;font-family:sans-serif;padding:40px;text-align:center;">
        <h2 style="color:#ff4d4d;">OAuth Authentication Error</h2>
        <p>{error}</p>
        <a href="/" style="color:#00e5ff;font-weight:bold;">Return to Dashboard</a>
        </body></html>
        """, status_code=400)

    if not code:
        return HTMLResponse("<h3>No authorization code received</h3>", status_code=400)

    states = get_oauth_states()
    state_data = states.pop(state, {}) if state else {}
    save_oauth_states(states)

    target_profile = state_data.get("profile", "new_channel")
    code_verifier = state_data.get("verifier")
    redirect_uri = "http://localhost:8000/api/channels/oauth2callback"

    try:
        flow = Flow.from_client_secrets_file(
            str(CLIENT_SECRETS_FILE),
            scopes=SCOPES,
            redirect_uri=redirect_uri,
            state=state
        )
        if code_verifier:
            flow.code_verifier = code_verifier

        flow.fetch_token(code=code, code_verifier=code_verifier if code_verifier else None)
        creds = flow.credentials

        # Fetch channel profile info from YouTube API
        youtube = build("youtube", "v3", credentials=creds)
        res = youtube.channels().list(mine=True, part="snippet,statistics").execute()
        items = res.get("items", [])
        if not items:
            raise RuntimeError("No YouTube channel found associated with this Google Account.")

        ch = items[0]
        ch_id = ch.get("id", "")
        snippet = ch.get("snippet", {})
        stats = ch.get("statistics", {})

        ch_title = snippet.get("title", target_profile)
        custom_url = snippet.get("customUrl", "")
        thumbnails = snippet.get("thumbnails", {})
        avatar = thumbnails.get("high", {}).get("url") or thumbnails.get("default", {}).get("url", "")

        # Save token
        token_filename = f"token_{target_profile}.json"
        save_path = TOKENS_DIR / token_filename

        token_data = {
            "profile": target_profile,
            "channel_id": ch_id,
            "channel_title": ch_title,
            "custom_url": custom_url,
            "thumbnail": avatar,
            "subscriber_count": stats.get("subscriberCount", "Hidden"),
            "video_count": stats.get("videoCount", "0"),
            "token": creds.token,
            "refresh_token": creds.refresh_token,
            "token_uri": creds.token_uri,
            "client_id": creds.client_id,
            "client_secret": creds.client_secret,
            "scopes": creds.scopes
        }

        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(token_data, f, indent=2, ensure_ascii=False)

        # Set as currently active channel
        set_active_channel(target_profile)
        logger.info(f"Successfully saved and connected YouTube channel: '{ch_title}' ({custom_url})")

        return RedirectResponse(url=f"/?auth_success=1&channel={target_profile}")

    except Exception as e:
        logger.error(f"OAuth exchange failed: {e}")
        return HTMLResponse(f"""
        <html><body style="background:#090d16;color:#fff;font-family:sans-serif;padding:40px;text-align:center;">
        <h2 style="color:#ff4d4d;">YouTube Authentication Failed</h2>
        <p style="color:#94a3b8;">{str(e)}</p>
        <a href="/" style="display:inline-block;margin-top:20px;padding:10px 20px;background:#00e5ff;color:#000;text-decoration:none;border-radius:8px;font-weight:bold;">Return to Dashboard</a>
        </body></html>
        """, status_code=500)


# --- VIDEO ASSETS & METADATA APIS ---
@app.get("/api/videos/available")
async def get_available_videos():
    """Scans masters and output folders for rendered videos and pairs them with thumbnails and metadata."""
    videos = []
    search_dirs = [MASTERS_DIR, OUTPUT_DIR]

    seen_stems = set()
    for s_dir in search_dirs:
        if not s_dir.exists():
            continue
        for mp4_file in s_dir.glob("*.mp4"):
            stem = mp4_file.stem
            if stem in seen_stems:
                continue
            seen_stems.add(stem)

            # Look for thumbnail (.jpg or .png)
            thumb_path = None
            for ext in [".jpg", ".png", ".jpeg"]:
                candidate = s_dir / f"{stem}{ext}"
                if candidate.exists():
                    thumb_path = candidate
                    break
                candidate_thumb = s_dir / f"{stem}_thumbnail{ext}"
                if candidate_thumb.exists():
                    thumb_path = candidate_thumb
                    break

            if not thumb_path:
                for candidate_name in ["clean_cinematic_poster.jpg", "ai_thumbnail.jpg"]:
                    cand = ROOT_DIR / "output" / candidate_name
                    if cand.exists():
                        thumb_path = cand
                        break

            meta_json = s_dir / f"{stem}_metadata.json"
            meta_data = {}
            if meta_json.exists():
                try:
                    meta_data = json.loads(meta_json.read_text(encoding="utf-8"))
                except Exception:
                    pass

            file_size_mb = round(mp4_file.stat().st_size / (1024 * 1024), 2)
            mod_time = mp4_file.stat().st_mtime

            clean_name = stem.replace("_", " ").title()
            default_title = meta_data.get("title") or f"{clean_name} | Full Hindi Audio Drama (Pocket FM Style)"
            default_desc = meta_data.get("description") or (
                f"🔥 {default_title}\n\n"
                f"🎧 Headphones Recommended for 3D Audio Experience!\n\n"
                f"📖 Story Summary:\nEk dilchasp kahani jo aapko ant tak bandhe rakhegi.\n\n"
                f"⚡ Don't forget to Like, Share and Subscribe to the channel!\n\n"
                f"#PocketFM #AudioDrama #HindiKahaniya #DesiAudioStories #HindiKahani"
            )
            default_tags = meta_data.get("tags") or [
                "hindi audio drama", "pocket fm story", "hindi kahaniya",
                "horror audio story", "romantic drama", "suspense kahani", "desi audio stories"
            ]

            videos.append({
                "stem": stem,
                "file_name": mp4_file.name,
                "video_path": str(mp4_file.resolve()),
                "file_size_mb": file_size_mb,
                "modified_at": mod_time,
                "thumbnail_path": str(thumb_path.resolve()) if thumb_path else None,
                "thumbnail_url": f"/media/file?path={thumb_path.resolve()}" if thumb_path else None,
                "video_preview_url": f"/media/file?path={mp4_file.resolve()}",
                "title": default_title,
                "description": default_desc,
                "tags": default_tags if isinstance(default_tags, list) else default_tags.split(",")
            })

    videos.sort(key=lambda x: x["modified_at"], reverse=True)
    return {"videos": videos, "total": len(videos)}


# --- ASYNC UPLOAD ENGINE WITH PROGRESS ---
class UploadRequest(BaseModel):
    video_path: str
    title: str
    description: str
    tags: str
    privacy_status: str = "public"
    thumbnail_path: Optional[str] = None
    channel_profile: Optional[str] = None


def run_upload_worker(task_id: str, req: UploadRequest):
    try:
        active_prof = req.channel_profile or get_active_channel()
        uploader = YouTubeUploader(active_prof)

        def progress_cb(pct: int, current_bytes: Optional[int], total_bytes: Optional[int], msg: str = ""):
            UPLOAD_TASKS[task_id].update({
                "percent": pct,
                "message": msg,
                "uploaded_mb": round((current_bytes or 0) / (1024 * 1024), 2),
                "total_mb": round((total_bytes or 0) / (1024 * 1024), 2)
            })

        UPLOAD_TASKS[task_id]["status"] = "uploading"
        UPLOAD_TASKS[task_id]["message"] = "Initializing YouTube upload..."

        result = uploader.upload_video(
            video_path=Path(req.video_path),
            title=req.title,
            description=req.description,
            tags=req.tags,
            privacy_status=req.privacy_status,
            thumbnail_path=Path(req.thumbnail_path) if req.thumbnail_path else None,
            progress_callback=progress_cb
        )

        UPLOAD_TASKS[task_id].update({
            "status": "completed",
            "percent": 100,
            "message": "Published successfully!",
            "result": result
        })
        logger.info(f"Upload task {task_id} completed: {result.get('url')}")

    except Exception as e:
        logger.error(f"Upload task {task_id} failed: {e}", exc_info=True)
        UPLOAD_TASKS[task_id].update({
            "status": "failed",
            "message": str(e),
            "error": str(e)
        })


@app.post("/api/upload/start")
async def start_upload(req: UploadRequest, background_tasks: BackgroundTasks):
    v_path = Path(req.video_path)
    if not v_path.exists():
        raise HTTPException(status_code=400, detail=f"Video file not found at: {req.video_path}")

    task_id = str(uuid.uuid4())
    UPLOAD_TASKS[task_id] = {
        "task_id": task_id,
        "status": "queued",
        "percent": 0,
        "message": "Queued for upload...",
        "video_title": req.title,
        "channel": req.channel_profile or get_active_channel()
    }

    background_tasks.add_task(run_upload_worker, task_id, req)
    return {"status": "started", "task_id": task_id}


@app.get("/api/upload/progress/{task_id}")
async def get_upload_progress(task_id: str):
    if task_id not in UPLOAD_TASKS:
        raise HTTPException(status_code=404, detail="Task ID not found")
    return UPLOAD_TASKS[task_id]


@app.get("/api/history")
async def get_history():
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []


if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("   🎙️ Pocket FM Studio - YouTube Automation Hub Server")
    print("="*60)
    print("  Local URL: http://localhost:8000")
    print("  Connecting with client_secrets.json from C:/Audio-automation")
    print("="*60 + "\n")
    uvicorn.run("web_server:app", host="127.0.0.1", port=8000, reload=False)
