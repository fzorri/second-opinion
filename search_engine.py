"""
search_engine.py - SQLite FTS5 search engine for Second Opinion conversations.

Provides full-text search across all conversation files with BM25 ranking.
Zero external dependencies - uses only sqlite3 (built-in).

Features:
- FTS5 with unicode61 tokenizer (accent-insensitive for Spanish + English)
- BM25 ranking for relevance scoring
- Incremental indexing (only processes new/modified files)
- Event-driven deletion notification
- Startup reconciliation for consistency
"""

import os
import re
import json
import sqlite3
from datetime import datetime
from config import SEARCH_DB_PATH, MODELS_CONFIGURATION


# ─── Database Setup ───────────────────────────────────────────────────────────

def get_db():
    """Return a database connection with row_factory set."""
    conn = sqlite3.connect(SEARCH_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create the FTS5 virtual table if it doesn't exist."""
    conn = get_db()
    try:
        conn.execute('''
            CREATE VIRTUAL TABLE IF NOT EXISTS conversations USING fts5(
                file_path UNINDEXED,
                model_folder UNINDEXED,
                conversation_name,
                created_at UNINDEXED,
                total_tokens UNINDEXED,
                message_count UNINDEXED,
                content,
                tokenize='unicode61 remove_diacritics 1'
            )
        ''')
        conn.commit()
    finally:
        conn.close()


# ─── Conversation Loading ─────────────────────────────────────────────────────

def _load_conversation(file_path):
    """Load a conversation JSON file. Returns (messages, metadata) or (None, None)."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            data = json.load(f)
        
        # Handle both list and dict formats
        if isinstance(data, list):
            return data, None
        elif isinstance(data, dict):
            return data.get("messages", []), data.get("metadata")
        return None, None
    except Exception:
        return None, None


def _extract_text(messages):
    """Extract plain text from conversation messages."""
    if not messages:
        return ""
    
    text_parts = []
    for msg in messages:
        content = msg.get("content", "")
        if isinstance(content, list):
            # Multimodal content blocks
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    text_parts.append(block.get("text", ""))
        elif isinstance(content, str):
            text_parts.append(content)
    
    return " ".join(text_parts)


def _extract_preview(messages, max_chars=100):
    """Extract a short preview from conversation messages."""
    text = _extract_text(messages)
    # Remove file markers for preview
    text = re.sub(r'\[File:.*?\]', '', text)
    text = re.sub(r'\[Ref:.*?\]', '', text)
    text = re.sub(r'\[Path:.*?\]', '', text)
    text = re.sub(r'\[IMAGE:.*?\]', '', text)
    text = re.sub(r'\[Image:.*?\]', '', text)
    text = text.strip()
    
    if len(text) > max_chars:
        return text[:max_chars] + "..."
    return text


# ─── Indexing ─────────────────────────────────────────────────────────────────

def index_conversation(file_path, model_folder):
    """Index a single conversation file into the FTS5 table."""
    messages, metadata = _load_conversation(file_path)
    if messages is None:
        return False
    
    content = _extract_text(messages)
    if not content.strip():
        return False
    
    conversation_name = ""
    created_at = ""
    total_tokens = 0
    message_count = len(messages)
    
    if metadata:
        conversation_name = metadata.get("conversation_name", "")
        created_at = metadata.get("last_updated", "")
        total_tokens = metadata.get("total_tokens", 0)
    
    # Extract date from filename if not in metadata
    if not created_at:
        basename = os.path.basename(file_path)
        match = re.search(r'(\d{8}-\d{6})', basename)
        if match:
            created_at = match.group(1)
    
    conn = get_db()
    try:
        # Delete existing entry if re-indexing
        conn.execute("DELETE FROM conversations WHERE file_path = ?", (file_path,))
        
        # Insert new entry
        conn.execute('''
            INSERT INTO conversations (file_path, model_folder, conversation_name, 
                                      created_at, total_tokens, message_count, content)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (file_path, model_folder, conversation_name, created_at, 
              total_tokens, message_count, content))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"  Error indexing {os.path.basename(file_path)}: {e}")
        return False
    finally:
        conn.close()


def bulk_index_all(progress_callback=None):
    """Scan all model folders and index conversation files.
    
    Args:
        progress_callback: Optional function(indexed, total) called during indexing.
    
    Returns:
        tuple: (indexed_count, skipped_count, error_count)
    """
    init_db()
    
    # Collect all model folders
    model_folders = {}
    for provider_data in MODELS_CONFIGURATION.get("providers", {}).values():
        for model in provider_data.get("models", []):
            folder = model.get("model_folder", "")
            if folder:
                model_folders[os.path.normpath(folder)] = model.get("model_name", "")
    
    # Also scan for orphaned folders
    models_dir = os.path.join(os.path.dirname(__file__), "models")
    if os.path.isdir(models_dir):
        for item in os.listdir(models_dir):
            item_path = os.path.join(models_dir, item)
            if os.path.isdir(item_path) and not item.startswith("."):
                norm_path = os.path.normpath(item_path)
                if norm_path not in model_folders:
                    model_folders[norm_path] = f"Orphaned ({item})"
    
    # Scan and index
    indexed = 0
    skipped = 0
    errors = 0
    
    # Get already indexed files
    conn = get_db()
    try:
        indexed_files = set()
        for row in conn.execute("SELECT file_path FROM conversations"):
            indexed_files.add(row["file_path"])
    finally:
        conn.close()
    
    # Count total files first
    total_files = 0
    for folder_path in model_folders:
        if os.path.isdir(folder_path):
            for filename in os.listdir(folder_path):
                if filename.startswith("conversation_history_") and filename.endswith(".json"):
                    total_files += 1
    
    # Index files
    processed = 0
    for folder_path, model_name in model_folders.items():
        if not os.path.isdir(folder_path):
            continue
        
        for filename in os.listdir(folder_path):
            if not (filename.startswith("conversation_history_") and filename.endswith(".json")):
                continue
            
            file_path = os.path.join(folder_path, filename)
            processed += 1
            
            # Skip if already indexed
            if file_path in indexed_files:
                skipped += 1
                continue
            
            # Index the file
            try:
                success = index_conversation(file_path, folder_path)
                if success:
                    indexed += 1
                else:
                    errors += 1
            except Exception:
                errors += 1
            
            # Report progress
            if progress_callback:
                progress_callback(processed, total_files)
    
    return indexed, skipped, errors


# ─── Search ───────────────────────────────────────────────────────────────────

def _sanitize_query(query):
    """Sanitize a search query for FTS5 MATCH syntax."""
    # Remove FTS5 special characters
    sanitized = re.sub(r'["\(\)\*\+\-\:\;\{\}\[\]\/\\]', ' ', query)
    # Collapse whitespace
    sanitized = re.sub(r'\s+', ' ', sanitized).strip()
    return sanitized


def search_conversations(query, limit=10):
    """Search conversations using FTS5 with BM25 ranking.
    
    Args:
        query: Search query string
        limit: Maximum number of results to return
    
    Returns:
        list of dicts with keys: file_path, model_folder, conversation_name,
                                  created_at, total_tokens, message_count, snippet, rank
    """
    sanitized = _sanitize_query(query)
    if not sanitized:
        return []
    
    init_db()
    conn = get_db()
    try:
        results = conn.execute('''
            SELECT 
                file_path,
                model_folder,
                conversation_name,
                created_at,
                total_tokens,
                message_count,
                snippet(conversations, 6, '<b>', '</b>', '...', 30) as snippet,
                bm25(conversations) as rank
            FROM conversations
            WHERE conversations MATCH ?
            ORDER BY rank
            LIMIT ?
        ''', (sanitized, limit)).fetchall()
        
        return [dict(row) for row in results]
    except sqlite3.OperationalError:
        # Query syntax error - try with sanitized terms
        return []
    finally:
        conn.close()


# ─── Deletion ─────────────────────────────────────────────────────────────────

def remove_from_index(file_path):
    """Remove a conversation from the search index by file_path.
    
    This function is idempotent - no error if file_path not found.
    """
    init_db()
    conn = get_db()
    try:
        conn.execute("DELETE FROM conversations WHERE file_path = ?", (file_path,))
        conn.commit()
    except Exception:
        pass
    finally:
        conn.close()


def notify_deletion(file_path):
    """Notify the search index that a conversation has been deleted.
    
    This is the public function to call from history.py.
    Catches exceptions silently to avoid blocking deletion operations.
    """
    try:
        remove_from_index(file_path)
    except Exception:
        pass


# ─── Reconciliation ───────────────────────────────────────────────────────────

def reconcile_index():
    """Reconcile the search index with actual files on disk.
    
    - Removes stale entries (file no longer exists)
    - Adds missing entries (file exists but not indexed)
    
    Returns:
        tuple: (added_count, removed_count)
    """
    init_db()
    
    conn = get_db()
    try:
        # Get all indexed file paths
        indexed_files = set()
        for row in conn.execute("SELECT file_path FROM conversations"):
            indexed_files.add(row["file_path"])
        
        # Check which files still exist
        removed = 0
        for file_path in list(indexed_files):
            if not os.path.exists(file_path):
                conn.execute("DELETE FROM conversations WHERE file_path = ?", (file_path,))
                removed += 1
        
        conn.commit()
    finally:
        conn.close()
    
    # Index any missing files
    added = 0
    for provider_data in MODELS_CONFIGURATION.get("providers", {}).values():
        for model in provider_data.get("models", []):
            folder = model.get("model_folder", "")
            if not folder or not os.path.isdir(folder):
                continue
            
            for filename in os.listdir(folder):
                if not (filename.startswith("conversation_history_") and filename.endswith(".json")):
                    continue
                
                file_path = os.path.join(folder, filename)
                if file_path not in indexed_files:
                    try:
                        success = index_conversation(file_path, folder)
                        if success:
                            added += 1
                    except Exception:
                        pass
    
    return added, removed


# ─── Utility ──────────────────────────────────────────────────────────────────

def get_conversation(file_path):
    """Load a full conversation for display.
    
    Returns:
        tuple: (messages_list, metadata_dict) or (None, None)
    """
    return _load_conversation(file_path)


def is_indexed(file_path):
    """Check if a conversation is in the search index."""
    init_db()
    conn = get_db()
    try:
        row = conn.execute(
            "SELECT 1 FROM conversations WHERE file_path = ?", 
            (file_path,)
        ).fetchone()
        return row is not None
    finally:
        conn.close()


def get_index_stats():
    """Get statistics about the search index.
    
    Returns:
        dict with total_count, indexed_folders, etc.
    """
    init_db()
    conn = get_db()
    try:
        total = conn.execute("SELECT COUNT(*) as cnt FROM conversations").fetchone()["cnt"]
        folders = conn.execute(
            "SELECT DISTINCT model_folder FROM conversations"
        ).fetchall()
        return {
            "total_conversations": total,
            "indexed_folders": len(folders),
        }
    finally:
        conn.close()


# ─── UI Functions ─────────────────────────────────────────────────────────────

def _strip_html(text):
    """Remove HTML tags from snippet text."""
    return re.sub(r'<[^>]+>', '', text)


def _format_date(created_at):
    """Format a date string for display."""
    if not created_at:
        return "Unknown date"
    # Handle YYYYMMDD-HHMMSS format
    if len(created_at) >= 15 and created_at[8] == '-':
        try:
            return f"{created_at[:4]}-{created_at[4:6]}-{created_at[6:8]} {created_at[9:11]}:{created_at[11:13]}:{created_at[13:15]}"
        except Exception:
            return created_at
    return created_at


def _get_model_name(model_folder):
    """Get the model name from a model folder path."""
    for provider_data in MODELS_CONFIGURATION.get("providers", {}).values():
        for model in provider_data.get("models", []):
            if model.get("model_folder") == model_folder:
                return model.get("model_name", os.path.basename(model_folder))
    # Check if it's an orphaned folder
    folder_name = os.path.basename(model_folder)
    return f"Orphaned ({folder_name})"


def display_results(results):
    """Display search results in a formatted list.
    
    Args:
        results: List of result dicts from search_conversations()
    
    Returns:
        Number of results displayed
    """
    if not results:
        print("\n  No results found.")
        return 0
    
    print(f"\n  Found {len(results)} result(s):\n")
    
    for i, result in enumerate(results, 1):
        date = _format_date(result.get("created_at", ""))
        model_name = _get_model_name(result.get("model_folder", ""))
        name = result.get("conversation_name", "")
        tokens = result.get("total_tokens", 0)
        msg_count = result.get("message_count", 0)
        snippet = _strip_html(result.get("snippet", ""))
        
        # Build display line
        display_name = f'"{name}"' if name else "Unnamed conversation"
        
        print(f"  {i}. [{date}] {display_name} ({model_name})")
        print(f"     Tokens: {tokens:,} | Messages: {msg_count}")
        if snippet:
            print(f"     \"{snippet}\"")
        print()
    
    return len(results)


def handle_selection(results):
    """Handle user selection from search results.
    
    Args:
        results: List of result dicts from search_conversations()
    
    Returns:
        str: file_path if user selected a conversation, None otherwise
    """
    if not results:
        return None
    
    while True:
        try:
            choice = input("  Enter number to view, S+number to select & chat, Q to quit: ").strip()
            
            if not choice:
                continue
            
            if choice.upper() == "Q":
                return None
            
            # Handle "S1", "S2", etc.
            if choice.upper().startswith("S") and choice[1:].isdigit():
                idx = int(choice[1:]) - 1
                if 0 <= idx < len(results):
                    return results[idx]["file_path"]
                print("  Invalid selection.")
                continue
            
            # Handle plain numbers for view
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(results):
                    file_path = results[idx]["file_path"]
                    _view_conversation(file_path)
                    continue
                print("  Invalid selection.")
                continue
            
            print("  Invalid input. Use number, S+number, or Q.")
            
        except KeyboardInterrupt:
            print()
            return None
        except EOFError:
            return None


def _view_conversation(file_path):
    """Display a conversation using the existing History.print_conversation pattern."""
    try:
        # Import here to avoid circular imports
        from history import History
        
        # Determine the model folder
        model_folder = os.path.dirname(file_path)
        
        # Create a temporary History instance and use print_conversation
        history = History(model_folder)
        history.print_conversation(file_path)
    except Exception as e:
        print(f"  Error viewing conversation: {e}")


def handle_search():
    """Main search handler - prompts for query, searches, and handles results.
    
    This is the function called from secop.py when user types /search.
    """
    from tools import Tools
    
    print("\n  SEARCH ALL CONVERSATIONS")
    print("  " + "-" * 40)
    
    try:
        query = input("  Enter search query: ").strip()
    except (KeyboardInterrupt, EOFError):
        print()
        return None
    
    if not query:
        print("  Empty query.")
        return None
    
    # Check if index is empty
    try:
        stats = get_index_stats()
        if stats["total_conversations"] == 0:
            print("\n  Search index is empty. Building index...")
            _show_indexing_progress()
    except Exception as e:
        print(f"\n  Error checking index: {e}")
        return None
    
    # Search
    try:
        results = search_conversations(query, limit=10)
    except Exception as e:
        print(f"\n  Search error: {e}")
        return None
    
    # Display results
    display_results(results)
    
    # Handle selection
    return handle_selection(results)


def _show_indexing_progress():
    """Show indexing progress."""
    try:
        indexed, skipped, errors = bulk_index_all()
        print(f"\n  Indexed: {indexed} | Skipped: {skipped} | Errors: {errors}")
        if indexed > 0:
            print("  Index built successfully.")
        elif indexed == 0 and skipped == 0 and errors == 0:
            print("  No conversation files found to index.")
    except Exception as e:
        print(f"\n  Indexing error: {e}")
