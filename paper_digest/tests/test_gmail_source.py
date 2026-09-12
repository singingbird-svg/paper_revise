import unittest
from email.message import EmailMessage

from paper_digest.gmail_source import _papers_from_message


class GmailSourceTests(unittest.TestCase):
    def test_extracts_paper_like_links_from_html_email(self) -> None:
        msg = EmailMessage()
        msg["Subject"] = "Google Scholar Alerts"
        msg["From"] = "scholaralerts-noreply@google.com"
        msg["Date"] = "Sat, 12 Apr 2026 08:00:00 +0800"
        msg.set_content("plain fallback")
        msg.add_alternative(
            """
            <html><body>
            <a href="https://example.org/paper1">A multi-agent planning method with LTL constraints</a>
            <p>This paper proposes a new decomposition strategy for distributed task allocation.</p>
            <a href="https://alerts.google.com">Manage alerts</a>
            </body></html>
            """,
            subtype="html",
        )

        papers = _papers_from_message(msg)
        self.assertEqual(len(papers), 1)
        self.assertEqual(papers[0].title, "A multi-agent planning method with LTL constraints")

