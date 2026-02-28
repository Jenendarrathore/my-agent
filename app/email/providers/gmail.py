import base64
from typing import List, Optional, Any, Dict
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build, Resource
from google.auth.transport.requests import Request
from app.email.providers.base import EmailProvider
from app.email.dto import EmailMessage
from app.email.exceptions import EmailAuthError, EmailFetchError
from datetime import datetime, timezone


class GmailProvider(EmailProvider):
    """
    Gmail API implementation of the EmailProvider.
    Stateless per session: credentials must be provided to connect().
    """

    def __init__(self):
        self._service: Optional[Resource] = None
        self._creds: Optional[Credentials] = None

    async def connect(self, credentials_data: Dict[str, Any]) -> None:
        """
        Connect to Gmail using OAuth2 credentials.
        :param credentials_data: Dict with access_token, refresh_token, client_id, client_secret.
        """
        try:
            self._creds = Credentials(
                token=credentials_data.get("access_token"),
                refresh_token=credentials_data.get("refresh_token"),
                client_id=credentials_data.get("client_id"),
                client_secret=credentials_data.get("client_secret"),
                token_uri="https://oauth2.googleapis.com/token"
            )

            # Refresh token if expired
            if self._creds.expired and self._creds.refresh_token:
                self._creds.refresh(Request())

            # build() is a synchronous call, in a real production app we might offload
            # it to a thread if latency is critical, but for workers it's fine.
            self._service = build("gmail", "v1", credentials=self._creds)
            
        except Exception as e:
            raise EmailAuthError(f"Oauth2 connection failed: {str(e)}", provider="gmail")

    async def fetch_messages(
        self, 
        cursor: Optional[str] = None, 
        limit: int = 50
    ) -> List[EmailMessage]:
        """
        Fetch a list of message summaries from Gmail.
        """
        if not self._service:
            raise EmailAuthError("Provider not connected", provider="gmail")

        try:
            # Note: q parameter can be added for filtering in future (e.g. 'label:INBOX')
            results = self._service.users().messages().list(
                userId='me', 
                maxResults=limit, 
                pageToken=cursor
            ).execute()

            messages_meta = results.get('messages', [])
            email_messages = []

            for meta in messages_meta:
                # Get basic metadata for the summary
                msg = self._service.users().messages().get(
                    userId='me', 
                    id=meta['id'], 
                    format='metadata'
                ).execute()
                
                email_messages.append(self._map_to_dto(msg))

            return email_messages
            
        except Exception as e:
            raise EmailFetchError(f"Fetch failed: {str(e)}", provider="gmail")

    async def fetch_message_body(self, message_id: str) -> Optional[EmailMessage]:
        """
        Fetch full content for a specific message.
        """
        if not self._service:
            raise EmailAuthError("Provider not connected", provider="gmail")

        try:
            msg = self._service.users().messages().get(
                userId='me', 
                id=message_id, 
                format='full'
            ).execute()
            
            return self._map_to_dto(msg, include_body=True)
            
        except Exception as e:
            raise EmailFetchError(f"Body fetch failed: {str(e)}", provider="gmail")

    async def disconnect(self) -> None:
        """Clear session data."""
        self._service = None
        self._creds = None

    def _map_to_dto(self, gmail_msg: Dict[str, Any], include_body: bool = False) -> EmailMessage:
        """Internal helper to convert Gmail API response to EmailMessage DTO."""
        payload = gmail_msg.get('payload', {})
        headers = {h['name'].lower(): h['value'] for h in payload.get('headers', [])}
        
        # Internal date is in milliseconds
        received_at_ms = int(gmail_msg.get('internalDate', 0))
        received_at = datetime.fromtimestamp(received_at_ms / 1000.0, tz=timezone.utc)

        body_text = None
        body_html = None

        if include_body:
            body_text, body_html = self._extract_body(payload)

        # Handle recipients
        to_header = headers.get('to', '')
        to_emails = [email.strip() for email in to_header.split(',') if email.strip()]

        return EmailMessage(
            provider="gmail",
            provider_message_id=gmail_msg['id'],
            thread_id=gmail_msg.get('threadId'),
            from_email=headers.get('from', ''),
            to_emails=to_emails,
            subject=headers.get('subject'),
            body_text=body_text,
            body_html=body_html,
            received_at=received_at
        )

    def _extract_body(self, payload: Dict[str, Any]) -> tuple[Optional[str], Optional[str]]:
        """Recursively extract plain and html parts from Gmail payload."""
        text = None
        html = None

        def _walk_parts(parts):
            nonlocal text, html
            for part in parts:
                mime_type = part.get('mimeType')
                data = part.get('body', {}).get('data')
                
                if data:
                    decoded = base64.urlsafe_b64decode(data).decode('utf-8', errors='replace')
                    if mime_type == 'text/plain' and not text:
                        text = decoded
                    elif mime_type == 'text/html' and not html:
                        html = decoded
                
                if 'parts' in part:
                    _walk_parts(part['parts'])

        if 'parts' in payload:
            _walk_parts(payload['parts'])
        else:
            # Single part message
            data = payload.get('body', {}).get('data')
            if data:
                decoded = base64.urlsafe_b64decode(data).decode('utf-8', errors='replace')
                mime_type = payload.get('mimeType')
                if mime_type == 'text/plain':
                    text = decoded
                elif mime_type == 'text/html':
                    html = decoded

        return text, html
