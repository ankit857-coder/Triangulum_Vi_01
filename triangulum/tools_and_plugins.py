import time
from langchain.tools import Tool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from duckduckgo_search import DDGS
from scholarly import scholarly
import pandas as pd

# First, let's try to import arxiv and pubmed tools, if not available, we'll skip them
try:
    import arxiv
    has_arxiv = True
except ImportError:
    has_arxiv = False

try:
    from Bio import Entrez
    has_pubmed = True
except ImportError:
    has_pubmed = False

# DuckDuckGo Search Tool
def real_info(query: str, max_results=3) -> str:
    """
    Perform a search using DuckDuckGo and format results for real-time data
    
    Args:
        query (str): Search query
        max_results (int): Maximum number of results to return
    
    Returns:
        str: Formatted search results focusing on current data
    """
    try:
        with DDGS() as ddgs:            # Enhance query for real-time results
            enhanced_query = f"current {query} live price today"
            results = list(ddgs.text(
                keywords=enhanced_query,
                max_results=max_results,
                region='wt-wt',
                safesearch='moderate'
            ))
            
            if not results:
                return f"No results found for: {query}"
                
            output = f"\nLatest data for: {query}\n\n"
            for i, result in enumerate(results, 1):
                title = result.get('title', 'No title available')
                body = result.get('body', result.get('snippet', 'No description available'))
                
                # Extract and format the most relevant information
                output += f"Source {i}:\n"
                output += f"Title: {title}\n"
                output += f"Details: {body}\n\n"
            
            return output
    
    except Exception as e:
        return f"An error occurred while searching: {str(e)}"

# Google Scholar Tool
def scholar_search(query: str, max_results=3) -> str:
    """
    Search Google Scholar for academic papers and citations
    
    Args:
        query (str): Search query
        max_results (int): Maximum number of results to return
    
    Returns:
        str: Formatted search results from Google Scholar
    """
    try:
        search_query = scholarly.search_pubs(query)
        results = []
        
        for i in range(max_results):
            try:
                pub = next(search_query)
                results.append({
                    'title': pub.get('bib', {}).get('title', 'No title'),
                    'author': pub.get('bib', {}).get('author', 'No author'),
                    'year': pub.get('bib', {}).get('year', 'No year'),
                    'citations': pub.get('num_citations', 0)
                })
            except StopIteration:
                break
                
        if not results:
            return f"No results found for: {query}"
            
        output = f"\nScholar results for: {query}\n\n"
        for i, result in enumerate(results, 1):
            output += f"Paper {i}:\n"
            output += f"Title: {result['title']}\n"
            output += f"Author(s): {result['author']}\n"
            output += f"Year: {result['year']}\n"
            output += f"Citations: {result['citations']}\n\n"
            
        return output
        
    except Exception as e:
        return f"An error occurred while searching Scholar: {str(e)}"

# Initialize the base tools list with always-available tools
tools = []

# Wikipedia Tool
wiki_tool = Tool(
    name="Wikipedia",
    func=WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper()).run,
    description="Useful for getting general information, historical data, and detailed explanations. Best for non-time-sensitive information.",
)
tools.append(wiki_tool)

# DuckDuckGo Tool
real_time_information = Tool(
    name="DuckDuckGo",
    func=real_info,
    description="Useful for getting real-time data like current prices, market values, latest news, and live updates. Best for time-sensitive information.",
)
tools.append(real_time_information)

# Google Scholar Tool
scholar_tool = Tool(
    name="GoogleScholar",
    func=scholar_search,
    description="Useful for finding academic papers across all disciplines, citation counts, and scholarly impact. Best for academic research.",
)
tools.append(scholar_tool)

# ArXiv Tool (only if available)
if has_arxiv:
    def arxiv_search(query: str, max_results=3) -> str:
        """Search arXiv for papers"""
        try:
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            results = list(search.results())
            
            if not results:
                return f"No results found for: {query}"
                
            output = f"\nArXiv results for: {query}\n\n"
            for i, result in enumerate(results, 1):
                output += f"Paper {i}:\n"
                output += f"Title: {result.title}\n"
                output += f"Authors: {', '.join(result.authors)}\n"
                output += f"Published: {result.published}\n"
                output += f"Summary: {result.summary[:200]}...\n"
                output += f"URL: {result.pdf_url}\n\n"
                
            return output
            
        except Exception as e:
            return f"An error occurred while searching ArXiv: {str(e)}"
    
    arxiv_tool = Tool(
        name="ArXiv",
        func=arxiv_search,
        description="Useful for finding scientific papers, especially in physics, mathematics, computer science, and related fields.",
    )
    tools.append(arxiv_tool)

# PubMed Tool (only if available)
if has_pubmed:
    def pubmed_search(query: str, max_results=3) -> str:
        """Search PubMed for papers"""
        try:
            Entrez.email = "your-email@example.com"  # Please replace with your email
            handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
            record = Entrez.read(handle)
            
            if not record["IdList"]:
                return f"No results found for: {query}"
                
            output = f"\nPubMed results for: {query}\n\n"
            for i, paper_id in enumerate(record["IdList"], 1):
                paper = Entrez.efetch(db="pubmed", id=paper_id, rettype="gb")
                paper_details = Entrez.read(paper)
                
                output += f"Paper {i}:\n"
                output += f"Title: {paper_details['Title']}\n"
                output += f"Authors: {', '.join(paper_details.get('Authors', ['No authors listed']))}\n"
                output += f"Journal: {paper_details.get('Journal', 'No journal listed')}\n"
                output += f"Abstract: {paper_details.get('Abstract', 'No abstract available')[:200]}...\n\n"
                
            return output
            
        except Exception as e:
            return f"An error occurred while searching PubMed: {str(e)}"
    
    pubmed_tool = Tool(
        name="PubMed",
        func=pubmed_search,
        description="Useful for finding medical and life sciences research papers.",
    )
    tools.append(pubmed_tool)

if __name__ == "__main__":
    # Test the tools here if needed
    pass
