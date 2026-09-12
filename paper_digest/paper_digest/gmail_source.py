from __future__ import annotations

import email
import html
import imaplib
import os
import re
from datetime import date
from email.message import Message
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser

from .models import Paper


class AnchorCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.current_href = ""
        self.current_text: list[str] = []
        self.anchors: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() == "a":
            self.current_href = dict(attrs).get("href", "") or ""
            self.current_text = []

    def handle_data(self, data: str) -> None:
        if self.current_href:
            self.current_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a" and self.current_href:
            text = " ".join(" ".join(self.current_text).split())
            if text and self.current_href:
                self.anchors.append((text, self.current_href))
            self.current_href = ""
            self.current_text = []


def fetch_gmail_alerts(target_date: date, gmail_config: dict) -> list[Paper]:
    if not gmail_config.get("enabled"):
        return []

    username = gmail_config.get("username", "")
    password_env = gmail_config.get("password_env", "")
    password = os.getenv(password_env, "")
    if not username or not password:
        raise ValueError("gmail username or password env is missing")

    host = gmail_config.get("host", "imap.gmail.com")
    port = int(gmail_config.get("port", 993))
    folders = gmail_config.get("folders", ["INBOX"])
    from_filters = [item.lower() for item in gmail_config.get("from_filters", [])]
    subject_keywords = [item.lower() for item in gmail_config.get("subject_keywords", [])]

    mail = imaplib.IMAP4_SSL(host, port)
    try:
        mail.login(username, password)
        results: list[Paper] = []
        for folder in folders:
            status, _ = mail.select(folder, readonly=True)
            if status != "OK":
                continue
            status, data = mail.search(None, "SINCE", _imap_date(target_date))
            if status != "OK":
                continue
            for msg_id in reversed((data[0] or b"").split()):
                status, raw = mail.fetch(msg_id, "(RFC822)")
                if status != "OK" or not raw or not raw[0]:
                    continue
                message = email.message_from_bytes(raw[0][1])
                if not _message_matches(message, target_date, from_filters, subject_keywords):
                    continue
                results.extend(_papers_from_message(message))
        return results
    finally:
        try:
            mail.logout()
        except Exception:
            pass


def _imap_date(value: date) -> str:
    return value.strftime("%d-%b-%Y")


def _message_matches(message: Message, target_date: date, from_filters: list[str], subject_keywords: list[str]) -> bool:
    from_header = (message.get("From") or "").lower()
    subject = (message.get("Subject") or "").lower()
    if from_filters and not any(item in from_header for item in from_filters):
        return False
    if subject_keywords and not any(item in subject for item in subject_keywords):
        return False
    when = parsedate_to_datetime(message.get("Date", "")) if message.get("Date") else None
    if when and when.date() != target_date:
        return False
    return True


def _papers_from_message(message: Message) -> list[Paper]:
    html_body = _extract_body(message, "text/html")
    text_body = _extract_body(message, "text/plain")
    anchors = _extract_anchors(html_body)
    description = _normalize_space(html.unescape(_strip_tags(html_body or text_body)))
    published = ""
    if message.get("Date"):
        try:
            published = parsedate_to_datetime(message.get("Date", "")).date().isoformat()
        except Exception:
            published = ""

    papers: list[Paper] = []
    for title, url in anchors:
        if not _looks_like_paper_link(title, url):
            continue
        papers.append(
            Paper(
                source="Gmail Alerts",
                title=title,
                abstract=_nearest_snippet(description, title),
                authors=[],
                url=url,
                published=published,
                venue="Google email alert",
            )
        )
    return papers


def _extract_body(message: Message, content_type: str) -> str:
    if message.is_multipart():
        for part in message.walk():
            if part.get_content_type() == content_type:
                payload = part.get_payload(decode=True) or b""
                charset = part.get_content_charset() or "utf-8"
                return payload.decode(charset, errors="ignore")
        return ""
    if message.get_content_type() == content_type:
        payload = message.get_payload(decode=True) or b""
        charset = message.get_content_charset() or "utf-8"
        return payload.decode(charset, errors="ignore")
    return ""


def _extract_anchors(html_body: str) -> list[tuple[str, str]]:
    if not html_body:
        return []
    parser = AnchorCollector()
    parser.feed(html_body)
    return parser.anchors


def _looks_like_paper_link(title: str, url: str) -> bool:
    blocked = ["unsubscribe", "preferences", "help.google", "support.google"]
    if len(title.split()) < 3:
        return False
    lowered = f"{title} {url}".lower()
    return not any(item in lowered for item in blocked)


def _strip_tags(text: str) -> str:
    return re.sub(r"<[^>]+>", " ", text)


def _normalize_space(text: str) -> str:
    return " ".join(text.split())


def _nearest_snippet(description: str, title: str) -> str:
    if not description:
        return ""
    index = description.find(title)
    if index < 0:
        return description[:400]
    start = min(len(description), index + len(title))
    snippet = description[start : start + 400].strip(" -:;|")
    return snippet[:400]
