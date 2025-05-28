import time
import re
from datetime import datetime
from functools import wraps
from typing import List, Dict, Any, Callable, Optional
from langchain.tools import Tool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from duckduckgo_search import DDGS
from scholarly import scholarly
import pandas as pd

# Retry decorator for handling transient errors
def retry_with_backoff(retries=3, backoff_in_seconds=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            x = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if x == retries:
                        raise e
                    sleep = (backoff_in_seconds * 2 ** x)
                    time.sleep(sleep)
                    x += 1
        return wrapper
    return decorator

def extract_year_from_text(text: str) -> Optional[str]:
    """Extract year from text using various patterns"""
    # Look for years between 2000 and current year
    current_year = datetime.now().year
    year_pattern = rf'(20[0-2][0-{str(current_year)[-1]}])'
    
    # Try different contexts where years might appear
    contexts = [
        r'published in ' + year_pattern,
        r'Published: ' + year_pattern,
        r'©' + year_pattern,
        r'\((' + year_pattern + r')\)',
        year_pattern  # Just look for the year itself
    ]
    
    for pattern in contexts:
        match = re.search(pattern, text)
        if match:
            year = match.group(1)
            if 2000 <= int(year) <= current_year:
                return year
    return None

@retry_with_backoff()
def scholar_search(query: str, max_results=3) -> str:
    """
    Search Google Scholar with improved metadata extraction
    """
    try:
        search_query = scholarly.search_pubs(query)
        results = []
        
        for i in range(max_results):
            try:
                pub = next(search_query)
                bib = pub.get('bib', {})
                
                # Extract year from multiple possible sources
                year = None
                if bib.get('year'):
                    year = bib['year']
                elif bib.get('pub_year'):
                    year = bib['pub_year']
                elif pub.get('year'):
                    year = pub['year']
                elif bib.get('abstract'):
                    year = extract_year_from_text(bib['abstract'])
                elif bib.get('title'):
                    year = extract_year_from_text(bib['title'])
                
                authors = bib.get('author', [])
                if isinstance(authors, str):
                    authors = [authors]
                
                results.append({
                    'title': bib.get('title', 'No title'),
                    'author': authors,
                    'year': year or 'Recent',
                    'citations': pub.get('num_citations', 0),
                    'abstract': bib.get('abstract', 'No abstract available'),
                    'venue': bib.get('venue', 'Unknown venue')
                })
            except StopIteration:
                break
            except Exception as e:
                continue
                
        if not results:
            return f"No results found for: {query}"
            
        output = f"\nScholar results for: {query}\n\n"
        for i, result in enumerate(results, 1):
            output += f"Paper {i}:\n"
            output += f"Title: {result['title']}\n"
            output += f"Author(s): {', '.join(str(a) for a in result['author'])}\n"
            output += f"Year: {result['year']}\n"
            output += f"Citations: {result['citations']}\n"
            output += f"Venue: {result['venue']}\n"
            output += f"Abstract: {result['abstract'][:300]}...\n\n"
            
        return output
    except Exception as e:
        return f"An error occurred while searching Google Scholar: {str(e)}"

@retry_with_backoff()
def real_info(query: str, max_results=3) -> str:
    """
    Enhanced DuckDuckGo search with better filtering and formatting
    """
    try:
        with DDGS() as ddgs:
            enhanced_query = f"latest {query} recent developments"
            results = list(ddgs.text(
                keywords=enhanced_query,
                max_results=max_results * 2,  # Get more results to filter
                region='wt-wt',
                safesearch='moderate'
            ))
            
            if not results:
                return f"No results found for: {query}"
            
            # Filter and sort results
            filtered_results = []
            for result in results:
                title = result.get('title', '')
                body = result.get('body', result.get('snippet', ''))
                
                # Skip results that don't seem recent or relevant
                if not any(word in body.lower() for word in ['recent', 'latest', 'new', '2023', '2024', '2025']):
                    continue
                    
                filtered_results.append({
                    'title': title,
                    'body': body,
                    'date': extract_year_from_text(body) or 'Recent'
                })
            
            # Take the top max_results
            filtered_results = filtered_results[:max_results]
                
            output = f"\nLatest developments for: {query}\n\n"
            for i, result in enumerate(filtered_results, 1):
                output += f"Source {i}:\n"
                output += f"Title: {result['title']}\n"
                output += f"Date: {result['date']}\n"
                output += f"Details: {result['body']}\n\n"
            
            return output
    
    except Exception as e:
        return f"An error occurred while searching DuckDuckGo: {str(e)}"

@retry_with_backoff()
def wiki_search(query: str) -> str:
    """
    Enhanced Wikipedia search with better error handling
    """
    try:
        wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
        result = wikipedia.run(query)
        if not result or len(result.strip()) < 20:  # Very short results are likely errors
            return f"No relevant Wikipedia results found for: {query}"
        return result
    except Exception as e:
        return f"An error occurred while searching Wikipedia: {str(e)}"

# Define the tools list with improved descriptions
tools = [
    Tool(
        name="DuckDuckGo",
        func=real_info,
        description="Use this tool when you need to find current information, news, or recent developments. The tool automatically filters for recent content."
    ),
    Tool(
        name="GoogleScholar",
        func=scholar_search,
        description="Use this tool when you need to find academic papers and research. The tool attempts to extract publication years and venue information."
    ),
    Tool(
        name="Wikipedia",
        func=wiki_search,
        description="Use this tool when you need to find general knowledge or background information. The tool provides comprehensive article summaries."
    )
]

if __name__ == "__main__":
    # Test the tools here if needed
    pass
