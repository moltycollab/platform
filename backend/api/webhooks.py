from fastapi import APIRouter, Request, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Dict, Any
import json
import hashlib
import hmac
from services.github_service import github_app_service


router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.post("/github")
async def github_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Handle GitHub webhooks
    """
    # Get the payload and signature
    payload = await request.body()
    signature = request.headers.get('X-Hub-Signature-256')
    
    if not signature:
        raise HTTPException(status_code=400, detail="Missing signature")
    
    # Verify the signature
    if not github_app_service.verify_webhook_signature(payload, signature):
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    # Parse the payload
    try:
        payload_json = json.loads(payload.decode('utf-8'))
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
    
    # Get the event type
    event_type = request.headers.get('X-GitHub-Event')
    delivery_id = request.headers.get('X-GitHub-Delivery')
    
    print(f"Received GitHub webhook: {event_type}, ID: {delivery_id}")
    
    # Process the event based on type
    if event_type == "push":
        background_tasks.add_task(handle_push_event, payload_json)
    elif event_type == "pull_request":
        background_tasks.add_task(handle_pull_request_event, payload_json)
    elif event_type == "issues":
        background_tasks.add_task(handle_issues_event, payload_json)
    elif event_type == "installation":
        background_tasks.add_task(handle_installation_event, payload_json)
    elif event_type == "installation_repositories":
        background_tasks.add_task(handle_installation_repositories_event, payload_json)
    else:
        print(f"Unhandled event type: {event_type}")
    
    return JSONResponse(content={"status": "received", "event": event_type, "id": delivery_id})


def handle_push_event(payload: Dict[str, Any]):
    """Handle push events"""
    repository = payload.get("repository", {})
    commits = payload.get("commits", [])
    ref = payload.get("ref", "")  # e.g., "refs/heads/main"
    
    print(f"Push event to {repository.get('name')}, branch {ref}, {len(commits)} commits")
    
    # Process each commit
    for commit in commits:
        author = commit.get("author", {})
        message = commit.get("message", "")
        print(f"Commit by {author.get('name', 'unknown')}: {message}")


def handle_pull_request_event(payload: Dict[str, Any]):
    """Handle pull request events"""
    action = payload.get("action", "")
    pull_request = payload.get("pull_request", {})
    repository = payload.get("repository", {})
    
    print(f"Pull request {action} in {repository.get('name')}: #{pull_request.get('number')} - {pull_request.get('title')}")
    
    # Different actions require different processing
    if action == "opened":
        print("New pull request opened")
    elif action == "closed":
        print("Pull request closed")
    elif action == "synchronize":
        print("Pull request updated")


def handle_issues_event(payload: Dict[str, Any]):
    """Handle issues events"""
    action = payload.get("action", "")
    issue = payload.get("issue", {})
    repository = payload.get("repository", {})
    
    print(f"Issue {action} in {repository.get('name')}: #{issue.get('number')} - {issue.get('title')}")


def handle_installation_event(payload: Dict[str, Any]):
    """Handle installation events"""
    action = payload.get("action", "")
    installation = payload.get("installation", {})
    repositories = payload.get("repositories", [])
    
    print(f"Installation {action} for user {installation.get('account', {}).get('login')}")
    print(f"Repositories affected: {len(repositories)}")


def handle_installation_repositories_event(payload: Dict[str, Any]):
    """Handle installation repositories events"""
    action = payload.get("action", "")
    installation = payload.get("installation", {})
    repositories_added = payload.get("repositories_added", [])
    repositories_removed = payload.get("repositories_removed", [])
    
    print(f"Installation repositories {action}")
    print(f"Added: {len(repositories_added)}, Removed: {len(repositories_removed)}")