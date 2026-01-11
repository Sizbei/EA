from composio import Composio

class InboxCleaner:
    def __init__(self, toolset: Composio, entity_id: str = "default"):
        self.toolset = toolset
        self.entity_id = entity_id

    def list_potential_bloat(self):
        """
        Identify senders with many emails in the inbox.
        """
        print("🔍 Scanning inbox for potential bloat...")
        
        # 1. Fetch recent emails
        result = self.toolset.tools.execute(
            slug="GMAIL_FETCH_EMAILS",
            arguments={"q": "", "max_results": 50},
            user_id=self.entity_id,
            dangerously_skip_version_check=True
        )
        
        # Accessing the specific field
        data = result.get('data', {}) if isinstance(result, dict) else {}
        emails = data.get('emails', [])
        
        if not emails:
            print("✨ Inbox looks clean! No emails found.")
            return []

        # 2. Group by sender
        from collections import Counter
        senders = Counter([e.get('sender', 'Unknown') for e in emails])
        
        print(f"\nAnalyzed {len(emails)} recent emails.")
        print("📁 Top Senders in Inbox:")
        for sender, count in senders.most_common(10):
            print(f" - {count:2d} emails from: {sender}")
            
        return emails

    def archive_by_query(self, query: str):
        """
        Archive all emails matching a query.
        """
        print(f"📦 Archiving emails matching: {query}")
        
        # 1. Get IDs
        result = self.toolset.tools.execute(
            slug="GMAIL_FETCH_EMAILS",
            arguments={"q": query, "max_results": 100},
            user_id=self.entity_id,
            dangerously_skip_version_check=True
        )
        
        emails = result.data.get('emails', []) if hasattr(result, 'data') else result.get('emails', [])
        ids = [e.get('messageId') for e in emails if e.get('messageId')]
        
        if not ids:
            print("No matching emails found.")
            return

        # 2. Batch modify (remove INBOX label)
        self.toolset.tools.execute(
            slug="GMAIL_BATCH_MODIFY_MESSAGES",
            arguments={
                "ids": ids,
                "remove_label_ids": ["INBOX"]
            },
            user_id=self.entity_id,
            dangerously_skip_version_check=True
        )
        
        print(f"✅ Successfully archived {len(ids)} emails.")
